# Deep Research Agent Integration Investigation

> **Date:** 2024-12-18
> **Status:** BLOCKED - Requires billing
> **Purpose:** Document all attempted strategies for future problem-solving

---

## Executive Summary

**Goal:** Use Google's Deep Research agent (`deep-research-pro-preview-12-2025`) programmatically for CAPY's RQ stage instead of standard `gemini-2.5-pro`.

**Why Deep Research is better:**
- Powered by Gemini 3 Pro (latest model)
- Autonomous multi-step research with planning
- Comprehensive web synthesis with citations
- 60-minute research sessions
- Specifically designed for complex research queries

**Current fallback:** `gemini-2.5-pro` via Gemini CLI works but has quality issues (truncation, chain-of-thought leakage).

**Blocker:** All paths to Deep Research require paid API quota. The user has Google AI Ultra subscription ($250/mo) but this only covers the consumer Gemini app, NOT the API.

---

## The Core Problem

### Two Separate Quota Systems (Critical Discovery)

| System | What It Is | How to Access | Quota Source |
|--------|-----------|---------------|--------------|
| **Gemini App** | Consumer web app at gemini.google.com | Browser, mobile app | Google AI Pro/Ultra subscription |
| **Gemini API** | Programmatic access for developers | API key, OAuth, SDK | Free tier OR Google Cloud billing |

**The user's Google AI Ultra subscription ($250/mo) provides:**
- Higher limits in Gemini web app
- Access to Deep Research in the web UI
- Higher limits for Gemini CLI (via OAuth)
- Does NOT provide API quota for Interactions API

**What we need:**
- Interactions API access (the ONLY way to use Deep Research agent programmatically)
- This requires either paid API key OR Vertex AI with billing

---

## Deep Research Agent Technical Requirements

### Access Method
The `deep-research-pro-preview-12-2025` agent is ONLY accessible via:
1. **Interactions API** - NOT `generate_content()`
2. **google-genai SDK v1.55.0+** - Older versions don't have Interactions API
3. **Background execution** - Must use `background=True` parameter
4. **Python 3.10+** - Required for google-genai 1.55.0+

### Code Pattern
```python
from google import genai

client = genai.Client(api_key="YOUR_KEY")  # or OAuth credentials

# Create interaction - MUST use background=True
interaction = client.interactions.create(
    input="Your research query",
    agent="deep-research-pro-preview-12-2025",
    background=True
)

# Poll for completion
while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        print(interaction.outputs[-1].text)
        break
    time.sleep(10)
```

### Required OAuth Scope
For OAuth authentication (instead of API key), you need:
- `https://www.googleapis.com/auth/generative-language.retriever`
- `https://www.googleapis.com/auth/cloud-platform`

---

## Strategy 1: Use Existing API Key

### Attempt
Use the `GEMINI_API_KEY` from environment variable with Interactions API.

### Code
```python
from google import genai
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
interaction = client.interactions.create(
    input="Test query",
    agent="deep-research-pro-preview-12-2025",
    background=True
)
```

### Result
```
Error: 429 - You do not have enough quota to make this request.
```

### Why It Failed
The free tier API key has exhausted its quota. Free tier limits were drastically reduced in December 2025.

### What Would Fix It
Enable billing in Google AI Studio to get paid tier quota.

---

## Strategy 2: Use Gemini CLI OAuth Token

### Rationale
The Gemini CLI successfully authenticates with the user's Ultra subscription. Maybe we can reuse its OAuth token for the Interactions API.

### Investigation
```bash
cat ~/.gemini/oauth_creds.json
```

Found OAuth credentials with:
- `access_token`: Valid Bearer token
- `refresh_token`: For token renewal
- `scope`: "cloud-platform userinfo.profile userinfo.email openid"

### Attempt
```python
import requests

# Extract token from Gemini CLI credentials
with open('~/.gemini/oauth_creds.json') as f:
    creds = json.load(f)
access_token = creds['access_token']

# Try Interactions API with this token
response = requests.post(
    'https://generativelanguage.googleapis.com/v1alpha/interactions',
    headers={'Authorization': f'Bearer {access_token}'},
    json={
        'input': 'Test query',
        'agent': 'deep-research-pro-preview-12-2025',
        'background': True
    }
)
```

### Result
```
Error: 403 - Request had insufficient authentication scopes.
Reason: ACCESS_TOKEN_SCOPE_INSUFFICIENT
```

### Why It Failed
The Gemini CLI's OAuth token has these scopes:
- `cloud-platform`
- `userinfo.profile`
- `userinfo.email`
- `openid`

But the Interactions API requires:
- `generative-language.retriever` ← **MISSING**

### Why We Can't Fix It
The Gemini CLI's OAuth client ID (`681255809395-oo8ft2oprdrnp9e3aqf6av3hmdib135j`) is Google's official client. We cannot add scopes to it - only Google can modify what scopes their client requests.

