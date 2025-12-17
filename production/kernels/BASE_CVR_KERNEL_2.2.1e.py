import numpy as np
import pandas as pd
import json
import math
from collections import deque, defaultdict
import re
import copy
import datetime
import logging


# ==========================================================================================
# CVR KERNEL (G3_2.2.1e Implementation - MRC Paradigm / Integrity Update)
# ==========================================================================================


# Configuration
FORECAST_YEARS = 20
EPSILON = 1e-9
KERNEL_VERSION = "G3_2.2.1e"
SENSITIVITY_TORNADO_TOP_N = 5
TERMINAL_G_RFR_CAP = True # If True, Terminal g is capped at RFR


# Configure Logging (Minimal logging for production)
logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ==========================================================================================
# 1. CORE ENGINES (DSL, SCM, APV)
# ==========================================================================================


# 1.1 Assumption DSL (Domain Specific Language) Engine
def apply_dsl(dsl, y0_value=None, forecast_years=FORECAST_YEARS):
    """Applies the DSL definition to generate a forecast array."""
    mode = dsl.get('mode')
    params = dsl.get('params', {})
    forecast = np.zeros(forecast_years)


    if mode == 'STATIC':
        value = float(params.get('value', 0))
        forecast.fill(value)


    elif mode == 'LINEAR_FADE':
        start_value = float(params.get('start_value'))
        end_value = float(params.get('end_value'))
        fade_years = int(params.get('fade_years'))


        if fade_years > forecast_years:
            fade_years = forecast_years


        if fade_years > 0:
            fade_steps = np.linspace(start_value, end_value, fade_years)
            forecast[:fade_years] = fade_steps


        if fade_years < forecast_years:
            forecast[fade_years:] = end_value


    elif mode == 'CAGR_INTERP':
        if y0_value is None:
            raise ValueError("CAGR_INTERP requires a valid y0_value.")


        start_cagr = float(params.get('start_cagr'))
        end_cagr = float(params.get('end_cagr'))
        interp_years = int(params.get('interp_years'))


        if interp_years > forecast_years:
            interp_years = forecast_years


        # 1. Generate the CAGR time series
        cagr_series = np.zeros(forecast_years)
        if interp_years > 0:
            cagr_steps = np.linspace(start_cagr, end_cagr, interp_years)
            cagr_series[:interp_years] = cagr_steps


        if interp_years < forecast_years:
            cagr_series[interp_years:] = end_cagr


        # 2. Apply the CAGR series to the base value
        current_value = y0_value
        for i in range(forecast_years):
            current_value *= (1 + cagr_series[i])
            forecast[i] = current_value


    elif mode == 'EXPLICIT_SCHEDULE':
        # (Implementation for EXPLICIT_SCHEDULE)
        schedule = params.get('schedule', {})
        sorted_years = sorted([int(y) for y in schedule.keys()])


        if not sorted_years:
            return forecast


        start_year = sorted_years[0]
        start_value = float(schedule[str(start_year)])


        if start_year > 1:
            forecast[:start_year-1] = start_value


        for i in range(len(sorted_years)):
            year = sorted_years[i]
            value = float(schedule[str(year)])
            idx = year - 1


            if idx < forecast_years:
                forecast[idx] = value


            if i + 1 < len(sorted_years):
                next_year = sorted_years[i+1]
                next_value = float(schedule[str(next_year)])
                next_idx = next_year - 1


                if next_year > year + 1:
                    gap_years = next_year - year
                    interp_steps = np.linspace(value, next_value, gap_years + 1)


                    start_fill_idx = idx + 1
                    end_fill_idx = next_idx


                    if end_fill_idx <= forecast_years:
                        forecast[start_fill_idx:end_fill_idx] = interp_steps[1:-1]
                    elif start_fill_idx < forecast_years:
                        fill_len = forecast_years - start_fill_idx
                        forecast[start_fill_idx:] = interp_steps[1:1+fill_len]


        last_defined_year = sorted_years[-1]
        if last_defined_year < forecast_years:
            last_value = float(schedule[str(last_defined_year)])
            forecast[last_defined_year-1:] = last_value


    else:
        raise ValueError(f"Unknown DSL mode: {mode}")


    return forecast


