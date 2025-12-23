#!/usr/bin/env python3
"""
CLI wrapper for CVR_KERNEL_INT (Integration).

Usage:
    python3 run_int_kernel.py \
        --a2 path/to/A2_ANALYTIC_KG.json \
        --a3 path/to/A3_CAUSAL_DAG.json \
        --a5 path/to/A5_GIM.json \
        --a6 path/to/A6_DR.json \
        --a10 path/to/A10_SCENARIO.json \
        --cascade path/to/A12_CASCADE.json \
        --output path/to/A7_VALUATION_INT.json

The kernel re-runs valuation/scenarios if cascade scope is not NONE.

The --cascade file should contain:
{
    "cascade_scope": "NONE" | "VALUATION_ONLY" | "FULL",
    "modifications": [...],
    "scenario_definitions": [...] (if FULL)
}
"""

import argparse
import json
import sys
import os
import importlib.util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KERNELS_DIR = os.path.join(SCRIPT_DIR, '..', 'kernels')

def main():
    parser = argparse.ArgumentParser(description='Run INTEGRATION CVR Kernel')
    parser.add_argument('--a2', required=True, help='Path to A.2 ANALYTIC_KG JSON')
    parser.add_argument('--a3', required=True, help='Path to A.3 CAUSAL_DAG JSON')
    parser.add_argument('--a5', required=True, help='Path to A.5 GIM JSON')
    parser.add_argument('--a6', required=True, help='Path to A.6 DR JSON')
    parser.add_argument('--a10', help='Path to A.10 SCENARIO JSON (for FULL cascade)')
    parser.add_argument('--cascade', required=True, help='Path to A.12 CASCADE JSON')
    parser.add_argument('--output', required=True, help='Path to write output JSON')
    parser.add_argument('--kernel-version', default='2_2_2e', help='Kernel version')

    args = parser.parse_args()

    # Import kernel
    kernel_file = os.path.join(KERNELS_DIR, f"CVR_KERNEL_INT_{args.kernel_version}.py")
    if not os.path.exists(kernel_file):
        print(f"ERROR: Kernel file not found: {kernel_file}", file=sys.stderr)
        sys.exit(1)

    try:
        spec = importlib.util.spec_from_file_location("kernel", kernel_file)
        kernel = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(kernel)
    except Exception as e:
        print(f"ERROR: Could not import kernel: {e}", file=sys.stderr)
        sys.exit(1)

    # Load artifacts
    def load_json(path, name):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            print(f"Loaded {name}: {path}")
            return data
        except Exception as e:
            print(f"ERROR loading {name}: {e}", file=sys.stderr)
            sys.exit(1)

    a2_raw = load_json(args.a2, 'A.2 ANALYTIC_KG')
    a3_raw = load_json(args.a3, 'A.3 CAUSAL_DAG')
    a5_raw = load_json(args.a5, 'A.5 GIM')
    a6_raw = load_json(args.a6, 'A.6 DR')
    cascade = load_json(args.cascade, 'A.12 CASCADE')

    cascade_inner = cascade.get('A.12_CASCADE', cascade)
    cascade_scope = cascade_inner.get('cascade_scope', 'NONE')
    print(f"Cascade scope: {cascade_scope}")

    if cascade_scope == 'NONE':
        print("No recalculation needed (cascade_scope=NONE)")
        # Just copy A.7 from prior state if it exists
        with open(args.output, 'w') as f:
            json.dump({"status": "NONE", "note": "No recalculation needed"}, f, indent=2)
        return 0

    # Unwrap artifacts
    kg = a2_raw.get('A.2_ANALYTIC_KG', a2_raw)
    dag_artifact = a3_raw.get('A.3_CAUSAL_DAG', a3_raw)
    gim_artifact = a5_raw

    # Normalize DR
    a6_inner = a6_raw.get('A.6_DISCOUNT_RATE', a6_raw)
    dr_value = a6_inner.get('DR') or a6_inner.get('DR_Static')
    if 'derivation_trace' in a6_inner:
        dr_value = a6_inner['derivation_trace'].get('DR_Static', dr_value)
    dr_trace = {'derivation_trace': {'DR_Static': dr_value}}
    print(f"DR: {dr_value}")

    print(f"\n{'='*60}")
    print(f"Executing INTEGRATION CVR Kernel v{args.kernel_version}")
    print(f"Cascade: {cascade_scope}")
    print(f"{'='*60}\n")

    if cascade_scope == 'VALUATION_ONLY':
        # Just re-run base valuation
        try:
            result = kernel.execute_cvr_workflow(
                kg=kg,
                dag_artifact=dag_artifact,
                gim_artifact=gim_artifact,
                dr_trace=dr_trace,
                sensitivity_scenarios=None
            )
            output = {"A.7_VALUATION_SUMMARY": result}
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)

    elif cascade_scope == 'FULL':
        # Need to re-run scenarios too
        if not args.a10:
            print("ERROR: FULL cascade requires --a10", file=sys.stderr)
            sys.exit(1)

        a10_raw = load_json(args.a10, 'A.10 SCENARIO')
        a10_inner = a10_raw.get('A.10_SCENARIO_MODEL_OUTPUT', a10_raw)

        # First re-run base valuation to get new IVPS
        try:
            base_result = kernel.execute_cvr_workflow(
                kg=kg,
                dag_artifact=dag_artifact,
                gim_artifact=gim_artifact,
                dr_trace=dr_trace,
                sensitivity_scenarios=None
            )
            base_ivps = base_result.get('ivps_summary', {}).get('IVPS')
            print(f"Recalculated base IVPS: {base_ivps}")
        except Exception as e:
            print(f"ERROR in base valuation: {e}", file=sys.stderr)
            sys.exit(1)

        # Get scenarios from cascade or A.10
        scenario_defs = cascade_inner.get('scenarios_finalized',
                                          a10_inner.get('scenario_results', []))
        constraints = a10_inner.get('sse_integration', {}).get('constraints', {})

        try:
            scen_result = kernel.execute_full_scenario_analysis(
                kg=kg,
                dag=dag_artifact,
                gim=gim_artifact,
                dr_trace=dr_trace,
                base_ivps=base_ivps,
                scenario_definitions=scenario_defs,
                constraints=constraints
            )
            output = {
                "A.7_VALUATION_SUMMARY": base_result,
                "A.10_SCENARIO_MODEL_OUTPUT": scen_result
            }
        except Exception as e:
            print(f"ERROR in scenario analysis: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)

    else:
        print(f"ERROR: Unknown cascade_scope: {cascade_scope}", file=sys.stderr)
        sys.exit(1)

    # Write output
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n{'='*60}")
    print(f"SUCCESS: Wrote output to {args.output}")
    print(f"{'='*60}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
