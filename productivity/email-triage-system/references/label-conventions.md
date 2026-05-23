# Label Conventions

The Janitor uses your existing Gmail labels for two purposes:
1. **Noise matching** — labels that already exist tell the Janitor what a given sender typically is
2. **Label application** — before archiving, the Janitor applies the appropriate category label

---

## Label Hierarchy (Recommended)

### By Category
| Category | Label Pattern | Purpose |
|----------|--------------|---------|
| Services | `Services/{domain}` | Transactional/account emails |
| Orders | `Orders/{domain}` | Purchase receipts, invoices |
| Promotions | `promotions/{domain}` | Marketing, promos, deals |
| Newsletters | `newsletter/{domain}` | Regular newsletter subscriptions |
| Security | `Security/{domain}` | Security alerts, password resets |
| Family | `Family/{domain}` | School, kids, family correspondence |
| Finance | `Finance/{domain}` | Financial statements, subscriptions |
| Domain | `domain/{domain}` | Catch-all domain label |

### By Type (Cross-Cutting)
| Label | Purpose |
|-------|---------|
| `type/financial` | Invoices, receipts, billing |
| `type/work` | Work-related emails |
| `type/personal` | Personal correspondence |
| `type/security` | Security alerts |
| `type/promo` | Marketing/promotional |
| `type/social` | Social notifications |

### Special Labels
| Label | Purpose |
|-------|---------|
| `receipts` | Generic receipts |
| `Follow up` | Needs attention |

---

## How Janitor Matches Labels

1. Extract the sender domain from the `from` field
2. Search existing Gmail labels for that domain
3. Match priority order: Services > Orders > Family > Security > Finance > promotions > newsletter > domain
4. Apply matching label + type label before archiving
5. If no label exists for the domain, archive without a custom label

---

## Label Auto-Detection

Labels are read dynamically from Gmail at startup — never hardcoded. This handles:

- Label renames (you rename `Services/example.com` to `Support/example.com`)
- New labels added for new senders
- Label hierarchy changes

The Janitor uses `service.users().labels().list(userId='me')` to fetch all labels and matches against them at runtime.

---

## When No Label Exists

If a sender has no existing label:
1. The Janitor still archives the email (removes from INBOX)
2. No custom label is applied
3. The sender/reason is logged in the JSONL output
4. You can add a label later, and the Janitor will start using it

---

## Creating Labels

You can create new labels in Gmail:
1. Go to Gmail → Settings → Labels → Create new label
2. Use the hierarchy convention: `Category/domain.com`
3. Labels are available to the Janitor immediately (no restart needed)

Or via API:
```bash
python -c "
from googleapiclient.discovery import build
# ... (auth code) ...
service.users().labels().create(userId='me', body={
    'name': 'Services/example.com',
    'labelListVisibility': 'labelShow',
    'messageListVisibility': 'show'
}).execute()
"
```