# 1.2 SCM (Structural Causal Model) Engine


def topological_sort(dag):
    """
    Performs a topological sort on the DAG.
    (G3_1.8 Hardening): Ensures only intra-timestep dependencies (GET calls) are considered.
    """
    in_degree = defaultdict(int)
    graph = defaultdict(list)
    nodes = set(dag.keys())


    # Regex to find GET('NodeName') calls (intra-timestep dependencies)
    get_regex = re.compile(r"GET\(['\"](.*?)['\"]\)")


    for node, definition in dag.items():
        # 1. Explicit dependencies from 'parents' list
        parents = definition.get('parents', [])
        for parent in parents:
            if parent in nodes and parent != node:
                if node not in graph[parent]:
                    graph[parent].append(node)
                    in_degree[node] += 1


        # 2. Implicit dependencies from 'equation' string (GET calls)
        equation = definition.get('equation', '')
        if equation:
            matches = get_regex.findall(equation)
            for dependency in matches:
                if dependency in nodes and dependency != node:
                    # Check if this dependency is already accounted for
                    if node not in graph[dependency]:
                        graph[dependency].append(node)
                        in_degree[node] += 1


    # 3. Perform the sort (Kahn's algorithm)
    queue = deque([node for node in nodes if in_degree[node] == 0])
    sorted_list = []


    while queue:
        node = queue.popleft()
        sorted_list.append(node)


        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)


    if len(sorted_list) != len(nodes):
        cycle_nodes = [node for node in nodes if in_degree[node] > 0]
        raise RuntimeError(f"A cycle was detected in the DAG. Check nodes for circular dependencies (must use PREV for lagged dependencies): {cycle_nodes}")


    return sorted_list


def prepare_inputs(kg, gim):
    """Prepares inputs by applying the DSL to generate forecast arrays for exogenous drivers."""
    inputs = {}
    y0_data = kg.get('core_data', {}).get('Y0_data', {})


    for handle, definition in gim.items():
        y0_value = y0_data.get(handle)


        if definition['mode'] == 'CAGR_INTERP' and y0_value is None:
            logger.error(f"Missing Y0 data for handle '{handle}' required by CAGR_INTERP.")
            raise ValueError(f"Missing Y0 data for handle '{handle}' in ANALYTIC_KG.")


        try:
            forecast_array = apply_dsl(definition, y0_value=y0_value)
            inputs[handle] = forecast_array
        except Exception as e:
            logger.error(f"Error applying DSL for handle '{handle}': {e}")
            raise RuntimeError(f"Failed to process GIM assumption for {handle}. Error: {e}") from e


    return inputs