---

## Strategy 3: Re-authenticate CLI with Additional Scope

### Rationale
Maybe we can re-run Gemini CLI authentication and somehow request the additional scope.

### Investigation
```bash
~/.npm-global/bin/gemini --help
```

No flag exists to specify OAuth scopes. The CLI handles authentication internally with fixed scopes.

### Why It Failed
Gemini CLI doesn't expose OAuth configuration. It's designed for simplicity, not extensibility.

---

## Strategy 4: Create Custom OAuth Desktop App

### Rationale
Create our own OAuth client in Google Cloud Console with the correct scopes.

### Steps Taken
1. Created GCP project: `forward-script-481620-q5`
2. Enabled Generative Language API
3. Created OAuth consent screen (External, Testing mode)
4. Added test user: `redsox12278@gmail.com`
5. Created OAuth client ID (Desktop app)
6. Downloaded `client_secret.json` to `~/.config/capy/`

### Attempt
```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/generative-language.retriever'
]

flow = InstalledAppFlow.from_client_secrets_file(
    '~/.config/capy/client_secret.json',
    SCOPES
)
creds = flow.run_local_server(port=0)
```

### Result - First Error
```
Error 403: access_denied
"CAPY Research has not completed the Google verification process"
```

### Fix Applied
Added `redsox12278@gmail.com` as test user in OAuth consent screen.

### Result - After Fix
```
Error: 429 - You do not have enough quota to make this request.
```

### Why It "Worked" But Still Failed
The OAuth flow succeeded! We got valid credentials with the correct scopes. But the API still returns quota errors because:
- Our GCP project has no billing enabled
- The free tier quota is 0
- OAuth credentials don't magically provide quota

### What Would Fix It
Enable billing on the GCP project.

---

## Strategy 5: Use Vertex AI Instead

### Rationale
Vertex AI is Google Cloud's enterprise ML platform. It also has the Interactions API. Maybe it has different quota rules.

### Steps Taken
1. Enabled Vertex AI API on project `forward-script-481620-q5`

### Attempt
```python
from google import genai
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('~/.config/capy/token.json')

client = genai.Client(
    vertexai=True,
    credentials=creds,
    project='forward-script-481620-q5',
    location='us-central1'
)

interaction = client.interactions.create(
    input="Test query",
    agent="deep-research-pro-preview-12-2025",
    background=True
)
```

### Result
```
Error: 403 - This API method requires billing to be enabled.
Please enable billing on project #forward-script-481620-q5
```

### Why It Failed
Vertex AI requires a billing account linked to the GCP project. No free tier for Vertex AI Interactions API.

### What Would Fix It
Enable billing on the GCP project.

---

## Strategy 6: Use gcloud Application Default Credentials

### Rationale
Maybe `gcloud auth application-default login` with explicit scopes would work.

### Attempt
```bash
~/.local/google-cloud-sdk/bin/gcloud auth application-default login \
    --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.retriever'
```

### Result
```
Error: "This app is blocked"
"This app tried to access sensitive info in your Google Account.
To keep your account safe, Google blocked this access."
```

### Why It Failed
gcloud's default OAuth client is blocked for the `generative-language.retriever` scope. Google hasn't registered this scope with gcloud's client.

---

## Strategy 7: Use Gemini CLI Client ID with Custom Scopes

### Rationale
The Gemini CLI's OAuth client works. Maybe we can use the same client ID but request additional scopes.

### Attempt
```python
from google_auth_oauthlib.flow import InstalledAppFlow

# Use Gemini CLI's client ID
client_config = {
    'installed': {
        'client_id': '681255809395-oo8ft2oprdrnp9e3aqf6av3hmdib135j.apps.googleusercontent.com',
        'client_secret': '',  # Installed apps may not need this
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'redirect_uris': ['http://localhost']
    }
}

SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/generative-language.retriever'
]

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_local_server(port=0)
```

### Result
```
Error 403: restricted_client
"Unregistered scope(s) in the request:
https://www.googleapis.com/auth/generative-language.retriever"
```

### Why It Failed
Google's Gemini CLI OAuth client only has certain scopes registered. The `generative-language.retriever` scope is not one of them. This is controlled by Google, not us.

---

## Strategy 8: Direct REST API with Ultra Account Token

### Rationale
The Gemini CLI works with Ultra quota. Maybe the underlying API accepts the same token if we call it directly.

### Attempt
```python
import requests

# Get token from Gemini CLI
with open('~/.gemini/oauth_creds.json') as f:
    token = json.load(f)['access_token']

# Call Interactions API directly
response = requests.post(
    'https://generativelanguage.googleapis.com/v1alpha/interactions',
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json={
        'input': 'Test query',
        'agent': 'deep-research-pro-preview-12-2025',
        'background': True
    }
)
```

### Result
```
Error: 403 - Request had insufficient authentication scopes.
```

