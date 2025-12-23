# CAPY Local Environment Setup

> **Last updated:** 2024-12-23
> **Machine:** Benjamin's Mac

This document captures the local environment configuration for CAPY development.

---

## Environment Variables

Location: `/Users/Benjamin/Dev/CAPY/.env`

```bash
MACHINE_NAME=Mac
USER_NAME=Benjamin
OS_TYPE=mac
CAPY_ROOT=~/Dev/CAPY
SOURCE_DOCS_PATH=~/Dropbox/CAPY-Sources
GEMINI_API_KEY=<your_api_key>
POPPLER_PATH=/opt/homebrew/bin
```

**Note:** The `.env` file is gitignored (contains secrets). Copy `.env.example` to `.env` and fill in your values.

**Note:** The API key has exhausted free tier quota. See "Deep Research Setup" for paid tier options.

---

## Python Environments

### System Python (Default)
- **Version:** 3.9.6
- **Location:** `/usr/bin/python3`
- **Use for:** Basic scripts, non-ML tasks

### Python 3.12 (CAPY venv)
- **Version:** 3.12.8
- **Location:** `/usr/local/bin/python3.12`
- **Use for:** RQ_ASK, Interactions API, google-genai SDK

### CAPY Virtual Environment
```bash
# Location
~/.venvs/capy/

# Activation
source ~/.venvs/capy/bin/activate

# Or run directly
~/.venvs/capy/bin/python your_script.py
```

**Installed packages:**
| Package | Version | Purpose |
|---------|---------|---------|
| google-genai | 1.56.0 | Gemini API (Interactions API) |
| google-generativeai | 0.8.6 | Legacy Gemini API |
| google-auth-oauthlib | 1.2.2 | OAuth authentication |
| google-auth-httplib2 | 0.3.0 | HTTP auth transport |

---

## Gemini CLI

### Installation

| Component | Version | Location |
|-----------|---------|----------|
| Node.js | v22.12.0 | System |
| npm | 10.9.0 | System |
| Gemini CLI | 0.21.2 | `~/.npm-global/bin/gemini` |

### Authentication

**Method:** OAuth with Google Ultra subscription

| File | Purpose |
|------|---------|
| `~/.gemini/settings.json` | Auth config (OAuth selected) |
| `~/.gemini/google_accounts.json` | Account binding |
| `~/.gemini/oauth_creds.json` | OAuth tokens (access + refresh) |

**Linked Account:** `redsox12278@gmail.com`

**OAuth Scopes (CLI):**
- `cloud-platform`
- `userinfo.profile`
- `userinfo.email`
- `openid`

**Note:** CLI OAuth does NOT include `generative-language.retriever` scope required for Interactions API.

### Usage

```bash
# Basic query
~/.npm-global/bin/gemini "Your question here"

# With specific model
~/.npm-global/bin/gemini -m gemini-2.5-pro "Your question"

# Non-interactive with output
~/.npm-global/bin/gemini -p "What is 2+2?"

# JSON output for scripting
~/.npm-global/bin/gemini -p "Your query" --output-format json
```

### Troubleshooting

If you get quota errors:
1. Check OAuth is still valid: `cat ~/.gemini/google_accounts.json`
2. Re-authenticate by running `~/.npm-global/bin/gemini` interactively in Terminal
3. Sign in with the Ultra account when browser opens

---

## OAuth Credentials (Custom App)

For Interactions API / Deep Research, we created custom OAuth credentials:

| File | Purpose |
|------|---------|
| `~/.config/capy/client_secret.json` | OAuth Desktop App credentials |
| `~/.config/capy/token.json` | Cached OAuth token |

**GCP Project:** `forward-script-481620-q5`

**OAuth Scopes (Custom):**
- `cloud-platform`
- `generative-language.retriever`
- `userinfo.email`

### Status
- OAuth consent screen configured
- Test user added: `redsox12278@gmail.com`
- Token obtained and cached
- **Blocker:** Requires billing enabled for API quota

---

## Deep Research Setup

### Current State: gemini-2.5-pro via CLI
- Works with Ultra subscription quota
- Has Google Search grounding
- Some quality issues (truncation, CoT leakage)

### To Enable Deep Research Agent

The `deep-research-pro-preview-12-2025` agent requires **paid API quota**.

**Option A: AI Studio Billing (Recommended)**
1. Go to https://aistudio.google.com
2. Dashboard → Usage and Billing → Set up Billing
3. Link billing account
4. Test with API key

**Option B: Vertex AI Billing**
1. Go to https://console.cloud.google.com/billing/enable?project=forward-script-481620-q5
2. Link billing account
3. Use OAuth + Vertex AI client

**Pricing:** $2/M input tokens, $12/M output tokens

---

## Directory Structure

```
~/Dev/CAPY/                    # Main repo (CAPY_ROOT)
├── .env                       # Environment variables
├── workshop/                  # Development environment
├── production/                # Live analysis runs
└── archive/                   # Historical versions

~/.venvs/capy/                 # Python 3.12 virtual environment
└── bin/
    └── python                 # Python 3.12.8

~/.config/capy/                # CAPY OAuth config
├── client_secret.json         # OAuth Desktop App credentials
└── token.json                 # Cached OAuth token

~/.gemini/                     # Gemini CLI config
├── settings.json              # Auth configuration
├── google_accounts.json       # OAuth account binding
├── oauth_creds.json           # OAuth tokens
├── installation_id            # CLI installation ID
└── tmp/                       # Temporary files

~/.npm-global/                 # Global npm packages
└── bin/
    └── gemini                 # Gemini CLI executable

~/Dropbox/CAPY-Sources/        # Source documents (PDFs)
```

