# Session Log: 2024-12-18

## Summary

Gemini Deep Research integration for RQ_GEN/RQ_ASK pipeline. Extended session covering:
1. Initial RQ stage smoke test with gemini-2.5-pro
2. Deep dive into Gemini Deep Research agent access
3. Environment setup for Interactions API
4. Discovery of authentication/quota architecture

---

## Part 1: Gemini CLI Setup (Previous Session)

### Objective
Enable programmatic access to Gemini Deep Research for the RQ fan-out stage.

### Actions

1. **Installed Node.js and npm**
   - Node.js v22.12.0
   - npm 10.9.0

2. **Installed Gemini CLI**
   - Version: 0.21.2
   - Location: `~/.npm-global/bin/gemini`

3. **Installed google-genai Python SDK**
   - Version: 1.47.0 → Later upgraded to 1.56.0
   - Via: `pip3 install google-genai`

4. **Configured OAuth Authentication**
   - Account: `redsox12278@gmail.com` (Google Ultra subscription)
   - Credentials cached at `~/.gemini/`
   - Verified working: `gemini "What is 2+2?"` returns results

### Environment Files Updated

| File | Change |
|------|--------|
| `/Users/Benjamin/Dev/CAPY/.env` | Added `GEMINI_API_KEY` |
| `~/.gemini/settings.json` | OAuth config for Ultra account |
| `~/.gemini/google_accounts.json` | Account binding |

---

## Part 2: RQ_GEN Prompt Update

### Objective
Convert RQ_GEN from 3×3 (AlphaSense + GDR) routing to 6×GDR routing.

### Changes to `workshop/orchestration/RQ_Gen_2_2_2e.md`

1. **Section II.B: Platform Architecture** - Changed to 6×GDR
2. **Section III.P3: Query Design Heuristics** - Removed AlphaSense routing
3. **Section IV.A: Mandatory Coverage** - All GDR
4. **Section IV.C: Platform Allocation Summary** - 6 GDR with concurrency note
5. **Section V.B: Effective Query Patterns** - Rewrote for GDR web synthesis
6. **Section VI: Output Schema** - Platform field = "GDR" only
7. **Section VII: Execution Checklist** - Unified GDR routing

---

## Part 3: RQ_ASK Executor

### Created Files

| File | Purpose |
|------|---------|
| `workshop/kernels/RQ_ASK_KERNEL_2_2_2e.py` | Async Gemini query executor |
| `workshop/kernels/run_rq_ask.py` | CLI wrapper for RQ_ASK |
| `workshop/kernels/gemini_auth.py` | OAuth helper (for future Interactions API) |
| `workshop/validators/A8_VALIDATOR.md` | A.8 schema/semantic validator |
| `workshop/validators/A9_VALIDATOR.md` | A.9 completeness validator |

### RQ_ASK Features
- Async Python execution for 6 parallel Gemini queries
- Supports both CLI and SDK execution modes
- Configurable concurrency (default: 6)
- Dataclass output format for A.9_RESEARCH_RESULTS artifact
- Timeout handling (10 min per query)
- Error collection and reporting

---

## Part 4: RQ Stage Smoke Test Results

### Test Run: DAVE Analysis
- **Date:** 2024-12-18
- **Model:** gemini-2.5-pro (via CLI)
- **Results:** 6/6 queries completed

### A.9 Validation Results

| Metric | Value |
|--------|-------|
| Success Rate | 6/6 (100%) |
| Avg Response Length | ~3,100 chars |
| Total Execution Time | 178.7s |

### Quality Issues Identified
1. **RQ2:** Chain-of-thought artifacts leaked into response ("Hmm, the user is asking...")
2. **RQ4:** Response truncated mid-sentence
3. **RQ6:** Response truncated mid-sentence

### Validation Verdict
- **Result:** WARN
- **Recommendation:** REVIEW before proceeding to ENRICH

---

## Part 5: Deep Research Agent Investigation

### Objective
Use the **best** Gemini model - the Deep Research agent (`deep-research-pro-preview-12-2025`) powered by Gemini 3 Pro - instead of standard gemini-2.5-pro.

### Key Discovery: Two Separate Quota Systems

| System | Access Method | Quota Source |
|--------|---------------|--------------|
| **Gemini App** (gemini.google.com) | Web UI | Google AI Ultra subscription ($250/mo) |
| **Gemini API** (programmatic) | API key or OAuth | Free tier OR Google Cloud billing |

**Critical Finding:** Google AI Ultra subscription does NOT provide API quota. These are completely separate systems.

### Deep Research Agent Access Requirements

The `deep-research-pro-preview-12-2025` agent is **only** accessible via:
1. **Interactions API** (not `generate_content`)
2. **google-genai SDK v1.55.0+**
3. **Background execution** (`background=True` required)

### Authentication Attempts

| Method | Result | Issue |
|--------|--------|-------|
| API Key (free tier) | ❌ 429 | Quota exhausted |
| Gemini CLI OAuth token | ❌ 403 | Missing `generative-language.retriever` scope |
| Custom OAuth Desktop App | ❌ 403 | "App blocked" by Google security |
| gcloud ADC | ❌ 403 | "App blocked" by Google security |
| Vertex AI + OAuth | ❌ 403 | Billing required on GCP project |

### Root Cause
- Gemini CLI's OAuth client ID (`681255809395-...`) doesn't have `generative-language.retriever` scope registered
- Custom OAuth apps need to add user as "test user" in consent screen
- Even with test user added, the Interactions API requires either:
  - **Paid API key** (billing enabled in AI Studio), OR
  - **Vertex AI** (billing enabled on GCP project)

---

## Part 6: Environment Setup Completed

### New Python Environment