def execute_scm(kg, dag, seq, gim):
    """Executes the SCM forecast over the forecast horizon."""


    # 1. Initialize Data Structures
    y0_data = kg.get('core_data', {}).get('Y0_data', {})
    # 'history' stores the full time series data (Y0 + Y1...Y20)
    history = defaultdict(lambda: np.zeros(FORECAST_YEARS + 1))


    # Load Y0 data (at index 0)
    for handle, value in y0_data.items():
        if handle in dag:
            try:
                history[handle][0] = float(value)
            except (TypeError, ValueError):
                history[handle][0] = 0.0


    # 2. Prepare Exogenous Inputs (Apply DSL)
    try:
        exogenous_inputs = prepare_inputs(kg, gim)
    except Exception as e:
        logger.error(f"Failed to prepare exogenous inputs: {e}")
        raise


    # Load exogenous inputs (Y1...Y20)
    for handle, forecast_array in exogenous_inputs.items():
        if handle in dag:
            history[handle][1:] = forecast_array


    # 3. Define Helper Functions (PREV, GET) for use in equations
    # (G3_1.8 Hardening): Robust handling of data access and error conditions.


    def GET(handle, t):
        if handle not in history:
            raise NameError(f"Handle '{handle}' not found during SCM execution (GET).")
        return history[handle][t]


    def PREV(handle, t):
        if t <= 0:
            raise IndexError(f"Cannot access data before Y0 for handle '{handle}' (PREV at t=0). Check ANALYTIC_KG Y0 data.")


        if handle not in history:
            raise NameError(f"Handle '{handle}' not found during SCM execution (PREV).")


        return history[handle][t-1]


    # 4. Execute the Forecast (Time-Step Iteration)
    for t in range(1, FORECAST_YEARS + 1):
        # t represents the current year (Y1 to Y20)


        for handle in seq:
            definition = dag[handle]
            equation_str = definition.get('equation')


            if not equation_str:
                # Node is exogenous or static, already populated.
                continue


            # Execute the equation
            try:
                # Prepare the execution environment
                exec_env = {
                    'GET': lambda h: GET(h, t),
                    'PREV': lambda h: PREV(h, t),
                    'max': max, 'min': min, 'math': math, 'np': np
                }


                # Execute the equation string
                result = eval(equation_str, exec_env)


                # Store the result
                history[handle][t] = float(result)


            except Exception as e:
                logger.error(f"SCM Execution Error at t={t} for handle '{handle}'. Equation: '{equation_str}'. Error: {e}")
                raise RuntimeError(f"Failed to execute equation for {handle} at year {t}. Error: {e}") from e


    # 5. Format Output as DataFrame
    # Return the forecast period (Y1...Y20)
    forecast_data = {handle: data[1:] for handle, data in history.items() if handle in seq}
    index = [f"Y{i+1}" for i in range(FORECAST_YEARS)]
    df = pd.DataFrame(forecast_data, index=index)


    # Ensure columns are in the topologically sorted order
    ordered_cols = [col for col in seq if col in df.columns]
    df = df[ordered_cols]


    return df


# 1.5 APV (Adjusted Present Value) Valuation Engine


