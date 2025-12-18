#!/usr/bin/env python3
"""
run_rq_ask.py
CLI wrapper for RQ_ASK_KERNEL_2_2_2e.py

Usage:
    python run_rq_ask.py <a8_json_path> <output_dir> <ticker>

Example:
    python run_rq_ask.py \
        production/analyses/{TICKER}_CAPY_{TIMESTAMP}/04_RQ/{TICKER}_A8_RESEARCH_PLAN.json \
        production/analyses/{TICKER}_CAPY_{TIMESTAMP}/04_RQ \
        {TICKER}

Output:
    Creates A9_RESEARCH_RESULTS_{TICKER}_{TIMESTAMP}.json in output_dir
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Add kernels directory to path for import
sys.path.insert(0, str(Path(__file__).parent))

from RQ_ASK_KERNEL_2_2_2e import execute_research_plan, save_results


def main():
    parser = argparse.ArgumentParser(
        description="Execute RQ_ASK research plan via Gemini Deep Research"
    )
    parser.add_argument(
        "a8_path",
        type=str,
        help="Path to A.8 Research Plan JSON file"
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="Directory to save A.9 results"
    )
    parser.add_argument(
        "ticker",
        type=str,
        help="Company ticker symbol"
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=6,
        help="Maximum concurrent queries (default: 6)"
    )
    parser.add_argument(
        "--use-sdk",
        action="store_true",
        help="Use SDK instead of CLI (requires GEMINI_API_KEY)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse A.8 and show queries without executing"
    )

    args = parser.parse_args()

    # Load A.8 research plan
    a8_path = Path(args.a8_path)
    if not a8_path.exists():
        print(f"ERROR: A.8 file not found: {a8_path}", file=sys.stderr)
        sys.exit(1)

    with open(a8_path, 'r') as f:
        a8_data = json.load(f)

    # Extract research plan from A.8 wrapper
    if "A.8_RESEARCH_STRATEGY_MAP" in a8_data:
        research_plan = a8_data["A.8_RESEARCH_STRATEGY_MAP"]
    else:
        # Assume it's the inner structure directly
        research_plan = a8_data

    # Dry run - just show what would be executed
    if args.dry_run:
        rq_list = research_plan.get("Research_Plan", [])
        print(f"\n=== DRY RUN: {len(rq_list)} queries for {args.ticker} ===\n")
        for rq in rq_list:
            print(f"[{rq['RQ_ID']}] {rq.get('Coverage_Objective', 'N/A')}")
            print(f"  Platform: {rq.get('Platform', 'GDR')}")
            print(f"  Prompt: {rq['Prompt_Text'][:100]}...")
            print()
        sys.exit(0)

    # Execute research plan
    print(f"\n=== Executing RQ_ASK for {args.ticker} ===")
    print(f"A.8 Source: {a8_path}")
    print(f"Output Dir: {args.output_dir}")
    print(f"Max Concurrent: {args.max_concurrent}")
    print(f"Mode: {'SDK' if args.use_sdk else 'CLI'}")
    print()

    results = asyncio.run(
        execute_research_plan(
            research_plan=research_plan,
            ticker=args.ticker,
            max_concurrent=args.max_concurrent,
            use_cli=not args.use_sdk
        )
    )

    # Save results
    output_path = save_results(results, args.output_dir)

    # Print summary
    print(f"\n=== Execution Complete ===")
    print(f"Total Queries: {results.total_queries}")
    print(f"Successful: {results.successful_queries}")
    print(f"Failed: {results.failed_queries}")
    print(f"Total Time: {results.execution_time_seconds:.1f}s")
    print(f"Results saved to: {output_path}")

    # Exit with error if any queries failed
    if results.failed_queries > 0:
        print(f"\nWARNING: {results.failed_queries} queries failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
