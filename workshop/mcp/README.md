# Gemini MCP Server

MCP server that provides Claude Code with access to Gemini APIs.

## Tools Provided

| Tool | Purpose | Use Case |
|------|---------|----------|
| `gemini_deep_research` | Long-running web research | RQ_ASK single query |
| `gemini_batch_deep_research` | Parallel research (up to 6) | RQ_ASK full execution |
| `gemini_generate` | Standard text generation | Silicon Council, general |
| `gemini_generate_with_thinking` | Extended reasoning | Complex analysis |
| `gemini_list_models` | List available models | Discovery |

## Setup

### 1. Install Dependencies

```bash
pip install fastmcp google-genai
```

### 2. Get Your API Key

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 3. Configure Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "python",
      "args": ["C:/path/to/CAPY/workshop/mcp/gemini_mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Windows path example:**
```json
"args": ["C:\\Users\\YourName\\CAPY\\workshop\\mcp\\gemini_mcp_server.py"]
```

### 4. Restart Claude Code

After updating settings, restart Claude Code for the MCP server to load.

## Usage Examples

Once configured, Claude Code can call these tools directly:

```
# Deep research for RQ_ASK
mcp__gemini__gemini_deep_research(query="Research the history of CFPB enforcement actions against fintech lenders 2020-2025")

# Batch research (all 6 RQs at once)
mcp__gemini__gemini_batch_deep_research(queries=["RQ1...", "RQ2...", ...])

# Silicon Council generation with thinking
mcp__gemini__gemini_generate_with_thinking(
    prompt="Analyze this valuation model...",
    thinking_level="high"
)
```

## Troubleshooting

### "GEMINI_API_KEY not set"
Ensure the API key is in your Claude Code settings under `env`.

### Server not loading
Check Claude Code logs. Common issues:
- Python not in PATH
- Missing dependencies
- Incorrect path in settings

### 403 Permission Denied
Your API key may need the Generative Language API enabled in Google Cloud Console.