def calculate_apv(forecast_df, dr, kg):
    """Calculates the Intrinsic Value Per Share (IVPS) using the APV methodology."""


    # 1. Extract Required Data
    if 'FCF_Unlevered' not in forecast_df.columns or 'ROIC' not in forecast_df.columns or 'NOPAT' not in forecast_df.columns:
         raise ValueError("Forecast DataFrame must contain 'FCF_Unlevered', 'ROIC', and 'NOPAT'.")


    fcf = forecast_df['FCF_Unlevered'].values
    nopat_T = forecast_df['NOPAT'].iloc[-1]


    market_context = kg.get('market_context', {})
    share_data = kg.get('share_data', {})
    core_data = kg.get('core_data', {}).get('Y0_data', {})


    rfr = market_context.get('RFR')
    fdso = share_data.get('FDSO')
    total_debt_y0 = core_data.get('Total_Debt', 0.0)
    excess_cash_y0 = core_data.get('Excess_Cash', 0.0)
    minority_interest_y0 = core_data.get('Minority_Interest', 0.0)


    if fdso is None or fdso <= 0:
        raise ValueError("FDSO must be provided and positive in ANALYTIC_KG.")


    # 2. Calculate PV of Explicit FCF
    discount_factors = np.array([(1 + dr)**-(i+1) for i in range(FORECAST_YEARS)])
    pv_fcf = np.sum(fcf * discount_factors)


    # 3. Determine Terminal Growth (g) and Terminal ROIC (r)
    # We use the Value Driver Formula: TV = NOPAT(T+1) * (1 - g/r) / (DR - g)


    # Terminal ROIC (r): We use the ROIC at Y20, assuming the GIM already models the convergence.
    roic_T = forecast_df['ROIC'].iloc[-1]
    terminal_roic_r = roic_T


    # Terminal Growth (g): Estimated based on NOPAT growth convergence, subject to constraints.
    nopat_growth_rates = forecast_df['NOPAT'].pct_change().values[1:]
    # Use the average growth of the last 3 years to smooth volatility
    terminal_g_estimate = np.mean(nopat_growth_rates[-3:])
    terminal_g = terminal_g_estimate


    # Apply Constraints to Terminal Growth
    if TERMINAL_G_RFR_CAP and rfr is not None:
        if terminal_g > rfr:
            logger.info(f"Capping terminal growth ({terminal_g:.4f}) at RFR ({rfr:.4f}).")
            terminal_g = rfr


    if terminal_g >= dr:
        logger.warning(f"Terminal growth ({terminal_g:.4f}) exceeds DR ({dr:.4f}). Adjusting g to 99% of DR.")
        terminal_g = dr * 0.99


    if terminal_g < 0:
        terminal_g = 0


    # 4. Calculate Terminal Value (TV)
    nopat_T_plus_1 = nopat_T * (1 + terminal_g)


    # Calculate Reinvestment Rate (IR) = g / r
    if abs(terminal_roic_r) > EPSILON:
        reinvestment_rate_terminal = terminal_g / terminal_roic_r
    else:
        reinvestment_rate_terminal = 0


    # Apply constraints to Reinvestment Rate
    if reinvestment_rate_terminal < 0:
        logger.warning(f"Terminal Reinvestment Rate is negative. Assuming rationalization (g=0).")
        terminal_g = 0
        reinvestment_rate_terminal = 0
        nopat_T_plus_1 = nopat_T


    # Value Driver Formula
    numerator = nopat_T_plus_1 * (1 - reinvestment_rate_terminal)
    denominator = dr - terminal_g


    if denominator <= 0: # Should be caught by constraints, but as a safeguard
        raise RuntimeError("APV denominator (DR - g) is non-positive.")


    terminal_value = numerator / denominator


    # 5. Calculate PV of Terminal Value
    pv_terminal_value = terminal_value / ((1 + dr)**FORECAST_YEARS)


    # 6. Calculate Enterprise Value (EV)
    enterprise_value = pv_fcf + pv_terminal_value


    # 7. Calculate Equity Value
    equity_value = enterprise_value - total_debt_y0 + excess_cash_y0 - minority_interest_y0


    # 8. Calculate Intrinsic Value Per Share (IVPS)
    ivps = equity_value / fdso


    # 9. Package Results
    results = {
        "IVPS": ivps,
        "Equity_Value": equity_value,
        "Enterprise_Value": enterprise_value,
        "DR": dr,
        "Terminal_g": terminal_g,
        "Terminal_ROIC_r": terminal_roic_r,
        "FDSO": fdso,
        "Net_Debt": total_debt_y0 - excess_cash_y0
    }
    return results


# ==========================================================================================
# 2. INTERNAL ARTIFACT GENERATORS (Helpers)
# ==========================================================================================


def validate_dag_coverage(kg, dag_artifact):
    """
    Validates that all nodes in the DAG which are present in Y0_data have corresponding entries
    in the `coverage_manifest`
    Also checks that nodes explicitly listed in `coverage_manifest` exist in the DAG.
    """
    y0_data = kg.get('core_data', {}).get('Y0_data', {})
    dag_nodes = set(dag_artifact.get('DAG', {}).keys())
    coverage_manifest = dag_artifact.get('coverage_manifest', {})


    # 1. Check DAG nodes against Y0_data for coverage manifest entry
    missing_coverage = []
    for node in dag_nodes:
        if node in y0_data and node not in coverage_manifest:
            missing_coverage.append(node)


    if missing_coverage:
        raise RuntimeError(
            f"DAG Coverage Warning: The following DAG nodes are present in Y0_data "
            f"but lack an explicit entry in `coverage_manifest`: {', '.join(missing_coverage)}"
        )


    # 2. Check coverage manifest entries against actual DAG nodes
    invalid_coverage_entries = []
    for covered_node in coverage_manifest.keys():
        if covered_node not in dag_nodes:
            invalid_coverage_entries.append(covered_node)


    if invalid_coverage_entries:
        logger.warning(
            f"DAG Coverage Warning: The `coverage_manifest` lists entries for nodes ..."
            f"that do not exist in the DAG: {', '.join(invalid_coverage_entries)}"
        )