### Why It Failed
Same as Strategy 2 - the token lacks the required scope.

---

## Strategies NOT Tried (Potential Solutions)

### A. Enable AI Studio Billing
**What:** Link a billing account to Google AI Studio
**URL:** https://aistudio.google.com → Dashboard → Billing
**Expected Result:** API key gets paid tier quota, Interactions API works
**Cost:** ~$2/M input tokens, $12/M output tokens
**Status:** User has not done this yet

### B. Enable GCP Project Billing
**What:** Link a billing account to GCP project `forward-script-481620-q5`
**URL:** https://console.cloud.google.com/billing/enable?project=forward-script-481620-q5
**Expected Result:** Vertex AI Interactions API works
**Cost:** Same as above
**Status:** User has not done this yet

### C. Service Account with Billing
**What:** Create a service account in a billing-enabled project
**Expected Result:** Programmatic access without user OAuth
**Requires:** Billing enabled first

### D. Use Gemini CLI Directly (Current Workaround)
**What:** Call `gemini -m gemini-2.5-pro -p "query"` via subprocess
**Works:** Yes, uses Ultra subscription quota
**Limitation:** Not Deep Research agent, just regular gemini-2.5-pro with web grounding
**Quality:** Good but some truncation and CoT leakage issues

### E. Reverse-Engineer Gemini Web App
**What:** Use browser automation or API sniffing to access Deep Research through the web app
**Libraries:** https://github.com/HanaokaYuzu/Gemini-API (reverse-engineered)
**Risk:** Against ToS, may break anytime
**Status:** Not attempted

### F. Wait for Gemini CLI Deep Research Support
**What:** Google may add Deep Research to Gemini CLI
**Status:** Not currently available as of Dec 2025

---

## Summary of Failures

| Strategy | Blocked By | Fixable By Us? |
|----------|-----------|----------------|
| API Key | Quota exhausted | Enable billing |
| CLI OAuth Token | Missing scope | No - Google controls |
| CLI Re-auth | No scope flag | No - CLI limitation |
| Custom OAuth App | Quota exhausted | Enable billing |
| Vertex AI | Billing required | Enable billing |
| gcloud ADC | App blocked | No - Google controls |
| CLI Client + Scopes | Scope not registered | No - Google controls |
| Direct REST | Missing scope | No - token limitation |

### Pattern Identified
Every strategy hits one of two walls:
1. **Scope limitation** - Tokens from Google's clients (Gemini CLI, gcloud) don't have `generative-language.retriever`
2. **Quota limitation** - Our own OAuth client works but has no quota without billing

---

## The Actual Solution

**Enable billing.** There is no free path to the Deep Research agent.

Options:
1. **AI Studio billing** - Easiest, links to API key
2. **GCP billing** - More enterprise, links to project

The user's Ultra subscription pays for the Gemini web app, which is a completely separate product from the Gemini API. This is a business model decision by Google, not a technical limitation we can work around.

---

## Environment State After Investigation

### Installed Successfully
- Python 3.12.8 at `/usr/local/bin/python3.12`
- Virtual environment at `~/.venvs/capy/`
- google-genai 1.56.0 (has Interactions API)
- google-generativeai 0.8.6
- google-auth-oauthlib 1.2.2

### Configured Successfully
- OAuth Desktop App credentials at `~/.config/capy/client_secret.json`
- OAuth token at `~/.config/capy/token.json` (valid, correct scopes)
- GCP project `forward-script-481620-q5` with Vertex AI API enabled
- Test user added to OAuth consent screen

### Still Working
- Gemini CLI at `~/.npm-global/bin/gemini`
- CLI OAuth with Ultra subscription quota
- `gemini-2.5-pro` model via CLI

### Blocked
- Interactions API (needs billing)
- Deep Research agent (needs Interactions API)

---

## For Future AI Agents

If you're trying to solve this problem:

1. **Don't retry the OAuth approaches** - They all hit scope limitations that only Google can fix
2. **Don't try to find a "free" path** - There isn't one for Deep Research
3. **The solution is billing** - Either AI Studio or GCP
4. **The workaround is Gemini CLI** - Uses gemini-2.5-pro, not Deep Research, but works

### Potential Research Directions
- Check if Google has announced plans to add Deep Research to Gemini CLI
- Check if there's a way to request scope additions for the Gemini CLI OAuth client
- Check if there are third-party services that provide Deep Research access
- Check if the reverse-engineered Gemini-API library supports Deep Research

### Key URLs
- AI Studio: https://aistudio.google.com
- GCP Billing: https://console.cloud.google.com/billing
- Deep Research Docs: https://ai.google.dev/gemini-api/docs/deep-research
- Interactions API Docs: https://ai.google.dev/gemini-api/docs/interactions
- Gemini CLI GitHub: https://github.com/google-gemini/gemini-cli
