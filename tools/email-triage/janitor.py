#!/usr/bin/env python3
"""
Email Janitor — Zero-LLM Gmail noise archiving CLI.

Layer 1 of the Email Triage System:
Pattern-matches incoming email against a noise-sender database,
batch-archives matched messages, and logs structured JSONL output.

Safe for cron. Idempotent. No LLM calls.
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # fallback to json for config loading

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print(
        "Missing Google API libraries. Install with:\n"
        "  pip install --upgrade google-api-python-client "
        "google-auth-httplib2 google-auth-oauthlib"
    )
    sys.exit(1)


# ─── Helpers ────────────────────────────────────────────────────────────────


def load_yaml(path: str) -> dict:
    """Load a YAML file, falling back to JSON if PyYAML is missing."""
    if yaml:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    import json as _json
    with open(path) as f:
        return _json.load(f)


def extract_domain(address: str) -> str:
    """Extract the domain part from an email address."""
    if '<' in address:
        # "Display Name <email@domain.com>"
        address = address.split('<')[1].split('>')[0]
    address = address.strip()
    if '@' in address:
        return address.split('@')[1].lower()
    return address.lower()


def extract_sender(address: str) -> str:
    """Extract the full email address from a possibly-display-named string."""
    if '<' in address:
        address = address.split('<')[1].split('>')[0]
    return address.strip().lower()


def glob_match(pattern: str, value: str) -> bool:
    """
    Simple glob matching for email patterns.
    Supports: *@domain, *@sub.domain, *@*
    """
    if pattern == '*':
        return True
    if pattern.startswith('*@'):
        domain_part = pattern[2:]
        if domain_part == '*':
            return True
        if value.endswith(domain_part):
            return True
        return False
    return pattern.lower() == value.lower()


def subject_match(subject: str, patterns: list) -> bool:
    """Match subject line against regex patterns (e.g. /sale|discount/i)."""
    if not patterns:
        return False
    for pattern in patterns:
        if pattern.startswith('/') and pattern.count('/') >= 2:
            # Parse /pattern/flags
            parts = pattern[1:].split('/')
            if len(parts) >= 1:
                regex = parts[0]
                flags = re.IGNORECASE if len(parts) >= 2 and 'i' in parts[1] else 0
                try:
                    if re.search(regex, subject, flags):
                        return True
                except re.error:
                    continue
    return False


def categorize_sender(sender: str, subject: str, noise_db: dict) -> str | None:
    """
    Check a sender+subject against the noise database.
    Returns the category name (e.g. 'promotions') or None if no match.
    """
    domain = extract_domain(sender)
    sender_lower = sender.lower()

    for category, config in noise_db.items():
        if not isinstance(config, dict):
            continue
        if config.get('description', '').startswith(
            'Security alerts — NOT archived'
        ):
            continue  # security is handled separately

        patterns = config.get('patterns', [])
        subject_pats = config.get('subject_patterns', [])

        for pattern in patterns:
            pattern_lower = pattern.lower()
            # Exact domain pattern: *@domain
            if pattern.startswith('*@'):
                if glob_match(pattern, domain):
                    return category
            # Exact email pattern
            elif glob_match(pattern, sender_lower):
                return category
            # Wildcard match against the full address
            elif pattern.endswith('*') and sender_lower.startswith(pattern[:-1]):
                return category
            elif pattern.startswith('*') and sender_lower.endswith(pattern[1:]):
                return category

        # Check subject patterns
        if subject_pats and subject_match(subject, subject_pats):
            return category

    return None


def is_security_sender(sender: str, subject: str, noise_db: dict) -> bool:
    """Check if a sender matches the security category (log only, no archive)."""
    domain = extract_domain(sender)
    sender_lower = sender.lower()
    security = noise_db.get('security', {})
    if not isinstance(security, dict):
        return False

    # Check patterns
    for pattern in security.get('patterns', []):
        pattern_lower = pattern.lower()
        if pattern.startswith('*@'):
            if glob_match(pattern, domain):
                return True
        elif glob_match(pattern, sender_lower):
            return True

    # Check subject patterns
    if security.get('subject_patterns') and subject_match(
        subject, security['subject_patterns']
    ):
        return True

    return False


def is_safe_sender(sender: str, safe_senders: list) -> bool:
    """Check if a sender is on the safe-sender allowlist."""
    sender_lower = sender.lower()
    domain = extract_domain(sender)
    for entry in safe_senders:
        entry_lower = entry.lower()
        if glob_match(entry_lower, sender_lower) or glob_match(entry_lower, domain):
            return True
        if entry_lower == sender_lower:
            return True
    return False


# ─── Gmail API ──────────────────────────────────────────────────────────────


def get_gmail_service(credentials_path: str):
    """Build and return an authenticated Gmail API service."""
    creds_path = os.path.expanduser(credentials_path)
    if not os.path.exists(creds_path):
        raise FileNotFoundError(
            f"Credentials not found at {creds_path}. "
            "Run the OAuth setup first (see references/gmail-api-setup.md)."
        )

    creds = Credentials.from_authorized_user_file(creds_path)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        with open(creds_path, 'w') as f:
            f.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def fetch_labels(service) -> dict:
    """Fetch all labels. Returns dict of label_name -> label_id."""
    try:
        result = service.users().labels().list(userId='me').execute()
        labels = result.get('labels', [])
        return {label['name']: label['id'] for label in labels}
    except HttpError as e:
        logging.error(f"Failed to fetch labels: {e}")
        return {}


def fetch_inbox_messages(
    service, max_results: int = 200
) -> list:
    """Fetch messages from INBOX."""
    try:
        result = (
            service.users()
            .messages()
            .list(userId='me', labelIds=['INBOX'], maxResults=max_results)
            .execute()
        )
        return result.get('messages', [])
    except HttpError as e:
        logging.error(f"Failed to list inbox messages: {e}")
        return []


def get_message_details(service, msg_id: str) -> dict | None:
    """Fetch full message details including headers."""
    try:
        msg = (
            service.users()
            .messages()
            .get(userId='me', id=msg_id, format='metadata')
            .execute()
        )
        headers = {h['name'].lower(): h['value'] for h in msg.get('payload', {}).get('headers', [])}
        return {
            'id': msg_id,
            'from': headers.get('from', ''),
            'subject': headers.get('subject', ''),
            'date': headers.get('date', ''),
            'label_ids': msg.get('labelIds', []),
        }
    except HttpError as e:
        logging.warning(f"Failed to get message {msg_id}: {e}")
        return None


def find_label_id(label_name: str, labels: dict) -> str | None:
    """Find a label ID by name (case-insensitive fuzzy match)."""
    # Exact match first
    if label_name in labels:
        return labels[label_name]

    # Try case-insensitive
    for name, lid in labels.items():
        if name.lower() == label_name.lower():
            return lid

    # Try with normalized domain
    return None


def archive_messages(
    service, msg_ids: list, label_ids_to_add: list | None = None, batch_size: int = 50
) -> dict:
    """
    Batch-archive messages (remove from INBOX).
    Optionally apply labels.
    Returns stats dict.
    """
    archived = 0
    errors = []

    for i in range(0, len(msg_ids), batch_size):
        batch = msg_ids[i : i + batch_size]
        body = {
            'ids': batch,
            'removeLabelIds': ['INBOX'],
        }
        if label_ids_to_add:
            body['addLabelIds'] = label_ids_to_add

        try:
            service.users().messages().batchModify(userId='me', body=body).execute()
            archived += len(batch)
        except HttpError as e:
            errors.append(f"Batch {i//batch_size}: {e}")

        # Rate limiting
        if i + batch_size < len(msg_ids):
            time.sleep(1.0 / 5)  # default 5 batches/sec

    return {'archived': archived, 'errors': errors}


# ─── Config Loading ─────────────────────────────────────────────────────────


def load_config(config_path: str) -> dict:
    """Load and validate Janitor configuration."""
    path = os.path.expanduser(config_path)
    if not os.path.exists(path):
        logging.warning(f"Config not found at {path}, using defaults")
        return {
            'credentials_path': '~/.google/gmail-token.json',
            'noise_db_path': '~/.config/email-janitor/noise-senders.yaml',
            'safe_senders_path': '~/.config/email-janitor/safe-senders.yaml',
            'log_dir': '~/.config/email-janitor/logs',
            'log_format': 'jsonl',
            'apply_labels': True,
            'batch_size': 50,
            'rate_limit_rps': 5,
            'dry_run_default': False,
            'log_security_only': True,
        }
    return load_yaml(path)


# ─── Logging ─────────────────────────────────────────────────────────────────


def write_log_entry(log_dir: str, entry: dict, fmt: str = 'jsonl'):
    """Write a structured log entry."""
    log_dir = os.path.expanduser(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%S')
    log_file = os.path.join(log_dir, f'{timestamp}.jsonl')

    if fmt == 'jsonl':
        with open(log_file, 'w') as f:
            f.write(json.dumps(entry) + '\n')
    else:
        # text format
        with open(log_file.replace('.jsonl', '.log'), 'w') as f:
            f.write(f"=== Janitor Run: {timestamp} ===\n")
            f.write(json.dumps(entry, indent=2) + '\n')

    return log_file


# ─── Main Logic ─────────────────────────────────────────────────────────────


def run_janitor(config_path: str, dry_run: bool = False, credential_path: str | None = None):
    """Execute one Janitor pass."""
    start_time = time.time()
    config = load_config(config_path)

    creds_path = credential_path or config.get('credentials_path', '~/.google/gmail-token.json')
    noise_db_path = os.path.expanduser(config.get('noise_db_path', '~/.config/email-janitor/noise-senders.yaml'))
    safe_senders_path = os.path.expanduser(config.get('safe_senders_path', '~/.config/email-janitor/safe-senders.yaml'))
    log_dir = config.get('log_dir', '~/.config/email-janitor/logs')
    log_format = config.get('log_format', 'jsonl')
    apply_labels = config.get('apply_labels', True)
    batch_size = config.get('batch_size', 50)
    log_security_only = config.get('log_security_only', True)

    # Load noise database
    if os.path.exists(noise_db_path):
        noise_db = load_yaml(noise_db_path)
    else:
        logging.warning(f"Noise database not found at {noise_db_path}")
        noise_db = {}

    # Load safe senders
    safe_senders = []
    if os.path.exists(safe_senders_path):
        safe_data = load_yaml(safe_senders_path)
        safe_senders = safe_data.get('safe_senders', []) if isinstance(safe_data, dict) else []
    else:
        logging.warning(f"Safe-sender list not found at {safe_senders_path}")

    # Authenticate
    try:
        service = get_gmail_service(creds_path)
    except FileNotFoundError as e:
        logging.error(str(e))
        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'error',
            'error': str(e),
            'total_processed': 0,
            'archived': 0,
            'skipped_safe': 0,
            'security_logged': 0,
            'categories': {},
            'errors': [str(e)],
            'duration_seconds': 0,
        }

    # Fetch labels
    label_map = fetch_labels(service) if apply_labels else {}

    # Fetch inbox messages
    messages = fetch_inbox_messages(service, max_results=200)
    if not messages:
        result = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'ok',
            'total_processed': 0,
            'archived': 0,
            'skipped_safe': 0,
            'security_logged': 0,
            'categories': {},
            'errors': [],
            'duration_seconds': round(time.time() - start_time, 2),
        }
        # Write log and return
        if not dry_run:
            write_log_entry(log_dir, result, log_format)
        return result

    # Process each message
    to_archive = []
    security_alerts = []
    safe_skipped = []
    categories = {}
    errors = []

    for msg_ref in messages:
        details = get_message_details(service, msg_ref['id'])
        if not details:
            errors.append(f"Could not fetch {msg_ref['id']}")
            continue

        sender = details['from']
        subject = details['subject']

        # Check safe-sender allowlist
        if is_safe_sender(sender, safe_senders):
            safe_skipped.append(details)
            continue

        # Check security (log only, never archive)
        if noise_db and is_security_sender(sender, subject, noise_db):
            security_alerts.append(details)
            continue

        # Check noise categories
        category = None
        if noise_db and not is_security_sender(sender, subject, noise_db):
            category = categorize_sender(sender, subject, noise_db)

        if category:
            to_archive.append(details)
            categories[category] = categories.get(category, 0) + 1
        else:
            # Not matched — log but don't archive (Reviewer's job)
            pass

    # Archive matched noise
    archive_result = {'archived': 0, 'errors': []}
    archive_labels = None
    if to_archive and not dry_run:
        # Determine which label to apply (use first matched category)
        if apply_labels:
            archive_labels = []
            for details in to_archive:
                domain = extract_domain(details['from'])
                # Try category/domain label
                label_name = f"{list(categories.keys())[0]}/{domain}" if categories else None
                if label_name:
                    label_id = find_label_id(label_name, label_map)
                    if label_id:
                        archive_labels.append(label_id)

        msg_ids = [d['id'] for d in to_archive]
        archive_result = archive_messages(service, msg_ids, archive_labels, batch_size)

    # Build result
    result = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'status': 'ok' if not errors else 'warnings',
        'total_processed': len(messages),
        'archived': archive_result['archived'],
        'skipped_safe': len(safe_skipped),
        'security_logged': len(security_alerts),
        'categories': categories,
        'errors': errors + archive_result['errors'],
        'duration_seconds': round(time.time() - start_time, 2),
    }

    if dry_run:
        result['dry_run'] = True
        result['would_archive'] = len(to_archive)
        result['would_skip_safe'] = len(safe_skipped)
        result['would_log_security'] = len(security_alerts)
        result['would_not_match'] = len(messages) - len(to_archive) - len(safe_skipped) - len(security_alerts)

    # Write log
    if not dry_run:
        log_file = write_log_entry(log_dir, result, log_format)
        result['log_file'] = log_file

    return result


# ─── CLI ────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description='Email Janitor — Zero-LLM Gmail noise archiving CLI.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  %(prog)s                          # normal run\n'
            '  %(prog)s --dry-run                # preview without archiving\n'
            '  %(prog)s --config ~/my-config.yaml\n'
            '  %(prog)s --creds ~/token.json --dry-run\n'
        ),
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be archived without making changes',
    )
    parser.add_argument(
        '--config', '-c',
        default='~/.config/email-janitor/config.yaml',
        help='Path to config file (default: ~/.config/email-janitor/config.yaml)',
    )
    parser.add_argument(
        '--creds',
        default=None,
        help='Override Gmail credentials path from config',
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging',
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S',
    )

    try:
        result = run_janitor(
            config_path=args.config,
            dry_run=args.dry_run,
            credential_path=args.creds,
        )

        # Print summary
        status_icon = '✅' if result.get('status') == 'ok' else '⚠️'
        print(f"\n{status_icon} Janitor Run Complete")
        print(f"   Processed: {result.get('total_processed', 0)} inbox messages")
        print(f"   Archived:  {result.get('archived', 0)}")

        if result.get('dry_run'):
            print(f"   Would archive:  {result.get('would_archive', 0)}")
            print(f"   Would skip (safe): {result.get('would_skip_safe', 0)}")
            print(f"   Would log (security): {result.get('would_log_security', 0)}")
            print(f"   Would leave: {result.get('would_not_match', 0)}")
        else:
            print(f"   Skipped (safe): {result.get('skipped_safe', 0)}")
            print(f"   Security (logged): {result.get('security_logged', 0)}")

        if result.get('categories'):
            print(f"   Categories: {result['categories']}")
        if result.get('errors'):
            print(f"   Errors ({len(result['errors'])}):")
            for err in result['errors'][:5]:
                print(f"      {err}")
        print(f"   Duration: {result.get('duration_seconds', 0)}s")

    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        if logging.getLogger().level <= logging.DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