def generate_forecast_summary(forecast_df, schema_version=KERNEL_VERSION):
    """Generates a summary of the forecast for internal analysis."""
    summary_data = {}
    key_items = ['Revenue', 'EBIT', 'NOPAT', 'ROIC']


    for item in key_items:
        if item in forecast_df.columns:
            summary_data[item] = forecast_df[item].to_dict()


    if 'Revenue' in forecast_df.columns and 'EBIT' in forecast_df.columns:
            summary_data['EBIT_Margin'] = (forecast_df['EBIT'] / forecast_df['Revenue']).to_dict()


    return {"schema_version": schema_version, "summary_data": summary_data}


# ==========================================================================================
# 3. ANALYSIS MODULES (Multiples, Sensitivity)
# ==========================================================================================


def calculate_implied_multiples(valuation_results, forecast_summary, kg, schema_version=KERNEL_VERSION):
    """Calculates implied valuation multiples based on the IVPS and market price."""


    ivps = valuation_results['IVPS']
    ev_implied = valuation_results['Enterprise_Value']
    fdso = valuation_results['FDSO']
    net_debt = valuation_results['Net_Debt']


    current_price = kg.get('market_context', {}).get('Current_Stock_Price')


    ev_market = None
    if current_price is not None:
        market_cap = current_price * fdso
        ev_market = market_cap + net_debt


    fs = forecast_summary.get('summary_data', {})
    implied_multiples = {}


    # Focus on Y1 multiples for the summary
    year = 'Y1'


    def calculate(num_implied, num_market, den_data, handle):
        if den_data and abs(den_data.get(year, 0)) > EPSILON:
            implied_multiples[f"Implied_{handle}_{year}"] = num_implied / den_data[year]
            if num_market is not None:
                implied_multiples[f"Market_{handle}_{year}"] = num_market / den_data[year]


    calculate(ev_implied, ev_market, fs.get('Revenue'), 'EV_Sales')
    calculate(ev_implied, ev_market, fs.get('EBIT'), 'EV_EBIT')
    calculate(ivps * fdso, (current_price * fdso) if current_price else None, fs.get('NOPAT'), 'P_NOPAT')


    return {
        "schema_version": schema_version,
        "current_market_price": current_price,
        "implied_multiples": implied_multiples
    }


def run_sensitivity_analysis(kg, dag, seq, gim, dr, base_results, scenarios, schema_version=KERNEL_VERSION):
    """Runs sensitivity analysis (Tornado chart) by modifying GIM assumptions or DR."""


    base_ivps = base_results['IVPS']
    tornado_data = []


    # Scenarios structure expected: List of dictionaries {driver, low, high}
    for scenario in scenarios:
        driver = scenario['driver']
        low_change = scenario['low']
        high_change = scenario['high']


        ivps_low = None
        ivps_high = None


        for direction, pct_change in [('low', low_change), ('high', high_change)]:
            temp_gim = copy.deepcopy(gim)
            temp_dr = dr


            try:
                # Modify the input
                if driver == 'Discount_Rate':
                    # Interpret change as absolute basis points change for DR
                    temp_dr += pct_change
                    if temp_dr <= 0.01: raise ValueError("Discount Rate too low.")


                elif driver in temp_gim:
                    # Modify the GIM assumption (apply percentage change to core parameters)
                    mode = temp_gim[driver]['mode']
                    params = temp_gim[driver]['params']


                    def apply_change(value, change):
                        return value * (1 + change)


                    if mode == 'STATIC':
                        params['value'] = apply_change(params['value'], pct_change)
                    elif mode == 'LINEAR_FADE':
                        params['start_value'] = apply_change(params['start_value'], pct_change)
                    elif mode == 'CAGR_INTERP':
                        params['start_cagr'] = apply_change(params['start_cagr'], pct_change)
                        params['end_cagr'] = apply_change(params['end_cagr'], pct_change)


                else:
                    continue


                # Re-run the SCM and APV
                forecast_df = execute_scm(kg, dag, seq, temp_gim)
                valuation_results = calculate_apv(forecast_df, temp_dr, kg)
                scenario_ivps = valuation_results['IVPS']


                if direction == 'low':
                    ivps_low = scenario_ivps
                else:
                    ivps_high = scenario_ivps


            except Exception as e:
                logger.error(f"Error during sensitivity analysis for {driver} ({direction}): {e}")


        # Append to tornado data
        if ivps_low is not None and ivps_high is not None:
            # Ensure ordering (low DR results in high IVPS, etc.)
            if ivps_low > ivps_high:
                 ivps_low, ivps_high = ivps_high, ivps_low


            tornado_data.append({
                "Driver": driver,
                "IVPS_Low": ivps_low,
                "IVPS_High": ivps_high,
                "Impact": ivps_high - ivps_low
            })


    # Sort by impact magnitude
    tornado_data.sort(key=lambda x: abs(x['Impact']), reverse=True)


    return {
        "schema_version": schema_version,
        "base_case_ivps": base_ivps,
        "Tornado_Chart_Data": tornado_data
    }


