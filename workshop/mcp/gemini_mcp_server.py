#!/usr/bin/env python3
"""
gemini_mcp_server.py
====================
CAPY Pipeline: Gemini MCP Server

A FastMCP server that provides Claude Code access to Gemini APIs.
Supports both Deep Research (for RQ_ASK) and standard generation (for Silicon Council).

TOOLS PROVIDED:
- gemini_deep_research: Long-running research queries via Interactions API
- gemini_generate: Standard text generation with optional thinking mode
- gemini_list_models: List available models

SETUP:
1. Install dependencies:
   pip install fastmcp google-genai

2. Set your API key:
   export GEMINI_API_KEY='your-api-key'

3. Run the server:
   python gemini_mcp_server.py

4. Configure in Claude Code settings (~/.claude/settings.json):
   {
     "mcpServers": {
       "gemini": {
         "command": "python",
         "args": ["/path/to/gemini_mcp_server.py"],
         "env": {
           "GEMINI_API_KEY": "your-api-key"
         }
       }
     }
   }

VERSION: 1.0.0
DATE: 2024-12-18
"""

import os
import sys
import time
import asyncio
from typing import Optional, Literal

# Check dependencies
try:
    from fastmcp import FastMCP
except ImportError:
    print("ERROR: fastmcp not installed. Run: pip install fastmcp")
    sys.exit(1)

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)


# ============================================================================
# CONFIGURATION
# ============================================================================

# Deep Research settings
DEEP_RESEARCH_AGENT = "deep-research-pro-preview-12-2025"
DEEP_RESEARCH_POLL_INTERVAL = 15  # seconds
DEEP_RESEARCH_MAX_WAIT = 60  # minutes

# Default models
DEFAULT_MODEL = "gemini-2.5-pro"
DEFAULT_THINKING_MODEL = "gemini-3-flash-preview"

