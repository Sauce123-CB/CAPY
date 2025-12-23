#!/usr/bin/env python3
"""
CLI wrapper for CVR_KERNEL_SCEN (Scenario Analysis).

Usage:
    python3 run_scen_kernel.py \
        --a2 path/to/A2_ANALYTIC_KG.json \
        --a3 path/to/A3_CAUSAL_DAG.json \
        --a5 path/to/A5_GIM.json \
        --a6 path/to/A6_DR.json \
        --a7 path/to/A7_VALUATION.json \
        --args path/to/SCENARIO_ARGS.json \
        --output path/to/A10_SCENARIO.json

The kernel requires A.2-A.7 plus scenario execution args from T1.
It produces A.10 (Scenario Model Output).

The --args file should contain:
{
    "scenario_definitions": [...],
    "constraints": {...}
}
"""

import argparse
import json
import sys
import os
import importlib.util

# Add kernels directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KERNELS_DIR = os.path.join(SCRIPT_DIR, '..', 'kernels')

def main():
    parser = argparse.ArgumentParser(description='Run SCENARIO CVR Kernel')
    parser.add_argument('--a2', required=True, help='Path to A.2 ANALYTIC_KG JSON')
    parser.add_argument('--a3', required=True, help='Path to A.3 CAUSAL_DAG JSON')
    parser.add_argument('--a5', required=True, help='Path to A.5 GIM JSON')
    parser.add_argument('--a6', required=True, help='Path to A.6 DR JSON')
    parser.add_argument('--a7', required=True, help='Path to A.7 VALUATION JSON (for base IVPS)')
    parser.add_argument('--args', required=True, help='Path to scenario execution args JSON')
    parser.add_argument('--output', required=True, help='Path to write A.10 output JSON')
    parser.add_argument('--kernel-version', default='2_2_2e', help='Kernel version to use')

    args = parser.parse_args()

    # Import kernel using importlib (handles underscores/dots in filename)
    kernel_file = os.path.join(KERNELS_DIR, f"CVR_KERNEL_SCEN_{args.kernel_version}.py")
    if not os.path.exists(kernel_file):
        print(f"ERROR: Kernel file not found: {kernel_file}", file=sys.stderr)
        sys.exit(1)

    try:
        spec = importlib.util.spec_from_file_location("kernel", kernel_file)
        kernel = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(kernel)
    except Exception as e:
        print(f"ERROR: Could not import kernel from {kernel_file}: {e}", file=sys.stderr)
        sys.exit(1)

    # Load input artifacts
    def load_json(path, name):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            print(f"Loaded {name}: {path}")
            return data
        except Exception as e:
            print(f"ERROR loading {name} from {path}: {e}", file=sys.stderr)
            sys.exit(1)

    a2_raw = load_json(args.a2, 'A.2 ANALYTIC_KG')
    a3_raw = load_json(args.a3, 'A.3 CAUSAL_DAG')
    a5_raw = load_json(args.a5, 'A.5 GIM')
    a6_raw = load_json(args.a6, 'A.6 DR')
    a7_raw = load_json(args.a7, 'A.7 VALUATION')
    scen_args = load_json(args.args, 'Scenario Args')

    # Unwrap artifacts
    kg = a2_raw.get('A.2_ANALYTIC_KG', a2_raw)
    dag = a3_raw.get('A.3_CAUSAL_DAG', a3_raw)
    gim = a5_raw.get('A.5_GESTALT_IMPACT_MAP', a5_raw)

    # Get base IVPS from A.7
    a7_inner = a7_raw.get('A.7_VALUATION_SUMMARY', a7_raw)
    base_ivps = a7_inner.get('ivps_summary', {}).get('IVPS')
    if base_ivps is None:
        print(f"ERROR: Could not find IVPS in A.7. Keys present: {list(a7_inner.keys())}", file=sys.stderr)
        sys.exit(1)
    print(f"Base IVPS: {base_ivps}")

    # Normalize A.6 DR structure
    a6_inner = a6_raw.get('A.6_DISCOUNT_RATE', a6_raw)
    dr_value = None
    if 'derivation_trace' in a6_inner and 'DR_Static' in a6_inner['derivation_trace']:
        dr_value = a6_inner['derivation_trace']['DR_Static']
    elif 'DR' in a6_inner:
        dr_value = a6_inner['DR']
    elif 'DR_Static' in a6_inner:
        dr_value = a6_inner['DR_Static']

    if dr_value is None:
        print(f"ERROR: Could not find DR value in A.6. Keys present: {list(a6_inner.keys())}", file=sys.stderr)
        sys.exit(1)

    dr_trace = {'derivation_trace': {'DR_Static': dr_value}}
    print(f"DR: {dr_value}")

    # Get scenario definitions and constraints from args
    scenario_definitions = scen_args.get('scenario_definitions', scen_args.get('scenarios', []))
    constraints = scen_args.get('constraints', {})

    if not scenario_definitions:
        print(f"ERROR: No scenario_definitions found in args. Keys: {list(scen_args.keys())}", file=sys.stderr)
        sys.exit(1)

    print(f"Scenarios: {len(scenario_definitions)}")
    print(f"Constraints: {list(constraints.keys())}")

    # Execute kernel
    print(f"\n{'='*60}")
    print(f"Executing SCENARIO CVR Kernel v{args.kernel_version}")
    print(f"{'='*60}\n")

    try:
        result = kernel.execute_full_scenario_analysis(
            kg=kg,
            dag=dag,
            gim=gim,
            dr_trace=dr_trace,
            base_ivps=base_ivps,
            scenario_definitions=scenario_definitions,
            constraints=constraints
        )
    except Exception as e:
        print(f"\nERROR during kernel execution: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Write output
    try:
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(args.output, 'w') as f:
            json.dump({"A.10_SCENARIO_MODEL_OUTPUT": result}, f, indent=2)
        print(f"\n{'='*60}")
        print(f"SUCCESS: Wrote A.10 to {args.output}")
        print(f"{'='*60}")

        # Print key results
        e_ivps = result.get('sse_integration', {}).get('E_IVPS')
        num_states = result.get('sse_integration', {}).get('num_states')
        print(f"\nKey Results:")
        print(f"  E[IVPS]: {e_ivps}")
        print(f"  Base IVPS: {base_ivps}")
        print(f"  SSE States: {num_states}")

    except Exception as e:
        print(f"ERROR writing output to {args.output}: {e}", file=sys.stderr)
        sys.exit(1)

    return 0

if __name__ == '__main__':
    sys.exit(main())
