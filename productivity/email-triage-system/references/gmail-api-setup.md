# Gmail API Setup

How to create a Google Cloud project, enable the Gmail API, and generate OAuth credentials for the Janitor CLI.

---

## Step 1: Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click the project dropdown at the top → **New Project**
3. Name it (e.g., `email-janitor`) and create it
4. Wait for the project to be created, then select it from the dropdown

## Step 2: Enable the Gmail API

1. In your project, go to **APIs & Services** → **Library**
2. Search for "Gmail API"
3. Click **Enable**

## Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** user type (unless you have Google Workspace)
3. Fill in:
   - **App name:** Email Janitor
   - **User support email:** your email
   - **Developer contact info:** your email
4. Click **Save and Continue**
5. **Scopes:** Click **Add or Remove Scopes**, search for `Gmail API`, and select:
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/gmail.labels`
   (modify allows reading, labeling, and archiving; labels allows reading existing labels)
6. Click **Save and Continue**
7. **Test users:** Add your email address (required for External publishing)
8. Click **Save and Continue**

## Step 4: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. **Application type:** Desktop application
4. **Name:** Email Janitor CLI
5. Click **Create**
6. Download the JSON file and save it as `~/.google/gmail-client-id.json`

## Step 5: Generate a Token

Use the Google API Python client to generate a refresh token:

```python
# save as ~/.google/get-token.py
import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels',
]

flow = InstalledAppFlow.from_client_secrets_file(
    os.path.expanduser('~/.google/gmail-client-id.json'), SCOPES)
creds = flow.run_local_server(port=0)

# Save the token
token_path = os.path.expanduser('~/.google/gmail-token.json')
with open(token_path, 'w') as f:
    f.write(creds.to_json())
print(f'Token saved to {token_path}')
```

Run it:

```bash
cd ~/.google && python get-token.py
```

Your browser will open for authorization. Grant access. The token is saved to `~/.google/gmail-token.json`.

## Step 6: Verify

Test the token works:

```bash
python -c "
import json, os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(
    os.path.expanduser('~/.google/gmail-token.json'))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

service = build('gmail', 'v1', credentials=creds)
result = service.users().labels().list(userId='me').execute()
print(f'Found {len(result[\"labels\"])} labels')
"
```

You should see "Found N labels" with your label count.

## Token Lifecycle

- The token auto-refreshes via the Google client library
- Refresh tokens expire if unused for 6 months
- If auth fails, run the token generation script again

## Troubleshooting

**"Access blocked: The app hasn't been verified":**
- Click **Continue** anyway (you're in testing mode)
- If the button is disabled, add your email as a test user in OAuth consent screen settings

**"Token has expired or been revoked":**
- Re-run the token generation script

**MFA/2FA not triggering:**
- Some Google accounts require app-specific passwords — use OAuth instead (the flow above handles this)