| Component | Value |
|-----------|-------|
| Python Version | 3.12.8 |
| Install Location | `/usr/local/bin/python3.12` |
| Virtual Environment | `~/.venvs/capy/` |
| google-genai | 1.56.0 |
| google-generativeai | 0.8.6 |
| google-auth-oauthlib | 1.2.2 |

### OAuth Credentials Created

| File | Purpose |
|------|---------|
| `~/.config/capy/client_secret.json` | OAuth Desktop App credentials |
| `~/.config/capy/token.json` | Cached OAuth token (expires) |

### GCP Project
- **Project ID:** `forward-script-481620-q5`
- **Vertex AI API:** Enabled
- **Billing:** NOT enabled (blocker for Vertex AI Deep Research)

---

## Part 7: What Works Now

### Working: Gemini CLI with gemini-2.5-pro
```bash
~/.npm-global/bin/gemini -m gemini-2.5-pro -p "Your query here"
```
- Uses Ultra subscription quota via OAuth
- Has Google Search grounding built-in
- Good quality but not Deep Research agent

### Working: RQ_ASK Pipeline
```bash
~/.venvs/capy/bin/python workshop/kernels/run_rq_ask.py \
    production/analyses/DAVE_CAPY_20251207_113714/04_RQ/DAVE_A8_RESEARCH_PLAN.json \
    production/analyses/DAVE_CAPY_20251207_113714/04_RQ \
    DAVE
```
- Executes 6 parallel queries via CLI
- Produces A.9_RESEARCH_RESULTS artifact
- Validated by A.9 validator

---

## Part 8: Roadmap for Deep Research Integration

### Option A: Enable AI Studio Billing (Recommended)
1. Go to https://aistudio.google.com
2. Dashboard → Usage and Billing → Set up Billing
3. Link to billing account
4. Update `GEMINI_API_KEY` in environment
5. Test Interactions API with `deep-research-pro-preview-12-2025`

**Pricing:** $2/M input tokens, $12/M output tokens (~$0.50-2 per 6-query run)

### Option B: Enable Vertex AI Billing
1. Go to https://console.cloud.google.com/billing/enable?project=forward-script-481620-q5
2. Link billing account to project
3. Use OAuth credentials with Vertex AI client
4. Test Interactions API

**Same pricing, different billing path**

### Option C: Continue with gemini-2.5-pro (Current State)
- Works now with no additional setup
- Lower quality than Deep Research agent
- Some response quality issues (truncation, CoT leakage)

---

## Files Modified This Session

### Workshop - New Files
- `kernels/gemini_auth.py` - OAuth helper for Interactions API
- `validators/A8_VALIDATOR.md` - A.8 schema validator
- `validators/A9_VALIDATOR.md` - A.9 completeness validator

### Workshop - Updated Files
- `kernels/RQ_ASK_KERNEL_2_2_2e.py` - Model updated to gemini-2.5-pro
- `patches/SESSION_LOG_20241218.md` - This file

### Production - New Files
- `analyses/DAVE_CAPY_20251207_113714/04_RQ/DAVE_A8_RESEARCH_PLAN.json`
- `analyses/DAVE_CAPY_20251207_113714/04_RQ/A9_RESEARCH_RESULTS_DAVE_20251218_152213.json`

### User Environment
- `~/.venvs/capy/` - New Python 3.12 venv with google-genai 1.56.0
- `~/.config/capy/client_secret.json` - OAuth Desktop App credentials
- `~/.config/capy/token.json` - Cached OAuth token
- `/usr/local/bin/python3.12` - Python 3.12.8 installation

---

## Technical Reference

### Gemini Model Hierarchy (Dec 2025)

| Model | Access | Use Case |
|-------|--------|----------|
| `deep-research-pro-preview-12-2025` | Interactions API only | Best for complex research |
| `gemini-2.5-pro` | generate_content / CLI | General purpose, web grounding |
| `gemini-2.5-flash` | generate_content / CLI | Fast, cheaper |

### API Endpoints

| Endpoint | Authentication |
|----------|---------------|
| `generativelanguage.googleapis.com/v1alpha/interactions` | API key or OAuth |
| `aiplatform.googleapis.com` (Vertex AI) | OAuth + GCP billing |

### OAuth Scopes

| Scope | Purpose |
|-------|---------|
| `cloud-platform` | General GCP access |
| `generative-language.retriever` | Required for Interactions API |
| `userinfo.email` | User identification |

### Key URLs

| Resource | URL |
|----------|-----|
| AI Studio API Keys | https://aistudio.google.com/apikey |
| AI Studio Billing | https://aistudio.google.com (Dashboard → Billing) |
| GCP Billing | https://console.cloud.google.com/billing |
| Vertex AI API | https://console.cloud.google.com/apis/api/aiplatform.googleapis.com |
| Deep Research Docs | https://ai.google.dev/gemini-api/docs/deep-research |
| Interactions API Docs | https://ai.google.dev/gemini-api/docs/interactions |

---

## Lessons Learned

1. **Google AI subscriptions (Pro/Ultra) are for consumer app only** - They don't provide API quota
2. **Gemini CLI OAuth is scope-limited** - Can't add `generative-language.retriever` scope
3. **Deep Research requires Interactions API** - Cannot use `generate_content`
4. **Free API tier is very limited** - Exhausts quickly, especially for research queries
5. **Python 3.10+ required** - For google-genai 1.55.0+ which has Interactions API

---

## Next Session Priorities

1. **Decision:** Enable billing (AI Studio or Vertex AI) to access Deep Research agent
2. **If billing enabled:** Update RQ_ASK_KERNEL to use Interactions API
3. **If not:** Tune gemini-2.5-pro prompts to reduce truncation/CoT leakage
4. **Either way:** Complete DAVE analysis through ENRICH stage