# ==========================================================================================
# 4. LIGHTWEIGHT SUMMARY GENERATOR (G3_1.8 - The Selective Emission Artifact)
# ==========================================================================================


def generate_lightweight_valuation_summary(valuation_results, forecast_summary, implied_multiples, sensitivity_results, kg, forecast_df, gim, schema_version=KERNEL_VERSION):
    """Generates the LIGHTWEIGHT_VALUATION_SUMMARY (A.7) artifact."""
    v = valuation_results
    fs = forecast_summary.get('summary_data', {})
    im = implied_multiples.get('implied_multiples', {})
    sr = sensitivity_results


    def safe_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None


    # 1. IVPS Summary
    ivps_summary = {
        "IVPS": safe_float(v.get("IVPS")),
        "DR": safe_float(v.get("DR")),
        "Terminal_g": safe_float(v.get("Terminal_g")),
        "ROIC_Terminal": safe_float(v.get("Terminal_ROIC_r")),
        "Current_Market_Price": safe_float(implied_multiples.get("current_market_price"))
    }


    # 2. Implied Multiples Analysis
    implied_multiples_analysis = {
        "Implied_EV_Sales_Y1": im.get("Implied_EV_Sales_Y1"),
        "Implied_EV_EBIT_Y1": im.get("Implied_EV_EBIT_Y1"),
        "Implied_P_NOPAT_Y1": im.get("Implied_P_NOPAT_Y1"),
        "Market_EV_Sales_Y1": im.get("Market_EV_Sales_Y1"),
        "Market_EV_EBIT_Y1": im.get("Market_EV_EBIT_Y1"),
        "Market_P_NOPAT_Y1": im.get("Market_P_NOPAT_Y1")
    }


    # 3. Sensitivity Analysis (Tornado Summary)
    tornado_data = sr.get('Tornado_Chart_Data', [])
    tornado_summary = []
    base_ivps = safe_float(sr.get('base_case_ivps')) or ivps_summary["IVPS"]


    for item in tornado_data[:SENSITIVITY_TORNADO_TOP_N]:
        swing_percent = None
        ivps_low = safe_float(item.get("IVPS_Low"))
        ivps_high = safe_float(item.get("IVPS_High"))


        if base_ivps and abs(base_ivps) > EPSILON and ivps_low is not None and ivps_high is not None:
             swing_percent = (ivps_high - ivps_low) / base_ivps


        tornado_summary.append({
            "Driver_Handle": item.get("Driver"),
            "IVPS_Low": ivps_low,
            "IVPS_High": ivps_high,
            "IVPS_Swing_Percent": swing_percent
        })


    tornado_summary.sort(key=lambda x: abs(x.get("IVPS_Swing_Percent") or 0), reverse=True)


    # 4. Key Forecast Metrics
    revenue_cagr_y1_y5 = None
    if 'Revenue' in forecast_df.columns and len(forecast_df) >= 5:
        try:
            y0_revenue = kg.get('core_data', {}).get('Y0_data', {}).get('Revenue')
            if y0_revenue is not None and y0_revenue > 0:
                y5_revenue = forecast_df['Revenue'].iloc[4]
                revenue_cagr_y1_y5 = (y5_revenue / y0_revenue)**(1/5) - 1
        except Exception as e:
            logger.warning(f"Could not calculate Revenue CAGR Y1-Y5: {e}")


    ebit_margin_y5 = None
    if 'EBIT' in forecast_df.columns and 'Revenue' in forecast_df.columns and len(forecast_df) >= 5:
         rev_y5 = forecast_df['Revenue'].iloc[4]
         if abs(rev_y5) > EPSILON:
            ebit_margin_y5 = forecast_df['EBIT'].iloc[4] / rev_y5


    roic_y5 = None
    if 'ROIC' in forecast_df.columns and len(forecast_df) >= 5:
        roic_y5 = forecast_df['ROIC'].iloc[4]


    key_forecast_metrics = {
        "Revenue_CAGR_Y1_Y5": safe_float(revenue_cagr_y1_y5),
        "EBIT_Margin_Y5": safe_float(ebit_margin_y5),
        "ROIC_Y5": safe_float(roic_y5)
    }


    # 5. Terminal Driver Values (NEW PATCH)
    terminal_drivers = {}
    if gim and not forecast_df.empty:
        for driver in gim.keys():
            if driver in forecast_df.columns:
                # Extract Year 20 (final) value
                terminal_drivers[driver] = safe_float(forecast_df[driver].iloc[-1])
