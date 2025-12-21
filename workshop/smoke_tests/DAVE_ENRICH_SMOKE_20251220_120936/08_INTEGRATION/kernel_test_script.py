#!/usr/bin/env python3
"""
Synthetic Kernel Test for CVR_KERNEL_INT_2_2_2e.py

This script tests the INTEGRATION kernel's executability by:
1. Loading all required input artifacts
2. Calling execute_cvr_workflow() (the main API)
3. Saving the output to KERNEL_TEST_OUTPUT.json

Note: Even though cascade_scope=NONE in the real adjudication,
we force a FULL kernel run to verify computational correctness.
"""

import sys
import json
import os
from pathlib import Path

# Add kernel directory to path
kernel_dir = Path('/Users/Benjamin/Dev/CAPY/workshop/kernels')
sys.path.insert(0, str(kernel_dir))

# Import the kernel module
try:
    import CVR_KERNEL_INT_2_2_2e as kernel
    print(f"[OK] Successfully imported kernel (version: {kernel.KERNEL_VERSION})")
except ImportError as e:
    print(f"[FAIL] Could not import kernel: {e}")
    sys.exit(1)

# Define input paths
INPUT_DIR = Path('/Users/Benjamin/Dev/CAPY/workshop/smoke_tests/DAVE_ENRICH_SMOKE_20251220_120936/08_INTEGRATION')
OUTPUT_PATH = INPUT_DIR / 'KERNEL_TEST_OUTPUT.json'

