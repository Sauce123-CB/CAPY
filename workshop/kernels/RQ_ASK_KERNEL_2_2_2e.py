#!/usr/bin/env python3
"""
RQ_ASK_KERNEL_2_2_2e.py
========================
CAPY Pipeline: Research Question Execution Kernel

Executes 6 research questions in parallel via Gemini Deep Research API.
Uses the Interactions API with background mode for long-running research tasks.

REQUIREMENTS:
- Python 3.9+
- google-genai >= 1.55.0
- GEMINI_API_KEY environment variable set

USAGE:
    python RQ_ASK_KERNEL_2_2_2e.py <input_json> <output_dir>

    input_json: Path to A.8_RESEARCH_STRATEGY_MAP JSON file from RQ_GEN
    output_dir: Directory to write research bundle outputs

EXAMPLE:
    export GEMINI_API_KEY='your-api-key'
    python RQ_ASK_KERNEL_2_2_2e.py ./DAVE_A8_research_strategy.json ./research_output/

VERSION: 2.2.2e
DATE: 2024-12-18
"""

import os
import sys
import json
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict

# Attempt to import google-genai
try:
    from google import genai
except ImportError:
    print("ERROR: google-genai package not installed.")
    print("Install with: pip install google-genai")
    sys.exit(1)


# ============================================================================
# CONFIGURATION
# ============================================================================

DEEP_RESEARCH_AGENT = "deep-research-pro-preview-12-2025"
POLL_INTERVAL_SECONDS = 15  # How often to check research status
MAX_WAIT_MINUTES = 60  # Maximum time to wait for a single research task
CONCURRENT_LIMIT = 6  # All 6 queries run in parallel


@dataclass
class ResearchQuery:
    """Single research query with metadata."""
    rq_id: str
    coverage_objective: str
    platform_rationale: str
    a7_linkage: str
    prompt_text: str


