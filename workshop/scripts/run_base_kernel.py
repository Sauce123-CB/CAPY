#!/usr/bin/env python3
"""
CLI wrapper for BASE_CVR_KERNEL.

Usage:
    python3 run_base_kernel.py \
        --a2 path/to/A2_ANALYTIC_KG.json \
        --a3 path/to/A3_CAUSAL_DAG.json \
        --a5 path/to/A5_GIM.json \
        --a6 path/to/A6_DR.json \
        --output path/to/A7_VALUATION.json

The kernel requires A.2 (KG), A.3 (DAG), A.5 (GIM), and A.6 (DR).
It produces A.7 (Valuation Summary).
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
    parser = argparse.ArgumentParser(description='Run BASE CVR Kernel')
    parser.add_argument('--a2', required=True, help='Path to A.2 ANALYTIC_KG JSON')
    parser.add_argument('--a3', required=True, help='Path to A.3 CAUSAL_DAG JSON')
    parser.add_argument('--a5', required=True, help='Path to A.5 GIM JSON')
    parser.add_argument('--a6', required=True, help='Path to A.6 DR JSON')
    parser.add_argument('--output', required=True, help='Path to write A.7 output JSON')
    parser.add_argument('--kernel-version', default='2.2.3e', help='Kernel version to use')

    args = parser.parse_args()

    # Import kernel using importlib (handles dots in filename)
    kernel_file = os.path.join(KERNELS_DIR, f"BASE_CVR_KERNEL_{args.kernel_version}.py")
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

    # Unwrap artifacts if needed (handle {"A.2_ANALYTIC_KG": {...}} format)
    kg = a2_raw.get('A.2_ANALYTIC_KG', a2_raw)
    dag_artifact = a3_raw.get('A.3_CAUSAL_DAG', a3_raw)
    gim_artifact = a5_raw  # Kernel handles unwrapping internally

    # Normalize A.6 DR structure - kernel expects derivation_trace.DR_Static
    a6_inner = a6_raw.get('A.6_DISCOUNT_RATE', a6_raw)

    # Find DR value from various possible locations
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

    # Normalize to expected schema
    dr_trace = {
        'derivation_trace': {
            'DR_Static': dr_value
        }
    }
    print(f"Normalized DR: {dr_value}")

    # Execute kernel
    print(f"\n{'='*60}")
    print(f"Executing BASE CVR Kernel v{args.kernel_version}")
    print(f"{'='*60}\n")

    try:
        result = kernel.execute_cvr_workflow(
            kg=kg,
            dag_artifact=dag_artifact,
            gim_artifact=gim_artifact,
            dr_trace=dr_trace,
            sensitivity_scenarios=None,
            valuation_date=None
        )
    except Exception as e:
        print(f"\nERROR during kernel execution: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Write output
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(args.output, 'w') as f:
            json.dump({"A.7_VALUATION_SUMMARY": result}, f, indent=2)
        print(f"\n{'='*60}")
        print(f"SUCCESS: Wrote A.7 to {args.output}")
        print(f"{'='*60}")

        # Print key results
        ivps = result.get('ivps_summary', {}).get('IVPS')
        dr = result.get('ivps_summary', {}).get('DR')
        g = result.get('ivps_summary', {}).get('Terminal_g')
        print(f"\nKey Results:")
        print(f"  IVPS: {ivps}")
        print(f"  DR: {dr}")
        print(f"  Terminal g: {g}")

    except Exception as e:
        print(f"ERROR writing output to {args.output}: {e}", file=sys.stderr)
        sys.exit(1)

    return 0

if __name__ == '__main__':
    sys.exit(main())
