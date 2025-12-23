#!/usr/bin/env python3
"""
CLI wrapper for CVR_KERNEL_IRR (Expected Return Analysis).

Usage:
    python3 run_irr_kernel.py \
        --a2 path/to/A2_ANALYTIC_KG.json \
        --a7 path/to/A7_VALUATION.json \
        --a10 path/to/A10_SCENARIO.json \
        --a13 path/to/A13_RESOLUTION.json \
        --output path/to/A14_IRR_ANALYSIS.json

The kernel requires A.2, A.7, A.10, and A.13 (resolution estimates).
It produces A.14 (IRR Analysis).
"""

import argparse
import json
import sys
import os
import importlib.util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KERNELS_DIR = os.path.join(SCRIPT_DIR, '..', 'kernels')

def main():
    parser = argparse.ArgumentParser(description='Run IRR CVR Kernel')
    parser.add_argument('--a2', required=True, help='Path to A.2 ANALYTIC_KG JSON')
    parser.add_argument('--a7', required=True, help='Path to A.7 VALUATION JSON')
    parser.add_argument('--a10', required=True, help='Path to A.10 SCENARIO JSON')
    parser.add_argument('--a13', required=True, help='Path to A.13 RESOLUTION JSON')
    parser.add_argument('--output', required=True, help='Path to write A.14 output JSON')
    parser.add_argument('--kernel-version', default='2.2.5e', help='Kernel version')

    args = parser.parse_args()

    # Import kernel
    kernel_file = os.path.join(KERNELS_DIR, f"CVR_KERNEL_IRR_{args.kernel_version}.py")
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
    a7_raw = load_json(args.a7, 'A.7 VALUATION')
    a10_raw = load_json(args.a10, 'A.10 SCENARIO')
    a13_raw = load_json(args.a13, 'A.13 RESOLUTION')

    # Unwrap artifacts
    kg = a2_raw.get('A.2_ANALYTIC_KG', a2_raw)
    a7_summary = a7_raw.get('A.7_VALUATION_SUMMARY', a7_raw)
    a9_scenario = a10_raw.get('A.10_SCENARIO_MODEL_OUTPUT', a10_raw)
    a13 = a13_raw.get('A.13_RESOLUTION', a13_raw)

    # Extract rho estimates from A.13
    rho_estimates = a13.get('rho_estimates', {})
    if not rho_estimates and 'scenario_resolution' in a13:
        # Alternative format
        for s in a13.get('scenario_resolution', []):
            sid = s.get('scenario_id')
            rho = s.get('rho', s.get('resolution_percentage'))
            if sid and rho is not None:
                rho_estimates[sid] = rho

    convergence_rate = a13.get('convergence_rate_assessment', {}).get('cr_final', 0.20)
    multiple_selection = a13.get('multiple_selection', None)

    print(f"Rho estimates: {rho_estimates}")
    print(f"Convergence rate: {convergence_rate}")

    # Extract market price from A.13 if present
    market_price = a13.get('market_inputs', {}).get('current_price')
    if market_price:
        print(f"Market price: {market_price}")

    print(f"\n{'='*60}")
    print(f"Executing IRR CVR Kernel v{args.kernel_version}")
    print(f"{'='*60}\n")

    try:
        result = kernel.execute_irr_workflow(
            kg=kg,
            a7_summary=a7_summary,
            a9_scenario_output=a9_scenario,
            a11_integration_trace=None,  # Not always needed
            rho_estimates=rho_estimates,
            hurdle_rate=0.15,
            capital_allocation='RETAIN_FCF',
            use_transition_factor=True,
            convergence_rate=convergence_rate,
            multiple_selection=multiple_selection
        )
    except Exception as e:
        print(f"ERROR during kernel execution: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Write output
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump({"A.14_IRR_ANALYSIS": result}, f, indent=2)

    print(f"\n{'='*60}")
    print(f"SUCCESS: Wrote A.14 to {args.output}")
    print(f"{'='*60}")

    # Print key results
    e_irr = result.get('irr_distribution', {}).get('E_IRR')
    p10 = result.get('irr_distribution', {}).get('P10')
    p90 = result.get('irr_distribution', {}).get('P90')
    print(f"\nKey Results:")
    print(f"  E[IRR]: {e_irr}")
    print(f"  P10-P90: [{p10}, {p90}]")

    return 0

if __name__ == '__main__':
    sys.exit(main())
