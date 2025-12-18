# CAPY Local Environment Setup

> **Last updated:** 2024-12-18
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
GEMINI_API_KEY=AIzaSyAZIIDk4VGYIqtvV4vp77j9yj4UJd36kp4
```

**Note:** The API key is a fallback. Primary authentication uses OAuth (see below).

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

**Linked Account:** `redsox12278@gmail.com`

### Usage

```bash
# Basic query
~/.npm-global/bin/gemini "Your question here"

# With specific model
~/.npm-global/bin/gemini -m gemini-2.0-flash-exp "Your question"

# Pipe input
echo "What is 2+2?" | ~/.npm-global/bin/gemini
```

### Troubleshooting

If you get quota errors:
1. Check OAuth is still valid: `cat ~/.gemini/google_accounts.json`
2. Re-authenticate by running `~/.npm-global/bin/gemini` interactively in Terminal
3. Sign in with the Ultra account when browser opens

---

## Python Dependencies

### google-genai SDK

```bash
pip3 show google-genai
# Version: 1.47.0
```

### Usage in Python

```python
from google import genai

# Using API key (limited quota)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# List available models
for model in client.models.list():
    print(model.name)
```

**Note:** The SDK API key has limited free tier quota. For production use, the CLI with OAuth is preferred.

---

## Directory Structure

```
~/Dev/CAPY/                    # Main repo (CAPY_ROOT)
├── .env                       # Environment variables
├── workshop/                  # Development environment
├── production/                # Live analysis runs
└── archive/                   # Historical versions

~/.gemini/                     # Gemini CLI config
├── settings.json              # Auth configuration
├── google_accounts.json       # OAuth account binding
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

# Test Gemini connection
~/.npm-global/bin/gemini "What is 2+2?"  # Should return "4"

# Check Python SDK
pip3 show google-genai  # Should show 1.47.0

# Check environment variables
source ~/Dev/CAPY/.env && echo $GEMINI_API_KEY  # Should show key
```

---

## Re-setup Instructions

If setting up on a new machine or after reset:

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
npm install -g @anthropic-ai/gemini-cli
# Or: npm install -g @anthropic-ai/gemini-cli --prefix ~/.npm-global
```

### 4. Authenticate
```bash
~/.npm-global/bin/gemini
# Follow browser prompts to sign in with Google Ultra account
```

### 5. Install Python SDK
```bash
pip3 install google-genai
```

### 6. Copy .env file
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
| Dev worktree | `~/.claude-worktrees/CAPY/intelligent-tharp` |

### Usage

```bash
# Push works automatically (credential stored)
git push origin branch-name

# If credential expires, regenerate PAT at:
# https://github.com/settings/tokens/new?description=CAPY-Claude-Code&scopes=repo
```

---

## Session Notes

### 2024-12-18
- Initial Gemini CLI setup
- OAuth configured with Ultra account
- Verified working with test queries
- Created RQ_ASK executor script
- GitHub PAT configured for automated push