---

## Verification Commands

Run these to verify environment is working:

```bash
# Check Node.js
node --version  # Should show v22.x

# Check Gemini CLI
~/.npm-global/bin/gemini --version  # Should show 0.21.2

# Test Gemini connection (uses Ultra quota)
~/.npm-global/bin/gemini -m gemini-2.5-pro "What is 2+2?"

# Check Python 3.12
/usr/local/bin/python3.12 --version  # Should show 3.12.8

# Check CAPY venv
~/.venvs/capy/bin/pip list | grep google  # Should show google-genai 1.56.0

# Check environment variables
source ~/Dev/CAPY/.env && echo $GEMINI_API_KEY

# Test RQ_ASK
~/.venvs/capy/bin/python workshop/kernels/run_rq_ask.py --help
```

---

## Re-setup Instructions

If setting up on a new machine or after reset:

### 0. PDF Preprocessing Dependencies

**Step 1: Install Homebrew** (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Follow the prompts, then add to PATH:
```bash
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Step 2: Install Poppler** (PDF CLI tools)
```bash
brew install poppler
```

**Step 3: Install Python packages**
```bash
pip3 install pdfplumber pdf2image pillow
```

**Step 4: Verify installation**
```bash
/opt/homebrew/bin/pdftotext -v    # Should show poppler version
python3 -c "import pdfplumber; print(pdfplumber.__version__)"
python3 -c "from pdf2image import convert_from_path; print('pdf2image OK')"
```

**Verified versions (2024-12-23):**

| Package | Version | Type | Purpose |
|---------|---------|------|---------|
| poppler | 25.12.0 | brew | CLI tools (pdftotext, pdftoppm) |
| pdfplumber | 0.11.8 | pip3 | Text-based PDF extraction (10-Ks, transcripts) |
| pdf2image | 1.17.0 | pip3 | PDF to image conversion (earnings decks) |
| pillow | 12.0.0 | pip3 | Image processing |

**Note:** `pdfplumber` handles text-based PDFs (10-Ks, transcripts). `pdf2image` handles visual PDFs (earnings decks, presentations) by converting to images.

### 1. Install Node.js
```bash
# Download from https://nodejs.org/ or use brew
brew install node
```

### 2. Configure npm global directory
```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
# Add to shell profile: export PATH=~/.npm-global/bin:$PATH
```

### 3. Install Gemini CLI
```bash
npm install -g @google/gemini-cli
```

### 4. Authenticate Gemini CLI
```bash
~/.npm-global/bin/gemini
# Follow browser prompts to sign in with Google Ultra account
```

### 5. Install Python 3.12
```bash
# Download from https://www.python.org/downloads/
# Or use the pkg at ~/Downloads/python-3.12.8.pkg
```

### 6. Create CAPY venv
```bash
mkdir -p ~/.venvs
/usr/local/bin/python3.12 -m venv ~/.venvs/capy
~/.venvs/capy/bin/pip install google-genai google-generativeai google-auth-oauthlib
```

### 7. Set up OAuth (optional, for Deep Research)
```bash
mkdir -p ~/.config/capy
# Create OAuth Desktop App at https://console.cloud.google.com/apis/credentials
# Download client_secret.json to ~/.config/capy/
# Run gemini_auth.py to get token
```

### 8. Copy .env file
Ensure `/Users/Benjamin/Dev/CAPY/.env` exists with required variables.

---

## Git / GitHub

### Authentication

**Method:** Personal Access Token (PAT) via credential store

| File | Purpose |
|------|---------|
| `~/.git-credentials` | Stored PAT (permissions 600) |

**Credential helper:** `git config --global credential.helper store`

### Repository

| Item | Value |
|------|-------|
| Remote | `https://github.com/Sauce123-CB/CAPY.git` |
| Main branch | `master` |
| Dev worktree | `~/.claude-worktrees/CAPY/exciting-haibt` |

### Usage

```bash
# Push works automatically (credential stored)
git push origin branch-name

# If credential expires, regenerate PAT at:
# https://github.com/settings/tokens/new?description=CAPY-Claude-Code&scopes=repo
```

---

## Session Notes

### 2024-12-18 (Extended Session)
- Initial Gemini CLI setup with OAuth
- RQ stage smoke test completed (6/6 queries succeeded)
- Deep Research agent investigation
- Discovered: Ultra subscription ≠ API quota (separate systems)
- Installed Python 3.12.8, created ~/.venvs/capy
- Installed google-genai 1.56.0 for Interactions API
- Created custom OAuth Desktop App credentials
- **Blocker:** Need billing for Deep Research agent access
- Documented roadmap for future sessions

### 2024-12-23 (New Machine Setup)
- Installed Homebrew on new Mac
- Installed Poppler 25.12.0 via brew
- Installed pdfplumber 0.11.8, pdf2image 1.17.0, pillow 12.0.0 via pip3
- Added POPPLER_PATH to .env
- Added .env to .gitignore (was exposing API key)
- Created .env.example template for new users
- Updated PDF setup documentation with step-by-step instructions