# Initialize MCP server
mcp = FastMCP("Gemini MCP Server")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_client() -> genai.Client:
    """Get authenticated Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set. "
            "Set it with: export GEMINI_API_KEY='your-api-key'"
        )
    return genai.Client(api_key=api_key)


# ============================================================================
# MCP TOOLS
# ============================================================================

@mcp.tool()
async def gemini_deep_research(
    query: str,
    max_wait_minutes: int = 60
) -> str:
    """
    Execute a deep research query using Gemini Deep Research agent.

    This tool performs comprehensive web research on the given query,
    synthesizing information from hundreds of sources. Ideal for:
    - Market research and competitive analysis
    - Historical data and precedent gathering
    - Industry trend analysis
    - Due diligence research

    Args:
        query: The research question or topic to investigate
        max_wait_minutes: Maximum time to wait for results (default 60)

    Returns:
        The synthesized research report from Gemini Deep Research

    Note: This is a long-running operation that may take 5-30 minutes.
    """
    client = get_client()

    # Start the research in background mode
    interaction = client.interactions.create(
        input=query,
        agent=DEEP_RESEARCH_AGENT,
        background=True
    )

    interaction_id = interaction.id
    max_polls = (max_wait_minutes * 60) // DEEP_RESEARCH_POLL_INTERVAL
    poll_count = 0

    while poll_count < max_polls:
        await asyncio.sleep(DEEP_RESEARCH_POLL_INTERVAL)
        poll_count += 1

        # Get updated status
        interaction = client.interactions.get(interaction_id)
        status = interaction.status

        if status == "completed":
            # Extract and return the result
            if interaction.outputs:
                return interaction.outputs[-1].text
            return "Research completed but no output was generated."

        elif status in ("failed", "cancelled"):
            return f"Research {status}. Please try again."

    return f"Research timed out after {max_wait_minutes} minutes. The query may be too complex."


@mcp.tool()
def gemini_generate(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system_instruction: Optional[str] = None,
    temperature: float = 1.0,
    max_output_tokens: int = 8192
) -> str:
    """
    Generate text using Gemini models.

    This tool provides standard text generation capabilities. Use for:
    - Analysis and synthesis tasks
    - Silicon Council deliberations
    - General purpose generation

    Args:
        prompt: The prompt or question to send to Gemini
        model: Model to use (default: gemini-2.5-pro). Options include:
               - gemini-2.5-pro (balanced)
               - gemini-2.5-flash (faster)
               - gemini-3-pro (most capable)
               - gemini-3-flash (fast + capable)
        system_instruction: Optional system prompt to guide behavior
        temperature: Creativity level 0.0-2.0 (default 1.0)
        max_output_tokens: Maximum response length (default 8192)

    Returns:
        The generated text response
    """
    client = get_client()

    # Build config
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens
    )

    if system_instruction:
        config.system_instruction = system_instruction

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config
    )

    return response.text


@mcp.tool()
def gemini_generate_with_thinking(
    prompt: str,
    model: str = DEFAULT_THINKING_MODEL,
    thinking_level: Literal["minimal", "low", "medium", "high"] = "high",
    system_instruction: Optional[str] = None,
    include_thoughts: bool = False,
    max_output_tokens: int = 16384
) -> str:
    """
    Generate text with extended thinking/reasoning capabilities.

    This tool enables Gemini's thinking mode for complex reasoning tasks.
    Use for:
    - Complex analytical problems
    - Multi-step reasoning
    - Silicon Council deep analysis
    - Problems requiring careful deliberation

    Args:
        prompt: The prompt or question requiring deep reasoning
        model: Model to use (default: gemini-3-flash-preview). Options:
               - gemini-3-flash-preview (recommended for thinking)
               - gemini-3-pro-preview
               - gemini-2.5-pro (uses thinkingBudget instead)
        thinking_level: Depth of reasoning (minimal/low/medium/high)
                       Higher = more thorough but slower
        system_instruction: Optional system prompt
        include_thoughts: If True, returns thought process with response
        max_output_tokens: Maximum response length (default 16384)

    Returns:
        The generated response (optionally with thought summaries)
    """
    client = get_client()

    # Build thinking config
    thinking_config = types.ThinkingConfig(
        thinking_level=thinking_level,
        include_thoughts=include_thoughts
    )

    config = types.GenerateContentConfig(
        thinking_config=thinking_config,
        max_output_tokens=max_output_tokens
    )

    if system_instruction:
        config.system_instruction = system_instruction

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config
    )

    # If thoughts were requested, format them with the response
    if include_thoughts and hasattr(response, 'candidates'):
        result_parts = []
        for candidate in response.candidates:
            if hasattr(candidate, 'thought_summary') and candidate.thought_summary:
                result_parts.append(f"## Thinking Process\n{candidate.thought_summary}\n")
            if hasattr(candidate, 'content') and candidate.content:
                result_parts.append(f"## Response\n{candidate.content.text}")
        if result_parts:
            return '\n'.join(result_parts)

    return response.text


@mcp.tool()
def gemini_list_models() -> str:
    """
    List available Gemini models.

    Returns a list of models that can be used with gemini_generate
    and gemini_generate_with_thinking tools.

    Returns:
        Formatted list of available models and their capabilities
    """
    client = get_client()

    models = list(client.models.list())

    result = ["# Available Gemini Models\n"]

    for model in models:
        name = model.name
        # Filter to just the model ID part
        if name.startswith("models/"):
            name = name[7:]
        result.append(f"- {name}")

    return '\n'.join(result)


# ============================================================================
# BATCH OPERATIONS (for RQ_ASK parallel execution)
# ============================================================================

@mcp.tool()
async def gemini_batch_deep_research(
    queries: list[str],
    max_wait_minutes: int = 60
) -> str:
    """
    Execute multiple deep research queries in parallel.

    This tool runs up to 6 research queries simultaneously, ideal for
    the RQ_ASK stage where multiple research questions need answers.

    Args:
        queries: List of research questions (max 6)
        max_wait_minutes: Maximum time to wait per query (default 60)

    Returns:
        JSON-formatted results with status and content for each query

    Note: This operation may take 10-30 minutes depending on query complexity.
    """
    import json

    if len(queries) > 6:
        return "Error: Maximum 6 queries allowed per batch"

    client = get_client()

    # Start all research tasks
    interactions = []
    for i, query in enumerate(queries):
        interaction = client.interactions.create(
            input=query,
            agent=DEEP_RESEARCH_AGENT,
            background=True
        )
        interactions.append({
            "index": i,
            "query": query[:100] + "..." if len(query) > 100 else query,
            "interaction_id": interaction.id,
            "status": "in_progress",
            "result": None
        })

    # Poll until all complete or timeout
    max_polls = (max_wait_minutes * 60) // DEEP_RESEARCH_POLL_INTERVAL
    poll_count = 0

    while poll_count < max_polls:
        # Check if all done
        pending = [i for i in interactions if i["status"] == "in_progress"]
        if not pending:
            break

        await asyncio.sleep(DEEP_RESEARCH_POLL_INTERVAL)
        poll_count += 1

        # Check each pending interaction
        for item in pending:
            interaction = client.interactions.get(item["interaction_id"])
            status = interaction.status

            if status == "completed":
                item["status"] = "completed"
                if interaction.outputs:
                    item["result"] = interaction.outputs[-1].text
                else:
                    item["result"] = "Completed with no output"
            elif status in ("failed", "cancelled"):
                item["status"] = status
                item["result"] = f"Research {status}"

    # Mark any still pending as timed out
    for item in interactions:
        if item["status"] == "in_progress":
            item["status"] = "timeout"
            item["result"] = f"Timed out after {max_wait_minutes} minutes"

    # Format results
    results = {
        "total": len(queries),
        "completed": sum(1 for i in interactions if i["status"] == "completed"),
        "failed": sum(1 for i in interactions if i["status"] in ("failed", "timeout")),
        "results": interactions
    }

    return json.dumps(results, indent=2)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Check for API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY not set. Set it before using the tools.")
        print("  export GEMINI_API_KEY='your-api-key'")
        print("")

    print("Starting Gemini MCP Server...")
    print(f"Deep Research Agent: {DEEP_RESEARCH_AGENT}")
    print(f"Default Model: {DEFAULT_MODEL}")
    print("")
    print("Available tools:")
    print("  - gemini_deep_research: Single research query")
    print("  - gemini_batch_deep_research: Parallel research queries (up to 6)")
    print("  - gemini_generate: Standard text generation")
    print("  - gemini_generate_with_thinking: Extended thinking mode")
    print("  - gemini_list_models: List available models")
    print("")

    # Run the MCP server
    mcp.run()