# 6. Forecast Trajectory Checkpoints (G3_1.8)
    # Capture nominal values at Y0, Y5, Y10, Y20 for key drivers (Exogenous and select Endogenous/Financial)


    trajectory_checkpoints = {"Y0": {}, "Y5": {}, "Y10": {}, "Y20": {}}
    y0_data = kg.get('core_data', {}).get('Y0_data', {})


    # Identify drivers to track: All GIM drivers (Exogenous) + Key Financials/Endogenous
    exogenous_drivers = list(gim.keys())
    key_internal_drivers = ['Revenue', 'EBIT', 'NOPAT', 'Invested_Capital', 'ROIC', 'FCF_Unlevered']


    # Robustly add key operational primitives modeled in the DAG
    # We look at columns in the forecast_df that are not exogenous and not the standard financials
    for driver in forecast_df.columns:
        if driver not in exogenous_drivers and driver not in key_internal_drivers:
            # Add the driver if it is not already included, prioritizing those present in Y0 data
             if driver in y0_data or len(key_internal_drivers) < 15: # Limit total internal drivers to keep summary lightweight
                 if driver not in key_internal_drivers:
                    key_internal_drivers.append(driver)


    all_drivers_to_track = exogenous_drivers + key_internal_drivers


    for driver in all_drivers_to_track:
        # Y0
        if driver in y0_data:
            trajectory_checkpoints["Y0"][driver] = safe_float(y0_data[driver])


        # Forecast Years (Y5, Y10, Y20)
        if driver in forecast_df.columns:
            if len(forecast_df) >= 5:
                trajectory_checkpoints["Y5"][driver] = safe_float(forecast_df[driver].iloc[4]) # Y5 is index 4
            if len(forecast_df) >= 10:
                trajectory_checkpoints["Y10"][driver] = safe_float(forecast_df[driver].iloc[9]) # Y10 is index 9
            if len(forecast_df) >= 20:
                # Use index 19 (iloc[-1]) for Y20 assuming FORECAST_YEARS=20
                trajectory_checkpoints["Y20"][driver] = safe_float(forecast_df[driver].iloc[-1])




    return {
        "schema_version": schema_version,
        "ivps_summary": ivps_summary,
        "implied_multiples_analysis": implied_multiples_analysis,
        "sensitivity_analysis": {
            "tornado_summary": tornado_summary
        },
        "key_forecast_metrics": key_forecast_metrics,
        "terminal_drivers": terminal_drivers,
        "forecast_trajectory_checkpoints": trajectory_checkpoints # G3_1.8
    }