@dataclass
class ResearchResult:
    """Result from a single research query."""
    rq_id: str
    status: str  # "completed", "failed", "timeout"
    interaction_id: Optional[str]
    result_text: Optional[str]
    error_message: Optional[str]
    duration_seconds: float
    timestamp: str


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def load_research_strategy(input_path: str) -> list[ResearchQuery]:
    """Load A.8 Research Strategy Map and extract research queries."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle nested structure if present
    if "A.8_RESEARCH_STRATEGY_MAP" in data:
        strategy = data["A.8_RESEARCH_STRATEGY_MAP"]
    else:
        strategy = data

    research_plan = strategy.get("Research_Plan", [])

    queries = []
    for item in research_plan:
        queries.append(ResearchQuery(
            rq_id=item.get("RQ_ID", f"RQ{len(queries)+1}"),
            coverage_objective=item.get("Coverage_Objective", ""),
            platform_rationale=item.get("Platform_Rationale", ""),
            a7_linkage=item.get("A7_Linkage", ""),
            prompt_text=item.get("Prompt_Text", "")
        ))

    return queries


async def execute_research_query(
    client: genai.Client,
    query: ResearchQuery,
    semaphore: asyncio.Semaphore
) -> ResearchResult:
    """
    Execute a single research query using Gemini Deep Research.
    Uses background mode and polls for completion.
    """
    async with semaphore:
        start_time = time.time()
        timestamp = datetime.now().isoformat()

        print(f"[{query.rq_id}] Starting Deep Research...")
        print(f"    Objective: {query.coverage_objective}")

        try:
            # Start the Deep Research interaction in background mode
            interaction = client.interactions.create(
                input=query.prompt_text,
                agent=DEEP_RESEARCH_AGENT,
                background=True
            )

            interaction_id = interaction.id
            print(f"[{query.rq_id}] Interaction started: {interaction_id}")

            # Poll for completion
            max_polls = (MAX_WAIT_MINUTES * 60) // POLL_INTERVAL_SECONDS
            poll_count = 0

            while poll_count < max_polls:
                await asyncio.sleep(POLL_INTERVAL_SECONDS)
                poll_count += 1

                # Get updated status
                interaction = client.interactions.get(interaction_id)
                status = interaction.status

                elapsed = time.time() - start_time
                print(f"[{query.rq_id}] Status: {status} ({elapsed:.0f}s elapsed)")

                if status == "completed":
                    # Extract the result text
                    result_text = ""
                    if interaction.outputs:
                        result_text = interaction.outputs[-1].text

                    duration = time.time() - start_time
                    print(f"[{query.rq_id}] COMPLETED in {duration:.0f}s")

                    return ResearchResult(
                        rq_id=query.rq_id,
                        status="completed",
                        interaction_id=interaction_id,
                        result_text=result_text,
                        error_message=None,
                        duration_seconds=duration,
                        timestamp=timestamp
                    )

                elif status in ("failed", "cancelled"):
                    duration = time.time() - start_time
                    error_msg = f"Research {status}"
                    print(f"[{query.rq_id}] FAILED: {error_msg}")

                    return ResearchResult(
                        rq_id=query.rq_id,
                        status="failed",
                        interaction_id=interaction_id,
                        result_text=None,
                        error_message=error_msg,
                        duration_seconds=duration,
                        timestamp=timestamp
                    )

            # Timeout
            duration = time.time() - start_time
            print(f"[{query.rq_id}] TIMEOUT after {duration:.0f}s")

            return ResearchResult(
                rq_id=query.rq_id,
                status="timeout",
                interaction_id=interaction_id,
                result_text=None,
                error_message=f"Exceeded {MAX_WAIT_MINUTES} minute timeout",
                duration_seconds=duration,
                timestamp=timestamp
            )

        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            print(f"[{query.rq_id}] ERROR: {error_msg}")

            return ResearchResult(
                rq_id=query.rq_id,
                status="failed",
                interaction_id=None,
                result_text=None,
                error_message=error_msg,
                duration_seconds=duration,
                timestamp=timestamp
            )


async def execute_all_queries(
    client: genai.Client,
    queries: list[ResearchQuery]
) -> list[ResearchResult]:
    """Execute all research queries in parallel."""
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)

    tasks = [
        execute_research_query(client, query, semaphore)
        for query in queries
    ]

    results = await asyncio.gather(*tasks)
    return list(results)


def compile_research_bundle(
    queries: list[ResearchQuery],
    results: list[ResearchResult],
    output_dir: Path
) -> dict:
    """
    Compile all research results into a single bundle for ENRICH stage.

    Creates:
    - research_bundle.json: Structured data for downstream processing
    - research_bundle.md: Human-readable markdown compilation
    - Individual RQ result files
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create result lookup
    result_map = {r.rq_id: r for r in results}

    # Build the bundle structure
    bundle = {
        "schema_version": "2.2.2e",
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_queries": len(queries),
            "completed": sum(1 for r in results if r.status == "completed"),
            "failed": sum(1 for r in results if r.status == "failed"),
            "timeout": sum(1 for r in results if r.status == "timeout"),
            "total_duration_seconds": sum(r.duration_seconds for r in results)
        },
        "research_results": []
    }

    # Build markdown content
    md_lines = [
        "# Research Bundle: RQ_ASK Output",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "",
        f"- Total Queries: {bundle['summary']['total_queries']}",
        f"- Completed: {bundle['summary']['completed']}",
        f"- Failed: {bundle['summary']['failed']}",
        f"- Timeout: {bundle['summary']['timeout']}",
        "",
        "---",
        ""
    ]

    # Process each query/result pair
    for query in queries:
        result = result_map.get(query.rq_id)

        entry = {
            "rq_id": query.rq_id,
            "coverage_objective": query.coverage_objective,
            "a7_linkage": query.a7_linkage,
            "prompt_text": query.prompt_text,
            "status": result.status if result else "missing",
            "result_text": result.result_text if result else None,
            "error_message": result.error_message if result else None,
            "duration_seconds": result.duration_seconds if result else 0
        }
        bundle["research_results"].append(entry)

        # Add to markdown
        md_lines.extend([
            f"## {query.rq_id}: {query.coverage_objective}",
            "",
            f"**Linkage:** {query.a7_linkage}",
            "",
            "### Query",
            "",
            "```",
            query.prompt_text,
            "```",
            "",
            f"### Response (Status: {result.status if result else 'missing'})",
            ""
        ])

        if result and result.status == "completed" and result.result_text:
            md_lines.append(result.result_text)

            # Also write individual result file
            rq_file = output_dir / f"{query.rq_id}_result.md"
            with open(rq_file, 'w', encoding='utf-8') as f:
                f.write(f"# {query.rq_id}: {query.coverage_objective}\n\n")
                f.write(f"**Query:**\n\n{query.prompt_text}\n\n")
                f.write(f"**Response:**\n\n{result.result_text}")
        elif result and result.error_message:
            md_lines.append(f"**ERROR:** {result.error_message}")
        else:
            md_lines.append("*No result available*")

        md_lines.extend(["", "---", ""])

    # Write JSON bundle
    json_path = output_dir / "research_bundle.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, indent=2)
    print(f"Wrote: {json_path}")

    # Write markdown bundle
    md_path = output_dir / "research_bundle.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    print(f"Wrote: {md_path}")

    return bundle


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python RQ_ASK_KERNEL_2_2_2e.py <input_json> <output_dir>")
        print("")
        print("  input_json: Path to A.8_RESEARCH_STRATEGY_MAP JSON from RQ_GEN")
        print("  output_dir: Directory for output files")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = Path(sys.argv[2])

    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set")
        print("Set it with: export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)

    # Validate input file
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    print("=" * 60)
    print("CAPY RQ_ASK Kernel v2.2.2e")
    print("=" * 60)
    print(f"Input:  {input_path}")
    print(f"Output: {output_dir}")
    print(f"Agent:  {DEEP_RESEARCH_AGENT}")
    print("")

    # Load research strategy
    print("Loading research strategy...")
    queries = load_research_strategy(input_path)
    print(f"Found {len(queries)} research queries")
    print("")

    # Initialize client
    print("Initializing Gemini client...")
    client = genai.Client(api_key=api_key)

    # Execute queries
    print("")
    print("=" * 60)
    print("EXECUTING RESEARCH QUERIES")
    print("=" * 60)
    print(f"Running {len(queries)} queries in parallel...")
    print(f"Max wait time per query: {MAX_WAIT_MINUTES} minutes")
    print("")

    start_time = time.time()
    results = asyncio.run(execute_all_queries(client, queries))
    total_time = time.time() - start_time

    # Summary
    print("")
    print("=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)
    completed = sum(1 for r in results if r.status == "completed")
    failed = sum(1 for r in results if r.status == "failed")
    timeout = sum(1 for r in results if r.status == "timeout")

    print(f"Completed: {completed}/{len(queries)}")
    print(f"Failed:    {failed}/{len(queries)}")
    print(f"Timeout:   {timeout}/{len(queries)}")
    print(f"Total time: {total_time:.0f}s ({total_time/60:.1f} min)")
    print("")

    # Compile bundle
    print("=" * 60)
    print("COMPILING RESEARCH BUNDLE")
    print("=" * 60)
    bundle = compile_research_bundle(queries, results, output_dir)

    print("")
    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"Research bundle ready at: {output_dir}")
    print("")
    print("Next step: Feed research_bundle.json to ENRICH stage")

    # Return exit code based on success
    if completed == len(queries):
        return 0
    elif completed > 0:
        return 1  # Partial success
    else:
        return 2  # Total failure


if __name__ == "__main__":
    sys.exit(main())
