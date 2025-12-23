#!/usr/bin/env python3
"""
Test script to verify kernel compatibility with fixed ZENV artifacts.
"""

import sys
import json
import importlib.util
from pathlib import Path

# Load kernel using importlib (filename has dots)
kernel_path = Path(__file__).parent.parent.parent / "kernels" / "BASE_CVR_KERNEL_2.2.3e.py"
spec = importlib.util.spec_from_file_location("kernel", kernel_path)
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)
execute_cvr_workflow = kernel.execute_cvr_workflow

# Load test artifacts
test_dir = Path(__file__).parent

with open(test_dir / "ZENV_A2_ANALYTIC_KG_FULL_FIXED.json") as f:
    kg = json.load(f)

with open(test_dir / "ZENV_A3_CAUSAL_DAG_FULL_FIXED.json") as f:
    dag_artifact = json.load(f)

with open(test_dir / "ZENV_A5_GIM_FULL_FIXED.json") as f:
    gim_artifact = json.load(f)

with open(test_dir / "ZENV_A6_DR_FIXED.json") as f:
    dr_trace = json.load(f)

# Run kernel
print("=" * 60)
print("RUNNING KERNEL WITH FIXED ZENV ARTIFACTS")
print("=" * 60)

try:
    result = execute_cvr_workflow(
        kg=kg,
        dag_artifact=dag_artifact,
        gim_artifact=gim_artifact,
        dr_trace=dr_trace,
        sensitivity_scenarios=None,
        valuation_date="2025-12-23"
    )

    print("\n" + "=" * 60)
    print("SUCCESS! Kernel executed without errors.")
    print("=" * 60)

    # Print key results
    ivps_summary = result.get("ivps_summary", {})
    print(f"\nIVPS: {ivps_summary.get('IVPS', 'N/A')}")
    print(f"DR: {ivps_summary.get('DR', 'N/A')}")
    print(f"Terminal g: {ivps_summary.get('Terminal_g', 'N/A')}")

    # Save result
    output_path = test_dir / "ZENV_A7_VALUATION_FIXED.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult saved to: {output_path}")

except Exception as e:
    print("\n" + "=" * 60)
    print(f"KERNEL FAILED: {type(e).__name__}")
    print("=" * 60)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