# ==========================================================================================
# 5. WORKFLOW ORCHESTRATOR (Main API) (Updated for G3_1.8)
# ==========================================================================================


def execute_cvr_workflow(kg, dag_artifact, gim_artifact, dr_trace, sensitivity_scenarios=None, valuation_date=None):
    """
    The main API for the CVR Kernel (G3_2.2.1e).
    Implements Selective Emission: Returns ONLY the LightweightValuationSummary (A.7).
    """
    print(f"CVR Kernel Execution Started (Version: {KERNEL_VERSION})... [MRC Mode]")


    schema_version = KERNEL_VERSION


# Extract structures from artifacts
    dag = dag_artifact.get('DAG', {})
    gim = gim_artifact.get('GIM', {})


    # 0.5 Validate DAG Coverage
    print("Validating DAG coverage against Y0_data")
    try:
        validate_dag_coverage(kg, dag_artifact)
    except RuntimeError as e:
        logger.error(f"DAG Coverage Validation Failed: {e}")
        raise


    # 1. Derive Execution Sequence (Topological Sort)
    print("Deriving SCM execution sequence...")


    try:
        seq = topological_sort(dag)
    except Exception as e:
        logger.error(f"Topological Sort Failed: {e}")
        raise


    # 2. Extract DR
    try:
        dr = float(dr_trace['derivation_trace']['DR_Static'])
    except (KeyError, TypeError, ValueError):
        raise RuntimeError("Failed to parse DR from DR_DERIVATION_TRACE.")


    # 3. Execute SCM Forecast
    print(f"Executing {FORECAST_YEARS}-Year SCM Forecast...")
    try:
        forecast_df = execute_scm(kg, dag, seq, gim)
    except Exception as e:
        logger.error(f"SCM Execution Failed: {e}")
        raise


    # 4. Execute APV Valuation
    print("Executing APV Valuation...")
    try:
        valuation_results = calculate_apv(forecast_df, dr, kg)
    except Exception as e:
        logger.error(f"APV Valuation Failed: {e}")
        raise


    # 5. Generate Internal Artifacts
    print("Generating Internal Summary Artifacts...")
    try:
        forecast_summary = generate_forecast_summary(forecast_df, schema_version)
    except Exception as e:
        logger.error(f"Forecast Summary Generation Failed: {e}")
        raise


    # 6. Calculate Implied Multiples
    print("Calculating Implied Multiples Analysis...")
    try:
        implied_multiples = calculate_implied_multiples(valuation_results, forecast_summary, kg, schema_version)
    except Exception as e:
        logger.warning(f"Implied Multiples Analysis Failed: {e}")
        implied_multiples = {}


    # 7. Execute Sensitivity Analysis
    sensitivity_results = {}
    if sensitivity_scenarios:
        print("Executing Sensitivity Analysis...")
        try:
            # Note: Sensitivity scenarios are expected to be a list of {driver, low, high} definitions.
            sensitivity_results = run_sensitivity_analysis(kg, dag, seq, gim, dr, valuation_results, sensitivity_scenarios, schema_version)
        except Exception as e:
            logger.warning(f"Sensitivity Analysis Failed: {e}")
            sensitivity_results = {}


    # 8. Generate Lightweight Summary (The Selective Emission)
    print("Generating Lightweight Valuation Summary (A.7)...")
    try:
        lightweight_summary = generate_lightweight_valuation_summary(
            valuation_results,
            forecast_summary,
            implied_multiples,
            sensitivity_results,
            kg,
            forecast_df,
            gim, # PASSED HERE IN PATCH
            schema_version
        )
    except Exception as e:
        logger.error(f"Lightweight Summary Generation Failed: {e}")
        raise


    print("CVR Kernel Execution Completed.")
    return lightweight_summary