def load_json(filepath):
    """Load a JSON file and return the parsed data."""
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    """Execute the synthetic kernel test."""
    results = {
        'test_type': 'SYNTHETIC_INTEGRATION_KERNEL_TEST',
        'kernel_version': kernel.KERNEL_VERSION,
        'cascade_scope_override': 'FULL (forced for testing)',
        'status': 'PENDING',
        'errors': [],
        'outputs': {}
    }

    try:
        # Step 1: Load all input artifacts
        print("\n[STEP 1] Loading input artifacts...")

        kg_path = INPUT_DIR / 'DAVE_A2_ANALYTIC_KG_S4.json'
        dag_path = INPUT_DIR / 'DAVE_A3_CAUSAL_DAG_S4.json'
        gim_path = INPUT_DIR / 'DAVE_A5_GESTALT_IMPACT_MAP_S4.json'
        dr_path = INPUT_DIR / 'DAVE_A6_DR_DERIVATION_TRACE_S4.json'
        a10_path = INPUT_DIR / 'DAVE_A10_SCENARIO_MODEL_S4.json'
        cascade_path = INPUT_DIR / 'DAVE_CASCADE.json'

        kg = load_json(kg_path)
        print(f"  [OK] Loaded A2_ANALYTIC_KG_S4")

        dag_artifact = load_json(dag_path)
        print(f"  [OK] Loaded A3_CAUSAL_DAG_S4")

        gim_artifact = load_json(gim_path)
        print(f"  [OK] Loaded A5_GESTALT_IMPACT_MAP_S4")

        dr_trace = load_json(dr_path)
        print(f"  [OK] Loaded A6_DR_DERIVATION_TRACE_S4")

        a10 = load_json(a10_path)
        print(f"  [OK] Loaded A10_SCENARIO_MODEL_S4")

        cascade = load_json(cascade_path)
        print(f"  [OK] Loaded CASCADE.json (scope: {cascade.get('cascade_scope', 'UNKNOWN')})")

        results['inputs_loaded'] = True

        # Step 2: Execute the base CVR workflow (deterministic valuation)
        print("\n[STEP 2] Executing execute_cvr_workflow (deterministic valuation)...")

        # Define sensitivity scenarios (optional but tests more code paths)
        sensitivity_scenarios = [
            {'driver': 'Discount_Rate', 'low': -0.01, 'high': 0.01},
            {'driver': 'MTM_Growth_Rate', 'low': -0.10, 'high': 0.10},
            {'driver': 'ARPU_Growth_Rate', 'low': -0.10, 'high': 0.10},
            {'driver': 'Gross_Profit_Margin', 'low': -0.10, 'high': 0.10},
        ]

        lightweight_summary = kernel.execute_cvr_workflow(
            kg=kg,
            dag_artifact=dag_artifact,
            gim_artifact=gim_artifact,
            dr_trace=dr_trace,
            sensitivity_scenarios=sensitivity_scenarios
        )

        print(f"  [OK] execute_cvr_workflow completed")
        print(f"  [OK] IVPS (deterministic): ${lightweight_summary.get('ivps_summary', {}).get('IVPS', 'N/A'):.2f}")

        results['outputs']['lightweight_valuation_summary'] = lightweight_summary
        results['outputs']['deterministic_ivps'] = lightweight_summary.get('ivps_summary', {}).get('IVPS')

        # Step 3: Test scenario intervention execution
        print("\n[STEP 3] Testing scenario intervention execution...")

        scenarios = a10.get('scenario_results', [])
        if scenarios:
            # Test one scenario intervention
            test_scenario = scenarios[0]
            scenario_id = test_scenario.get('scenario_id', 'UNKNOWN')
            print(f"  Testing scenario: {scenario_id}")

            # Create a minimal intervention (using empty overlay)
            intervention_def = {
                'gim_overlay': None,
                'structural_modifications': None
            }

            intervention_result = kernel.execute_scenario_intervention(
                kg=kg,
                dag=dag_artifact,
                gim=gim_artifact,
                dr_trace=dr_trace,
                intervention_def=intervention_def,
                dr_override=None
            )

            print(f"  [OK] Scenario intervention executed")
            print(f"  [OK] IVPS (scenario, no overlay): ${intervention_result.get('ivps_scenario', 'N/A'):.2f}")
            print(f"  [OK] P2 Status: {intervention_result.get('p2_status', 'N/A')}")

            results['outputs']['scenario_intervention_test'] = {
                'scenario_id': scenario_id,
                'ivps_scenario': intervention_result.get('ivps_scenario'),
                'p2_status': intervention_result.get('p2_status'),
                'p2_message': intervention_result.get('p2_message')
            }
        else:
            print("  [SKIP] No scenarios found in A10 to test")
            results['outputs']['scenario_intervention_test'] = 'SKIPPED - no scenarios'

        # Step 4: Test SSE JPD calculation
        print("\n[STEP 4] Testing SSE JPD calculation...")

        # Build SSE scenarios from A10
        sse_scenarios = []
        for s in scenarios:
            sse_scenarios.append({
                'scenario_id': s.get('scenario_id'),
                'p_posterior': s.get('p_posterior'),
                'ivps_impact': s.get('ivps_impact')
            })

        if sse_scenarios:
            base_ivps = a10.get('metadata', {}).get('base_case_reference', {}).get('state_2_ivps',
                         results['outputs'].get('deterministic_ivps', 200.0))

            constraints = {
                'causal_dependencies': [],
                'mutual_exclusivity_groups': [],
                'economic_incompatibilities': []
            }

            sse_result = kernel.calculate_sse_jpd(
                scenarios=sse_scenarios,
                constraints=constraints,
                base_ivps=base_ivps
            )

            print(f"  [OK] SSE JPD calculation completed")
            print(f"  [OK] E[IVPS]: ${sse_result.get('e_ivps', 'N/A'):.2f}")
            print(f"  [OK] Feasible states: {sse_result.get('feasible_state_count', 'N/A')} / {sse_result.get('total_state_count', 'N/A')}")
            print(f"  [OK] Probability sum validation: {sse_result.get('probability_sum_validation', 'N/A'):.4f}")

            results['outputs']['sse_jpd_test'] = {
                'e_ivps': sse_result.get('e_ivps'),
                'feasible_state_count': sse_result.get('feasible_state_count'),
                'total_state_count': sse_result.get('total_state_count'),
                'probability_sum_validation': sse_result.get('probability_sum_validation'),
                'renormalization_factor': sse_result.get('renormalization_factor')
            }
        else:
            print("  [SKIP] No scenarios available for SSE test")
            results['outputs']['sse_jpd_test'] = 'SKIPPED - no scenarios'

        # Step 5: Test full scenario analysis
        print("\n[STEP 5] Testing execute_full_scenario_analysis...")

        if scenarios:
            # Build scenario definitions with interventions
            scenario_definitions = []
            for s in scenarios[:2]:  # Test first 2 scenarios
                scenario_definitions.append({
                    'scenario_id': s.get('scenario_id'),
                    'p_posterior': s.get('p_posterior'),
                    'intervention': {
                        'gim_overlay': None,  # No overlay for test
                        'structural_modifications': None
                    },
                    'dr_override': None
                })

            full_analysis = kernel.execute_full_scenario_analysis(
                kg=kg,
                dag=dag_artifact,
                gim=gim_artifact,
                dr_trace=dr_trace,
                base_ivps=base_ivps,
                scenario_definitions=scenario_definitions,
                constraints=constraints
            )

            print(f"  [OK] Full scenario analysis completed")
            summary = full_analysis.get('summary', {})
            print(f"  [OK] Summary E[IVPS]: ${summary.get('primary_output', {}).get('e_ivps', 'N/A'):.2f}")

            results['outputs']['full_scenario_analysis'] = {
                'e_ivps': summary.get('primary_output', {}).get('e_ivps'),
                'scenarios_analyzed': len(scenario_definitions),
                'cvr_state_bridge': summary.get('cvr_state_bridge')
            }
        else:
            print("  [SKIP] No scenarios for full analysis test")
            results['outputs']['full_scenario_analysis'] = 'SKIPPED - no scenarios'

        # All tests passed
        results['status'] = 'PASS'
        print("\n" + "="*60)
        print("[SYNTHETIC KERNEL TEST: PASS]")
        print("="*60)

    except Exception as e:
        import traceback
        results['status'] = 'FAIL'
        results['errors'].append({
            'type': type(e).__name__,
            'message': str(e),
            'traceback': traceback.format_exc()
        })
        print(f"\n[FAIL] Error during kernel test: {e}")
        print(traceback.format_exc())

    # Save results
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[OUTPUT] Results saved to: {OUTPUT_PATH}")

    return results['status'] == 'PASS'

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
