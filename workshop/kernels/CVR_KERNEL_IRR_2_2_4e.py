# ==========================================================================================
# CVR KERNEL G3_2.2.4e_IRR (Consolidated: ENRICHMENT + SCENARIO + IRR)
# ==========================================================================================
# This consolidated kernel contains all modules required for IRR execution:
# - G3_2.2E ENRICHMENT base (DSL, SCM, APV engines)
# - G3_2.2S SCENARIO extension (SSE, JPD, interventions)
# - G3_2.2.4e IRR extension (TF methodology, CR layering, fork generation)
#
# T2 EXECUTION: Import and call execute_irr_workflow() with A.13 inputs.
# ==========================================================================================


import numpy as np
import pandas as pd
import json
import math
from collections import deque, defaultdict
import re
import copy
import logging


# ==========================================================================================
# CONFIGURATION
# ==========================================================================================


FORECAST_YEARS = 20
EPSILON = 1e-9
KERNEL_VERSION = "G3_2.2.4e_IRR"
SENSITIVITY_TORNADO_TOP_N = 5
TERMINAL_G_RFR_CAP = True  # If True, Terminal g is capped at RFR


# Configure Logging (Minimal for production)
logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ==========================================================================================
# 1. CORE ENGINES (DSL, SCM, APV)
# ==========================================================================================


# ------------------------------------------------------------------------------
# 1.1 Assumption DSL (Domain Specific Language) Engine
# Extended with S_CURVE and MULTI_STAGE_FADE modes for ENRICHMENT
# ------------------------------------------------------------------------------


def apply_dsl(dsl, y0_value=None, forecast_years=FORECAST_YEARS):
    """
    Applies the DSL definition to generate a forecast array.


    Supported Modes:
    - STATIC: Constant value
    - LINEAR_FADE: Linear interpolation to target
    - CAGR_INTERP: Compounding growth rate that fades
    - S_CURVE: Logistic function for adoption/penetration dynamics
    - MULTI_STAGE_FADE: Multiple distinct phases with different targets
    - EXPLICIT_SCHEDULE: Manual year-by-year specification
    """
    mode = dsl.get('mode')
    params = dsl.get('params', {})
    forecast = np.zeros(forecast_years)


    # -------------------------------------------------------------------------
    # MODE: STATIC
    # -------------------------------------------------------------------------
    if mode == 'STATIC':
        value = float(params.get('value', 0))
        forecast.fill(value)


    # -------------------------------------------------------------------------
    # MODE: LINEAR_FADE
    # -------------------------------------------------------------------------
    elif mode == 'LINEAR_FADE':
        start_value = float(params.get('start_value', y0_value if y0_value is not None else 0))
        end_value = float(params.get('end_value'))
        fade_years = int(params.get('fade_years'))


        if fade_years > forecast_years:
            fade_years = forecast_years


        if fade_years > 0:
            fade_steps = np.linspace(start_value, end_value, fade_years + 1)[1:]  # Exclude start, include end
            forecast[:fade_years] = fade_steps


        if fade_years < forecast_years:
            forecast[fade_years:] = end_value


    # -------------------------------------------------------------------------
    # MODE: CAGR_INTERP
    # -------------------------------------------------------------------------
    elif mode == 'CAGR_INTERP':
        if y0_value is None:
            raise ValueError("CAGR_INTERP requires a valid y0_value from ANALYTIC_KG.")


        start_cagr = float(params.get('start_cagr'))
        end_cagr = float(params.get('end_cagr'))
        interp_years = int(params.get('interp_years'))


        if interp_years > forecast_years:
            interp_years = forecast_years


        # Generate the CAGR time series (linear fade of growth rate)
        cagr_series = np.zeros(forecast_years)
        if interp_years > 0:
            cagr_steps = np.linspace(start_cagr, end_cagr, interp_years + 1)[1:]  # Y1 to Y_interp
            cagr_series[:interp_years] = cagr_steps


        if interp_years < forecast_years:
            cagr_series[interp_years:] = end_cagr


        # Apply the CAGR series to compound from Y0
        current_value = y0_value
        for i in range(forecast_years):
            current_value *= (1 + cagr_series[i])
            forecast[i] = current_value


    # -------------------------------------------------------------------------
    # MODE: S_CURVE (Logistic Function) - NEW FOR ENRICHMENT
    # -------------------------------------------------------------------------
    elif mode == 'S_CURVE':
        start_value = float(params.get('start_value', y0_value if y0_value is not None else 0))
        saturation_value = float(params.get('saturation_value'))
        inflection_year = float(params.get('inflection_year'))
        steepness = float(params.get('steepness', 0.5))


        # Logistic function: value(t) = start + (saturation - start) / (1 + exp(-k*(t - t0)))
        # Where k = steepness, t0 = inflection_year


        for i in range(forecast_years):
            t = i + 1  # Year 1 to Year 20
            exponent = -steepness * (t - inflection_year)


            # Prevent overflow in exp
            if exponent > 700:
                logistic_factor = 0.0
            elif exponent < -700:
                logistic_factor = 1.0
            else:
                logistic_factor = 1.0 / (1.0 + math.exp(exponent))


            forecast[i] = start_value + (saturation_value - start_value) * logistic_factor


    # -------------------------------------------------------------------------
    # MODE: MULTI_STAGE_FADE - NEW FOR ENRICHMENT
    # -------------------------------------------------------------------------
    elif mode == 'MULTI_STAGE_FADE':
        stages = params.get('stages', [])


        if not stages:
            raise ValueError("MULTI_STAGE_FADE requires at least one stage definition.")


        # Sort stages by end_year
        stages = sorted(stages, key=lambda s: s['end_year'])


        # Determine starting value
        current_value = float(params.get('start_value', y0_value if y0_value is not None else 0))
        current_year = 0  # Start from Y0


        for stage in stages:
            end_year = int(stage['end_year'])
            end_value = float(stage['end_value'])
            interpolation = stage.get('interpolation', 'LINEAR').upper()


            # Clamp end_year to forecast horizon
            if end_year > forecast_years:
                end_year = forecast_years


            stage_years = end_year - current_year


            if stage_years <= 0:
                continue


            # Generate values for this stage
            if interpolation == 'LINEAR':
                stage_values = np.linspace(current_value, end_value, stage_years + 1)[1:]
            elif interpolation == 'CAGR':
                # Compound growth from current to end
                if current_value > 0 and end_value > 0:
                    stage_cagr = (end_value / current_value) ** (1 / stage_years) - 1
                    stage_values = np.array([
                        current_value * ((1 + stage_cagr) ** (j + 1))
                        for j in range(stage_years)
                    ])
                else:
                    # Fallback to linear if values are non-positive
                    stage_values = np.linspace(current_value, end_value, stage_years + 1)[1:]
            else:
                # Default to linear
                stage_values = np.linspace(current_value, end_value, stage_years + 1)[1:]


            # Fill forecast array
            start_idx = current_year
            end_idx = min(current_year + stage_years, forecast_years)
            forecast[start_idx:end_idx] = stage_values[:end_idx - start_idx]


            # Update for next stage
            current_value = end_value
            current_year = end_year


            if current_year >= forecast_years:
                break


        # Fill remaining years with last value
        if current_year < forecast_years:
            forecast[current_year:] = current_value


    # -------------------------------------------------------------------------
    # MODE: EXPLICIT_SCHEDULE
    # -------------------------------------------------------------------------
    elif mode == 'EXPLICIT_SCHEDULE':
        schedule = params.get('schedule', {})
        sorted_years = sorted([int(y) for y in schedule.keys()])


        if not sorted_years:
            return forecast


        # Initial fill before first specified year
        start_year = sorted_years[0]
        start_value = float(schedule[str(start_year)])
        if start_year > 1:
            forecast[:start_year - 1] = start_value


        # Process each specified year and interpolate gaps
        for i in range(len(sorted_years)):
            year = sorted_years[i]
            value = float(schedule[str(year)])
            idx = year - 1  # Convert to 0-indexed


            if idx < forecast_years:
                forecast[idx] = value


            # Interpolate to next specified year
            if i + 1 < len(sorted_years):
                next_year = sorted_years[i + 1]
                next_value = float(schedule[str(next_year)])
                next_idx = next_year - 1


                if next_year > year + 1:
                    gap_years = next_year - year
                    interp_steps = np.linspace(value, next_value, gap_years + 1)


                    start_fill_idx = idx + 1
                    end_fill_idx = min(next_idx, forecast_years)


                    if start_fill_idx < forecast_years:
                        fill_len = end_fill_idx - start_fill_idx
                        forecast[start_fill_idx:end_fill_idx] = interp_steps[1:1 + fill_len]


        # Hold last value through end of forecast
        last_defined_year = sorted_years[-1]
        if last_defined_year < forecast_years:
            last_value = float(schedule[str(last_defined_year)])
            forecast[last_defined_year:] = last_value


    # -------------------------------------------------------------------------
    # UNKNOWN MODE
    # -------------------------------------------------------------------------
    else:
        raise ValueError(f"Unknown DSL mode: {mode}. Supported: STATIC, LINEAR_FADE, CAGR_INTERP, S_CURVE, MULTI_STAGE_FADE, EXPLICIT_SCHEDULE")


    return forecast


# ------------------------------------------------------------------------------
# 1.2 SCM (Structural Causal Model) Engine
# ------------------------------------------------------------------------------


def topological_sort(dag):
    """
    Performs a topological sort on the DAG.
    Ensures only intra-timestep dependencies (GET calls) are considered for ordering.
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
            # Filter out PREV references in parent list
            if parent.startswith('PREV('):
                continue
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
        raise RuntimeError(f"Cycle detected in DAG. Check nodes for circular dependencies (use PREV for lagged): {cycle_nodes}")


    return sorted_list


def validate_dag_coverage(kg, dag_artifact):
    """
    Validates that all Y0_data metrics are accounted for in the DAG (P5 Doctrine).
    Either they map to a node, are derivatives, or are explicitly excluded.
    """
    y0_data = kg.get('core_data', {}).get('Y0_data', {})
    dag = dag_artifact.get('DAG', {})
    coverage_manifest = dag_artifact.get('coverage_manifest', {}).get('Y0_data_coverage', {})


    dag_nodes = set(dag.keys())
    missing_metrics = []


    for metric in y0_data.keys():
        # Check if metric is in DAG
        if metric in dag_nodes:
            continue
        # Check if metric is documented in coverage manifest
        if metric in coverage_manifest:
            continue
        # Metric is unaccounted
        missing_metrics.append(metric)


    if missing_metrics:
        logger.warning(f"P5 Warning: Y0_data metrics not explicitly dispositioned in DAG: {missing_metrics}")
        # For ENRICHMENT, we issue a warning rather than failing
        # since DAG may have been enriched


def prepare_inputs(kg, gim):
    """Prepares inputs by applying the DSL to generate forecast arrays for exogenous drivers."""
    inputs = {}
    y0_data = kg.get('core_data', {}).get('Y0_data', {})


    for handle, definition in gim.items():
        y0_value = y0_data.get(handle)


        # CAGR_INTERP requires Y0 value
        if definition.get('mode') == 'CAGR_INTERP' and y0_value is None:
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
    def GET(handle, t):
        if handle not in history:
            raise NameError(f"Handle '{handle}' not found during SCM execution (GET).")
        return history[handle][t]


    def PREV(handle, t):
        if t <= 0:
            raise IndexError(f"Cannot access data before Y0 for handle '{handle}' (PREV at t=0).")
        if handle not in history:
            raise NameError(f"Handle '{handle}' not found during SCM execution (PREV).")
        return history[handle][t - 1]


    # 4. Execute the Forecast (Time-Step Iteration)
    for t in range(1, FORECAST_YEARS + 1):
        for handle in seq:
            definition = dag[handle]
            equation_str = definition.get('equation')


            if not equation_str:
                # Node is exogenous or static, already populated
                continue


            # Execute the equation
            try:
                exec_env = {
                    'GET': lambda h: GET(h, t),
                    'PREV': lambda h: PREV(h, t),
                    'MAX': max, 'MIN': min, 'ABS': abs,
                    'max': max, 'min': min, 'abs': abs,
                    'math': math, 'np': np
                }


                result = eval(equation_str, exec_env)
                history[handle][t] = float(result)


            except Exception as e:
                logger.error(f"SCM Execution Error at t={t} for handle '{handle}'. Equation: '{equation_str}'. Error: {e}")
                raise RuntimeError(f"Failed to execute equation for {handle} at year {t}. Error: {e}") from e


    # 5. Format Output as DataFrame (Y1...Y20)
    forecast_data = {handle: data[1:] for handle, data in history.items() if handle in seq}
    index = [f"Y{i + 1}" for i in range(FORECAST_YEARS)]
    df = pd.DataFrame(forecast_data, index=index)


    # Ensure columns are in topologically sorted order
    ordered_cols = [col for col in seq if col in df.columns]
    df = df[ordered_cols]


    return df


# ------------------------------------------------------------------------------
# 1.3 APV (Adjusted Present Value) Valuation Engine
# ------------------------------------------------------------------------------


def calculate_apv(forecast_df, dr, kg):
    """Calculates the Intrinsic Value Per Share (IVPS) using the APV methodology."""


    # 1. Validate Required Columns
    required_cols = ['FCF_Unlevered', 'ROIC', 'NOPAT']
    for col in required_cols:
        if col not in forecast_df.columns:
            raise ValueError(f"Forecast DataFrame must contain '{col}'.")


    fcf = forecast_df['FCF_Unlevered'].values
    nopat_T = forecast_df['NOPAT'].iloc[-1]


    # 2. Extract KG Data
    market_context = kg.get('market_context', {})
    share_data = kg.get('share_data', {})
    core_data = kg.get('core_data', {}).get('Y0_data', {})


    rfr = market_context.get('RFR')
    fdso = share_data.get('shares_out_diluted_tsm') or share_data.get('FDSO')


    # Capital structure for equity bridge
    capital_structure = kg.get('capital_structure', {}).get('net_debt_y0', {})
    if capital_structure:
        total_debt_y0 = capital_structure.get('gross_debt', 0.0)
        excess_cash_y0 = capital_structure.get('cash_equivalents', 0.0)
    else:
        total_debt_y0 = core_data.get('Total_Debt', 0.0)
        excess_cash_y0 = core_data.get('Excess_Cash', 0.0)


    minority_interest_y0 = core_data.get('Minority_Interest', 0.0)


    if fdso is None or fdso <= 0:
        raise ValueError("FDSO/shares_out_diluted_tsm must be provided and positive in ANALYTIC_KG.")


    # 3. Calculate PV of Explicit FCF
    discount_factors = np.array([(1 + dr) ** -(i + 1) for i in range(FORECAST_YEARS)])
    pv_fcf = np.sum(fcf * discount_factors)


    # 4. Determine Terminal Growth (g) and Terminal ROIC (r)
    roic_T = forecast_df['ROIC'].iloc[-1]
    terminal_roic_r = roic_T


    # Estimate terminal growth from NOPAT trajectory
    nopat_growth_rates = forecast_df['NOPAT'].pct_change().values[1:]
    terminal_g_estimate = np.mean(nopat_growth_rates[-3:])  # Average of last 3 years
    terminal_g = terminal_g_estimate


    # Apply Constraints
    if TERMINAL_G_RFR_CAP and rfr is not None:
        if terminal_g > rfr:
            logger.info(f"Capping terminal growth ({terminal_g:.4f}) at RFR ({rfr:.4f}).")
            terminal_g = rfr


    if terminal_g >= dr:
        logger.warning(f"Terminal growth ({terminal_g:.4f}) >= DR ({dr:.4f}). Adjusting g to 99% of DR.")
        terminal_g = dr * 0.99


    if terminal_g < 0:
        terminal_g = 0


    # 5. Calculate Terminal Value (Value Driver Formula)
    nopat_T_plus_1 = nopat_T * (1 + terminal_g)


    if abs(terminal_roic_r) > EPSILON:
        reinvestment_rate_terminal = terminal_g / terminal_roic_r
    else:
        reinvestment_rate_terminal = 0


    if reinvestment_rate_terminal < 0:
        logger.warning("Terminal Reinvestment Rate is negative. Assuming g=0.")
        terminal_g = 0
        reinvestment_rate_terminal = 0
        nopat_T_plus_1 = nopat_T


    numerator = nopat_T_plus_1 * (1 - reinvestment_rate_terminal)
    denominator = dr - terminal_g


    if denominator <= 0:
        raise RuntimeError(f"APV denominator (DR - g) is non-positive. DR={dr}, g={terminal_g}")


    terminal_value = numerator / denominator


    # 6. Calculate PV of Terminal Value
    pv_terminal_value = terminal_value / ((1 + dr) ** FORECAST_YEARS)


    # 7. Calculate Enterprise Value
    enterprise_value = pv_fcf + pv_terminal_value


    # 8. Calculate Equity Value
    net_debt = total_debt_y0 - excess_cash_y0
    equity_value = enterprise_value - net_debt - minority_interest_y0


    # 9. Calculate IVPS
    ivps = equity_value / fdso


    # 10. Package Results
    results = {
        "IVPS": ivps,
        "Equity_Value": equity_value,
        "Enterprise_Value": enterprise_value,
        "DR": dr,
        "Terminal_g": terminal_g,
        "Terminal_ROIC_r": terminal_roic_r,
        "Terminal_RR": reinvestment_rate_terminal,
        "FDSO": fdso,
        "Net_Debt": net_debt,
        "PV_Explicit_FCF": pv_fcf,
        "PV_Terminal_Value": pv_terminal_value
    }
    return results


# ==========================================================================================
# 2. INTERNAL ARTIFACT GENERATORS
# ==========================================================================================


def generate_forecast_summary(forecast_df, schema_version=KERNEL_VERSION):
    """Generates a summary of the forecast for internal analysis."""
    summary_data = {}
    key_items = ['Revenue', 'EBIT', 'NOPAT', 'ROIC', 'FCF_Unlevered', 'Invested_Capital']


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
    """
    Runs sensitivity analysis (Tornado chart) by modifying GIM assumptions or DR.
    Extended for S_CURVE and MULTI_STAGE_FADE modes.
    """


    base_ivps = base_results['IVPS']
    tornado_data = []


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
                    temp_dr += pct_change
                    if temp_dr <= 0.01:
                        raise ValueError("Discount Rate too low.")


                elif driver in temp_gim:
                    mode = temp_gim[driver].get('mode')
                    params = temp_gim[driver].get('params', {})


                    def apply_change(value, change):
                        return value * (1 + change)


                    # Apply percentage change based on mode
                    if mode == 'STATIC':
                        params['value'] = apply_change(params['value'], pct_change)


                    elif mode == 'LINEAR_FADE':
                        if 'start_value' in params:
                            params['start_value'] = apply_change(params['start_value'], pct_change)
                        params['end_value'] = apply_change(params['end_value'], pct_change)


                    elif mode == 'CAGR_INTERP':
                        params['start_cagr'] = apply_change(params['start_cagr'], pct_change)
                        params['end_cagr'] = apply_change(params['end_cagr'], pct_change)


                    elif mode == 'S_CURVE':
                        # Adjust the saturation value (the target ceiling/floor)
                        params['saturation_value'] = apply_change(params['saturation_value'], pct_change)


                    elif mode == 'MULTI_STAGE_FADE':
                        # Adjust all stage end_values proportionally
                        if 'stages' in params:
                            for stage in params['stages']:
                                stage['end_value'] = apply_change(stage['end_value'], pct_change)


                    elif mode == 'EXPLICIT_SCHEDULE':
                        # Adjust all scheduled values
                        if 'schedule' in params:
                            for year_key in params['schedule']:
                                params['schedule'][year_key] = apply_change(
                                    params['schedule'][year_key], pct_change
                                )


                    temp_gim[driver]['params'] = params


                else:
                    # Driver not found in GIM
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
                logger.warning(f"Sensitivity analysis error for {driver} ({direction}): {e}")


        # Append to tornado data if both scenarios succeeded
        if ivps_low is not None and ivps_high is not None:
            # Ensure proper ordering (low input -> low IVPS for most drivers)
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
# 4. LIGHTWEIGHT SUMMARY GENERATOR (The Selective Emission Artifact)
# ==========================================================================================


def generate_lightweight_valuation_summary(
    valuation_results, 
    forecast_summary, 
    implied_multiples, 
    sensitivity_results, 
    kg, 
    forecast_df, 
    gim, 
    schema_version=KERNEL_VERSION
):
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
    tornado_data = sr.get('Tornado_Chart_Data', []) if sr else []
    tornado_summary = []
    base_ivps = safe_float(sr.get('base_case_ivps')) if sr else ivps_summary["IVPS"]


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
                revenue_cagr_y1_y5 = (y5_revenue / y0_revenue) ** (1 / 5) - 1
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


    # 5. Terminal Driver Values
    terminal_drivers = {
        "Terminal_ROIC": safe_float(v.get("Terminal_ROIC_r")),
        "Terminal_RR": safe_float(v.get("Terminal_RR")),
        "Terminal_g": safe_float(v.get("Terminal_g"))
    }


    # Add GIM driver terminal values
    if gim and not forecast_df.empty:
        for driver in gim.keys():
            if driver in forecast_df.columns:
                terminal_drivers[driver] = safe_float(forecast_df[driver].iloc[-1])


    # 6. Forecast Trajectory Checkpoints
    trajectory_checkpoints = {"Y0": {}, "Y5": {}, "Y10": {}, "Y20": {}}
    y0_data = kg.get('core_data', {}).get('Y0_data', {})


    exogenous_drivers = list(gim.keys()) if gim else []
    key_internal_drivers = ['Revenue', 'EBIT', 'NOPAT', 'Invested_Capital', 'ROIC', 'FCF_Unlevered']


    # Add additional tracked drivers from forecast
    for driver in forecast_df.columns:
        if driver not in exogenous_drivers and driver not in key_internal_drivers:
            if driver in y0_data or len(key_internal_drivers) < 15:
                if driver not in key_internal_drivers:
                    key_internal_drivers.append(driver)


    all_drivers_to_track = exogenous_drivers + key_internal_drivers


    for driver in all_drivers_to_track:
        # Y0
        if driver in y0_data:
            trajectory_checkpoints["Y0"][driver] = safe_float(y0_data[driver])


        # Forecast Years
        if driver in forecast_df.columns:
            if len(forecast_df) >= 5:
                trajectory_checkpoints["Y5"][driver] = safe_float(forecast_df[driver].iloc[4])
            if len(forecast_df) >= 10:
                trajectory_checkpoints["Y10"][driver] = safe_float(forecast_df[driver].iloc[9])
            if len(forecast_df) >= 20:
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
        "forecast_trajectory_checkpoints": trajectory_checkpoints
    }


# ==========================================================================================
# 5. WORKFLOW ORCHESTRATOR (Main API)
# ==========================================================================================


def execute_cvr_workflow(kg, dag_artifact, gim_artifact, dr_trace, sensitivity_scenarios=None):
    """
    The main API for the CVR Kernel G3_2.2E (ENRICHMENT).
    Implements Selective Emission: Returns ONLY the LightweightValuationSummary (A.7).


    Parameters:
    -----------
    kg : dict
        A.2_ANALYTIC_KG artifact
    dag_artifact : dict
        A.3_CAUSAL_DAG artifact (with 'DAG' key containing node definitions)
    gim_artifact : dict
        A.5_GESTALT_IMPACT_MAP artifact (with 'GIM' key containing driver assumptions)
    dr_trace : dict
        A.6_DR_DERIVATION_TRACE artifact
    sensitivity_scenarios : list, optional
        List of sensitivity scenario definitions: [{'driver': str, 'low': float, 'high': float}]


    Returns:
    --------
    dict
        A.7_LIGHTWEIGHT_VALUATION_SUMMARY artifact
    """
    print(f"CVR Kernel Execution Started (Version: {KERNEL_VERSION})... [ENRICHMENT Mode]")


    schema_version = KERNEL_VERSION


    # Extract structures from artifacts
    dag = dag_artifact.get('DAG', {})
    gim = gim_artifact.get('GIM', {})


    # 0.5 Validate DAG Coverage (P5 - Warning only for ENRICHMENT)
    print("Validating DAG coverage against Y0_data (P5 Doctrine)...")
    try:
        validate_dag_coverage(kg, dag_artifact)
    except Exception as e:
        logger.warning(f"DAG Coverage Validation Warning: {e}")


    # 1. Derive Execution Sequence (Topological Sort)
    print("Deriving SCM execution sequence...")
    try:
        seq = topological_sort(dag)
    except Exception as e:
        logger.error(f"Topological Sort Failed: {e}")
        raise


    # 2. Extract DR from trace
    try:
        dr_data = dr_trace.get('derivation_trace', {})
        dr = float(dr_data.get('DR_Static'))
    except (KeyError, TypeError, ValueError) as e:
        raise RuntimeError(f"Failed to parse DR from DR_DERIVATION_TRACE: {e}")


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
        implied_multiples = calculate_implied_multiples(
            valuation_results, forecast_summary, kg, schema_version
        )
    except Exception as e:
        logger.warning(f"Implied Multiples Analysis Failed: {e}")
        implied_multiples = {"implied_multiples": {}}


    # 7. Execute Sensitivity Analysis
    sensitivity_results = {}
    if sensitivity_scenarios:
        print("Executing Sensitivity Analysis...")
        try:
            sensitivity_results = run_sensitivity_analysis(
                kg, dag, seq, gim, dr, valuation_results, sensitivity_scenarios, schema_version
            )
        except Exception as e:
            logger.warning(f"Sensitivity Analysis Failed: {e}")
            sensitivity_results = {"Tornado_Chart_Data": []}


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
            gim,
            schema_version
        )
    except Exception as e:
        logger.error(f"Lightweight Summary Generation Failed: {e}")
        raise


    print("CVR Kernel Execution Completed.")
    return lightweight_summary


# ==========================================================================================
# END OF ENRICHMENT MODULE (DSL, SCM, APV)
# ==========================================================================================


# ==========================================================================================
# SCENARIO EXTENSION MODULE (SSE, JPD, Interventions)
# ==========================================================================================
# 
# This module extends the kernel with scenario modeling and SSE integration.
# Insert this code AFTER the existing G3_2.2E kernel functions.
#
# Dependencies: numpy, pandas, copy, math, itertools (add itertools to imports)
# ==========================================================================================


from itertools import product
import copy
import math


# Update kernel version (modify existing constant)
# KERNEL_VERSION = "G3_2.2S"


# ==========================================================================================
# 1. INTERVENTION APPLICATION FUNCTIONS
# ==========================================================================================


def apply_gim_overlay(base_gim, gim_overlay):
    """
    Applies a GIM overlay to the base GIM, creating a scenario-modified GIM.


    The overlay contains only the drivers that differ from the base case.
    Drivers not in the overlay retain their base case values.


    Parameters:
    -----------
    base_gim : dict
        The base case GIM artifact (A.5) with structure {'GIM': {...}}
    gim_overlay : dict
        Dictionary of modified drivers: {driver_handle: new_assumption_dict}


    Returns:
    --------
    dict : Modified GIM artifact
    """
    # Deep copy to avoid mutating the base
    modified_gim = copy.deepcopy(base_gim)


    # Get the GIM dict (handle both {'GIM': {...}} and direct dict formats)
    if 'GIM' in modified_gim:
        gim_dict = modified_gim['GIM']
    else:
        gim_dict = modified_gim


    # Apply overlay
    if gim_overlay:
        for driver_handle, new_assumption in gim_overlay.items():
            if driver_handle in gim_dict:
                # Update existing driver
                gim_dict[driver_handle]['assumption'] = new_assumption
            else:
                # Add new driver (for structural additions that need GIM entries)
                gim_dict[driver_handle] = {
                    'assumption': new_assumption,
                    'source': 'SCENARIO_OVERLAY'
                }


    return modified_gim


def apply_structural_modifications(base_dag, modifications):
    """
    Applies structural modifications to the DAG for structural/hybrid interventions.


    Parameters:
    -----------
    base_dag : dict
        The base case CAUSAL_DAG artifact (A.3)
    modifications : list
        List of modification specifications:
        [
            {
                'modification_type': 'ADD_NODE' | 'REMOVE_NODE' | 'MODIFY_EQUATION' | 'ADD_EDGE',
                'target_node': str,
                'details': {
                    'new_equation': str (for MODIFY_EQUATION),
                    'new_edges': list (for ADD_EDGE),
                    'node_definition': dict (for ADD_NODE)
                }
            }
        ]


    Returns:
    --------
    dict : Modified DAG artifact
    """
    modified_dag = copy.deepcopy(base_dag)


    # Get the DAG structure
    if 'DAG' in modified_dag:
        dag_struct = modified_dag['DAG']
    else:
        dag_struct = modified_dag


    # Ensure required sub-structures exist
    if 'nodes' not in dag_struct:
        dag_struct['nodes'] = {}
    if 'edges' not in dag_struct:
        dag_struct['edges'] = {}
    if 'equations' not in dag_struct:
        dag_struct['equations'] = {}


    for mod in modifications or []:
        mod_type = mod.get('modification_type', mod.get('type'))
        target = mod.get('target_node')
        details = mod.get('details', {})


        if mod_type == 'ADD_NODE':
            # Add a new node to the DAG
            node_def = details.get('node_definition', {})
            dag_struct['nodes'][target] = node_def
            # Add edges if specified
            if 'new_edges' in details:
                dag_struct['edges'][target] = details['new_edges']
            else:
                dag_struct['edges'][target] = []
            # Add equation if specified
            if 'new_equation' in details:
                dag_struct['equations'][target] = details['new_equation']


        elif mod_type == 'REMOVE_NODE':
            # Remove a node (use with caution - may break dependencies)
            if target in dag_struct['nodes']:
                del dag_struct['nodes'][target]
            if target in dag_struct['edges']:
                del dag_struct['edges'][target]
            if target in dag_struct['equations']:
                del dag_struct['equations'][target]


        elif mod_type == 'MODIFY_EQUATION':
            # Modify an existing equation
            if 'new_equation' in details:
                dag_struct['equations'][target] = details['new_equation']


        elif mod_type == 'ADD_EDGE':
            # Add edges to an existing node
            if target in dag_struct['edges']:
                dag_struct['edges'][target].extend(details.get('new_edges', []))
            else:
                dag_struct['edges'][target] = details.get('new_edges', [])


    return modified_dag


# ==========================================================================================
# 2. SCENARIO INTERVENTION EXECUTION
# ==========================================================================================


def execute_scenario_intervention(kg, dag, gim, dr_trace, intervention_def, dr_override=None):
    """
    Executes a single scenario intervention and returns the deterministic IVPS.


    This function applies the intervention to the base case artifacts, executes
    the SCM forecast, calculates APV valuation, and validates P2 constraints.


    Parameters:
    -----------
    kg : dict
        A.2_ANALYTIC_KG artifact (base case)
    dag : dict
        A.3_CAUSAL_DAG artifact (base case)
    gim : dict
        A.5_GESTALT_IMPACT_MAP artifact (base case)
    dr_trace : dict
        A.6_DR_DERIVATION_TRACE artifact
    intervention_def : dict
        Intervention specification:
        {
            'gim_overlay': dict | None,
            'structural_modifications': list | None
        }
    dr_override : float, optional
        Scenario-specific discount rate (overrides dr_trace if provided)


    Returns:
    --------
    dict : {
        'ivps_scenario': float,
        'ivps_base': float,
        'ivps_impact': float,
        'terminal_g': float,
        'terminal_roic': float,
        'terminal_rr': float,
        'dr_used': float,
        'p2_status': 'PASS' | 'FAIL',
        'p2_message': str,
        'forecast_df': DataFrame (for debugging, optional)
    }
    """


    # 1. Apply GIM overlay
    gim_overlay = intervention_def.get('gim_overlay')
    modified_gim = apply_gim_overlay(gim, gim_overlay) if gim_overlay else copy.deepcopy(gim)


    # 2. Apply structural modifications
    structural_mods = intervention_def.get('structural_modifications')
    modified_dag = apply_structural_modifications(dag, structural_mods) if structural_mods else copy.deepcopy(dag)


    # 3. Determine discount rate
    if dr_override is not None:
        dr = float(dr_override)
    else:
        # Extract from dr_trace (handle various structures)
        try:
            dr_data = dr_trace.get('derivation_trace', dr_trace)
            if isinstance(dr_data.get('DR_Static'), dict):
                dr = float(dr_data['DR_Static']['value'])
            else:
                dr = float(dr_data.get('DR_Static', dr_data.get('dr_calculation', {}).get('DR_Static', {}).get('value')))
        except (KeyError, TypeError, ValueError) as e:
            raise RuntimeError(f"Failed to extract DR from dr_trace: {e}")


    # 4. Execute topological sort on modified DAG
    dag_struct = modified_dag.get('DAG', modified_dag)
    try:
        seq = topological_sort(dag_struct)
    except Exception as e:
        raise RuntimeError(f"Topological sort failed on modified DAG: {e}")


    # 5. Execute SCM forecast
    gim_struct = modified_gim.get('GIM', modified_gim)
    try: 
        forecast_df = execute_scm(kg, dag_struct, seq, gim_struct)
    except Exception as e:
        raise RuntimeError(f"SCM execution failed for scenario: {e}")


    # 6. Calculate APV valuation
    try:
        valuation_results = calculate_apv(forecast_df, dr, kg)
    except Exception as e:
        raise RuntimeError(f"APV calculation failed for scenario: {e}")


    # 7. Extract results
    ivps_scenario = valuation_results.get('IVPS', 0.0)
    terminal_g = valuation_results.get('Terminal_g', 0.0)


    # Get terminal ROIC from forecast
    terminal_roic = 0.0
    if 'ROIC' in forecast_df.columns:
        terminal_roic = float(forecast_df['ROIC'].iloc[-1])
    elif 'Terminal_ROIC' in valuation_results:
        terminal_roic = valuation_results['Terminal_ROIC']


    # Calculate terminal reinvestment rate
    terminal_rr = 0.0
    if 'Reinvestment_Rate' in forecast_df.columns:
        terminal_rr = float(forecast_df['Reinvestment_Rate'].iloc[-1])
    elif terminal_roic > EPSILON:
        terminal_rr = terminal_g / terminal_roic if terminal_roic > EPSILON else 0.0


    # 8. P2 Reconciliation (Economic Governor Check)
    p2_status = 'PASS'
    p2_messages = []


    # Check g < DR (perpetuity validity)
    if terminal_g >= dr:
        p2_status = 'FAIL'
        p2_messages.append(f"Terminal g ({terminal_g:.4f}) >= DR ({dr:.4f}). Perpetuity undefined.")


    # Check Economic Governor: g ≈ ROIC × RR
    if terminal_roic > EPSILON and terminal_rr > EPSILON:
        implied_g = terminal_roic * terminal_rr
        governor_diff = abs(terminal_g - implied_g)
        # Allow 10% tolerance
        if governor_diff > max(0.005, abs(implied_g) * 0.10):
            p2_messages.append(f"Economic Governor deviation: g={terminal_g:.4f}, ROIC×RR={implied_g:.4f}")
            # This is a warning, not necessarily a failure


    p2_message = "; ".join(p2_messages) if p2_messages else "Economic Governor satisfied."


    # 9. Calculate base case IVPS for comparison (need to run base case too)
    # For efficiency, we assume base_ivps is passed separately or cached
    # Here we return components for the caller to compute impact


    return {
        'ivps_scenario': ivps_scenario,
        'terminal_g': terminal_g,
        'terminal_roic': terminal_roic,
        'terminal_rr': terminal_rr,
        'dr_used': dr,
        'p2_status': p2_status,
        'p2_message': p2_message,
        'valuation_details': {
            'enterprise_value': valuation_results.get('Enterprise_Value', 0.0),
            'equity_value': valuation_results.get('Equity_Value', 0.0),
            'pv_explicit_fcf': valuation_results.get('PV_Explicit_FCF', 0.0),
            'pv_terminal_fcf': valuation_results.get('PV_Terminal_FCF', 0.0)
        }
    }


# ==========================================================================================
# 3. STRUCTURED STATE ENUMERATION (SSE) FUNCTIONS
# ==========================================================================================


def enumerate_states(scenario_ids):
    """
    Enumerates all 2^N possible states for N scenarios.


    Parameters:
    -----------
    scenario_ids : list
        List of scenario identifiers ['S1', 'S2', 'S3', ...]


    Returns:
    --------
    list : List of state dictionaries
        [
            {'state_id': 'BASE', 'scenarios_active': []},
            {'state_id': 'S1', 'scenarios_active': ['S1']},
            {'state_id': 'S1_S2', 'scenarios_active': ['S1', 'S2']},
            ...
        ]
    """
    n = len(scenario_ids)
    states = []


    # Generate all 2^N combinations using binary representation
    for i in range(2**n):
        active_scenarios = []
        for j in range(n):
            if i & (1 << j):
                active_scenarios.append(scenario_ids[j])


        # Generate state ID
        if not active_scenarios:
            state_id = 'BASE'
        else:
            state_id = '_'.join(sorted(active_scenarios))


        states.append({
            'state_id': state_id,
            'scenarios_active': active_scenarios,
            'binary_mask': i
        })


    return states


def calculate_initial_probabilities(states, scenarios, constraints):
    """
    Calculates initial probabilities for all states based on marginal probabilities
    and causal dependencies.


    Parameters:
    -----------
    states : list
        Output from enumerate_states()
    scenarios : list
        List of scenario definitions:
        [{'scenario_id': 'S1', 'p_posterior': 0.25, 'ivps_impact': 15.0}, ...]
    constraints : dict
        Constraint definitions including causal_dependencies


    Returns:
    --------
    list : States with p_initial added
    """
    # Build lookup for scenario probabilities
    p_marginal = {s['scenario_id']: s['p_posterior'] for s in scenarios}


    # Build dependency lookup
    # dependencies[dependent] = {'condition': scenario_id, 'p_conditional': float}
    dependencies = {}
    for dep in constraints.get('causal_dependencies', []):
        dependent = dep['dependent_scenario']
        condition = dep['condition_scenario']
        p_cond = dep['p_conditional']
        dependencies[dependent] = {'condition': condition, 'p_conditional': p_cond}


    for state in states:
        active = set(state['scenarios_active'])
        p_initial = 1.0


        for scenario_id, p_marg in p_marginal.items():
            is_active = scenario_id in active


            # Check if this scenario has a dependency
            if scenario_id in dependencies:
                dep_info = dependencies[scenario_id]
                condition_id = dep_info['condition']
                condition_active = condition_id in active


                if is_active:
                    if condition_active:
                        # Dependent occurs and condition occurs
                        # P(Dependent AND Condition) = P(Condition) × P(Dependent|Condition)
                        # We handle this by using P(Dependent|Condition) for the dependent
                        p_initial *= dep_info['p_conditional']
                    else:
                        # Dependent occurs but condition doesn't
                        # This is typically low probability or infeasible
                        # P(Dependent AND NOT Condition) = P(Dependent) × P(NOT Condition | Dependent)
                        # For simplicity, use marginal probability adjusted
                        # This case often should be near-zero or handled as infeasible
                        p_initial *= p_marg * 0.1  # Penalty for occurring without condition
                else:
                    if condition_active:
                        # Dependent doesn't occur but condition occurs
                        # P(NOT Dependent | Condition) = 1 - P(Dependent|Condition)
                        p_initial *= (1 - dep_info['p_conditional'])
                    else:
                        # Neither occurs
                        p_initial *= (1 - p_marg)
            else:
                # Independent scenario
                if is_active:
                    p_initial *= p_marg
                else:
                    p_initial *= (1 - p_marg)


        state['p_initial'] = p_initial


    return states


def apply_constraints(states, constraints):
    """
    Applies MECE and Economic Incompatibility constraints to identify infeasible states.


    Parameters:
    -----------
    states : list
        States with p_initial calculated
    constraints : dict
        {
            'mutual_exclusivity_groups': [{'scenarios': ['S1', 'S2'], ...}],
            'economic_incompatibilities': [{'scenario_pair': ['S3', 'S4'], ...}]
        }


    Returns:
    --------
    list : States with feasibility_status and constraint_violated fields
    """
    mece_groups = constraints.get('mutual_exclusivity_groups', [])
    incompatibles = constraints.get('economic_incompatibilities', [])


    for state in states:
        active = set(state['scenarios_active'])
        state['feasibility_status'] = 'FEASIBLE'
        state['constraint_violated'] = None


        # Check MECE constraints
        for mece in mece_groups:
            mece_scenarios = set(mece.get('scenarios', []))
            # Count how many MECE scenarios are active
            active_mece = active.intersection(mece_scenarios)
            if len(active_mece) > 1:
                state['feasibility_status'] = 'INFEASIBLE_MECE'
                state['constraint_violated'] = f"MECE violation: {active_mece}"
                break


        if state['feasibility_status'] != 'FEASIBLE':
            continue


        # Check Economic Incompatibility constraints
        for incomp in incompatibles:
            pair = set(incomp.get('scenario_pair', []))
            if pair.issubset(active):
                state['feasibility_status'] = 'INFEASIBLE_INCOMPATIBLE'
                state['constraint_violated'] = f"Incompatibility violation: {pair}"
                break


    return states


def renormalize_probabilities(states):
    """
    Renormalizes probabilities of feasible states to sum to 1.0.


    Parameters:
    -----------
    states : list
        States with feasibility_status applied


    Returns:
    --------
    tuple : (states with p_final, renormalization_factor)
    """
    # Sum probabilities of feasible states
    feasible_prob_sum = sum(
        s['p_initial'] for s in states 
        if s['feasibility_status'] == 'FEASIBLE'
    )


    if feasible_prob_sum < EPSILON:
        raise RuntimeError("No feasible states with positive probability. Check constraints.")


    renormalization_factor = 1.0 / feasible_prob_sum


    for state in states:
        if state['feasibility_status'] == 'FEASIBLE':
            state['p_final'] = state['p_initial'] * renormalization_factor
        else:
            state['p_final'] = 0.0


    return states, renormalization_factor


def calculate_state_ivps(states, scenarios, base_ivps):
    """
    Calculates IVPS for each state using the Additive Impact Mandate.


    Parameters:
    -----------
    states : list
        States with probabilities calculated
    scenarios : list
        Scenario definitions with ivps_impact
    base_ivps : float
        Base case IVPS (State 2)


    Returns:
    --------
    list : States with ivps_raw, ivps_final, limited_liability_applied
    """
    # Build impact lookup
    impacts = {s['scenario_id']: s['ivps_impact'] for s in scenarios}


    for state in states:
        if state['feasibility_status'] != 'FEASIBLE':
            state['ivps_raw'] = None
            state['ivps_final'] = None
            state['limited_liability_applied'] = False
            continue


        # Calculate raw IVPS using additive impact
        total_impact = sum(impacts.get(sid, 0.0) for sid in state['scenarios_active'])
        ivps_raw = base_ivps + total_impact


        # Apply Limited Liability Constraint
        limited_liability_applied = ivps_raw < 0
        ivps_final = max(0.0, ivps_raw)


        state['ivps_raw'] = ivps_raw
        state['ivps_final'] = ivps_final
        state['limited_liability_applied'] = limited_liability_applied


    return states


def calculate_sse_jpd(scenarios, constraints, base_ivps):
    """
    Main API for Structured State Enumeration.
    Implements the Initialize-Filter-Renormalize procedure.


    This function guarantees computational integrity for JPD calculation.


    Parameters:
    -----------
    scenarios : list
        List of scenario definitions:
        [
            {
                'scenario_id': 'S1',
                'p_posterior': 0.25,
                'ivps_impact': 15.0
            },
            ...
        ]
    constraints : dict
        {
            'causal_dependencies': [
                {'dependent_scenario': 'S2', 'condition_scenario': 'S1', 'p_conditional': 0.8}
            ],
            'mutual_exclusivity_groups': [
                {'scenarios': ['S1a', 'S1b'], 'root_event': 'Acquisition outcome'}
            ],
            'economic_incompatibilities': [
                {'scenario_pair': ['S_BULL', 'S_BEAR']}
            ]
        }
    base_ivps : float
        Base case IVPS from State 2


    Returns:
    --------
    dict : {
        'states': list of state dictionaries with full detail,
        'e_ivps': float,
        'distribution_stats': dict,
        'renormalization_factor': float,
        'feasible_state_count': int,
        'total_state_count': int,
        'probability_sum_validation': float
    }
    """
    # Extract scenario IDs
    scenario_ids = [s['scenario_id'] for s in scenarios]


    # Phase 1: Initialize - Enumerate all states
    states = enumerate_states(scenario_ids)
    total_state_count = len(states)


    # Phase 1b: Calculate initial probabilities
    states = calculate_initial_probabilities(states, scenarios, constraints)


    # Phase 2: Filter - Apply constraints
    states = apply_constraints(states, constraints)


    # Phase 3: Renormalize
    states, renormalization_factor = renormalize_probabilities(states)


    # Calculate state IVPS values
    states = calculate_state_ivps(states, scenarios, base_ivps)


    # Validation
    probability_sum = sum(s['p_final'] for s in states)
    feasible_state_count = sum(1 for s in states if s['feasibility_status'] == 'FEASIBLE')


    # Calculate E[IVPS]
    e_ivps = sum(
        s['p_final'] * s['ivps_final'] 
        for s in states 
        if s['feasibility_status'] == 'FEASIBLE'
    )


    # Calculate distribution statistics
    distribution_stats = calculate_distribution_statistics(states, base_ivps)


    return {
        'states': states,
        'e_ivps': e_ivps,
        'distribution_stats': distribution_stats,
        'renormalization_factor': renormalization_factor,
        'feasible_state_count': feasible_state_count,
        'total_state_count': total_state_count,
        'probability_sum_validation': probability_sum
    }


# ==========================================================================================
# 4. DISTRIBUTION ANALYSIS FUNCTIONS
# ==========================================================================================


def calculate_percentile(sorted_states, target_percentile):
    """
    Calculates the IVPS at a given percentile from sorted states.


    Parameters:
    -----------
    sorted_states : list
        States sorted by ivps_final ascending, with cumulative_probability
    target_percentile : float
        Target percentile (0.0 to 1.0, e.g., 0.10 for P10)


    Returns:
    --------
    float : IVPS at the target percentile
    """
    if not sorted_states:
        return 0.0


    for i, state in enumerate(sorted_states):
        if state['cumulative_probability'] >= target_percentile:
            # Linear interpolation for more accurate percentile
            if i == 0:
                return state['ivps_final']


            prev_state = sorted_states[i-1]
            prev_cum = prev_state['cumulative_probability']
            curr_cum = state['cumulative_probability']


            if curr_cum - prev_cum < EPSILON:
                return state['ivps_final']


            # Interpolate
            fraction = (target_percentile - prev_cum) / (curr_cum - prev_cum)
            return prev_state['ivps_final'] + fraction * (state['ivps_final'] - prev_state['ivps_final'])


    # If we get here, return the maximum
    return sorted_states[-1]['ivps_final']


def calculate_distribution_statistics(states, base_ivps):
    """
    Calculates comprehensive distribution statistics from the SSE results.


    Parameters:
    -----------
    states : list
        States with p_final and ivps_final calculated
    base_ivps : float
        Base case IVPS for reference


    Returns:
    --------
    dict : Distribution statistics
    """
    # Filter to feasible states
    feasible_states = [s for s in states if s['feasibility_status'] == 'FEASIBLE' and s['p_final'] > EPSILON]


    if not feasible_states:
        return {
            'error': 'No feasible states with positive probability'
        }


    # Sort by IVPS for percentile calculations
    sorted_states = sorted(feasible_states, key=lambda x: x['ivps_final'])


    # Calculate cumulative probabilities
    cumulative = 0.0
    for state in sorted_states:
        cumulative += state['p_final']
        state['cumulative_probability'] = cumulative


    # Basic statistics
    ivps_values = [s['ivps_final'] for s in feasible_states]
    probabilities = [s['p_final'] for s in feasible_states]


    # E[IVPS] (mean)
    e_ivps = sum(p * v for p, v in zip(probabilities, ivps_values))


    # Variance and Std Dev
    variance = sum(p * (v - e_ivps)**2 for p, v in zip(probabilities, ivps_values))
    std_dev = math.sqrt(variance) if variance > 0 else 0.0


    # Min/Max
    min_ivps = min(ivps_values)
    max_ivps = max(ivps_values)


    # Percentiles
    p10 = calculate_percentile(sorted_states, 0.10)
    p25 = calculate_percentile(sorted_states, 0.25)
    p50 = calculate_percentile(sorted_states, 0.50)  # Median
    p75 = calculate_percentile(sorted_states, 0.75)
    p90 = calculate_percentile(sorted_states, 0.90)


    # Coefficient of Variation
    cv = std_dev / e_ivps if e_ivps > EPSILON else 0.0


    # Skewness determination
    if abs(e_ivps - p50) < std_dev * 0.1:
        skewness = 'SYMMETRIC'
    elif e_ivps > p50:
        skewness = 'RIGHT'
    else:
        skewness = 'LEFT'


    # Modality detection (simplified)
    # Count "peaks" - states with higher probability than neighbors
    # This is a heuristic; true modality detection would require more sophisticated analysis
    peaks = 0
    for i, state in enumerate(sorted_states):
        is_peak = True
        if i > 0 and sorted_states[i-1]['p_final'] >= state['p_final']:
            is_peak = False
        if i < len(sorted_states) - 1 and sorted_states[i+1]['p_final'] > state['p_final']:
            is_peak = False
        if is_peak and state['p_final'] > 0.05:  # Threshold for meaningful peak
            peaks += 1


    if peaks <= 1:
        modality = 'UNIMODAL'
    elif peaks == 2:
        modality = 'BIMODAL'
    else:
        modality = 'MULTIMODAL'


    return {
        'e_ivps': e_ivps,
        'median_p50': p50,
        'p10': p10,
        'p25': p25,
        'p75': p75,
        'p90': p90,
        'min_ivps': min_ivps,
        'max_ivps': max_ivps,
        'range': max_ivps - min_ivps,
        'standard_deviation': std_dev,
        'variance': variance,
        'coefficient_of_variation': cv,
        'skewness': skewness,
        'modality': modality,
        'base_ivps_reference': base_ivps,
        'sorted_states': sorted_states  # For visualization
    }


def generate_distribution_visualization(distribution_stats, num_buckets=10):
    """
    Generates both ASCII and structured visualizations of the IVPS distribution.


    Parameters:
    -----------
    distribution_stats : dict
        Output from calculate_distribution_statistics()
    num_buckets : int
        Number of buckets for the histogram (default 10)


    Returns:
    --------
    dict : {
        'ascii_representation': str,
        'structured_data': list of bucket dicts
    }
    """
    sorted_states = distribution_stats.get('sorted_states', [])


    if not sorted_states:
        return {
            'ascii_representation': 'No feasible states to visualize.',
            'structured_data': []
        }


    min_ivps = distribution_stats['min_ivps']
    max_ivps = distribution_stats['max_ivps']
    e_ivps = distribution_stats['e_ivps']
    p10 = distribution_stats['p10']
    p50 = distribution_stats['median_p50']
    p90 = distribution_stats['p90']


    # Handle edge case where all values are the same
    if max_ivps - min_ivps < EPSILON:
        bucket_width = 1.0
        num_buckets = 1
    else:
        bucket_width = (max_ivps - min_ivps) / num_buckets


    # Initialize buckets
    buckets = []
    for i in range(num_buckets):
        bucket_start = min_ivps + i * bucket_width
        bucket_end = bucket_start + bucket_width
        bucket_mid = (bucket_start + bucket_end) / 2
        buckets.append({
            'bucket_index': i,
            'ivps_bucket_label': f'${bucket_start:.0f}-{bucket_end:.0f}',
            'ivps_bucket_start': bucket_start,
            'ivps_bucket_end': bucket_end,
            'ivps_bucket_midpoint': bucket_mid,
            'probability_mass': 0.0
        })


    # Assign states to buckets
    for state in sorted_states:
        ivps = state['ivps_final']
        prob = state['p_final']


        # Find the appropriate bucket
        bucket_idx = int((ivps - min_ivps) / bucket_width) if bucket_width > EPSILON else 0
        bucket_idx = min(bucket_idx, num_buckets - 1)  # Handle edge case at max


        buckets[bucket_idx]['probability_mass'] += prob


    # Calculate cumulative probability
    cumulative = 0.0
    for bucket in buckets:
        cumulative += bucket['probability_mass']
        bucket['cumulative_probability'] = cumulative


    # Generate ASCII representation
    max_bar_width = 40
    max_prob = max(b['probability_mass'] for b in buckets) if buckets else 0


    ascii_lines = []
    ascii_lines.append("IVPS Distribution (Probability Mass)")
    ascii_lines.append("")


    for bucket in buckets:
        label = bucket['ivps_bucket_label'].ljust(12)
        prob = bucket['probability_mass']


        if max_prob > EPSILON:
            bar_width = int((prob / max_prob) * max_bar_width)
        else:
            bar_width = 0


        bar = '█' * bar_width
        pct_str = f"({prob*100:.1f}%)"


        # Mark special buckets
        markers = []
        mid = bucket['ivps_bucket_midpoint']
        if bucket['ivps_bucket_start'] <= e_ivps < bucket['ivps_bucket_end']:
            markers.append('← E[IVPS]')


        marker_str = ' '.join(markers)


        ascii_lines.append(f"{label} | {bar} {pct_str} {marker_str}")


    ascii_lines.append("")
    ascii_lines.append(f"E[IVPS]: ${e_ivps:.2f} | Median: ${p50:.2f} | P10: ${p10:.2f} | P90: ${p90:.2f}")


    ascii_representation = '\n'.join(ascii_lines)


    # Prepare structured data (without the internal sorted_states)
    structured_data = [
        {
            'ivps_bucket_label': b['ivps_bucket_label'],
            'ivps_bucket_midpoint': b['ivps_bucket_midpoint'],
            'probability_mass': b['probability_mass'],
            'cumulative_probability': b['cumulative_probability']
        }
        for b in buckets
    ]


    return {
        'ascii_representation': ascii_representation,
        'structured_data': structured_data
    }


# ==========================================================================================
# 5. PROBABILITY SENSITIVITY ANALYSIS
# ==========================================================================================


def calculate_probability_sensitivity(scenarios, constraints, base_ivps, delta_p=0.10):
    """
    Analyzes how changes in scenario probabilities affect E[IVPS].


    Parameters:
    -----------
    scenarios : list
        Scenario definitions
    constraints : dict
        SSE constraints
    base_ivps : float
        Base case IVPS
    delta_p : float
        Probability shift to test (default 0.10 = 10%)


    Returns:
    --------
    list : Sensitivity results for each scenario
    """
    # Get baseline E[IVPS]
    baseline_result = calculate_sse_jpd(scenarios, constraints, base_ivps)
    baseline_e_ivps = baseline_result['e_ivps']


    sensitivities = []


    for i, scenario in enumerate(scenarios):
        scenario_id = scenario['scenario_id']
        original_p = scenario['p_posterior']


        # Create modified scenarios with increased probability
        modified_scenarios = copy.deepcopy(scenarios)
        new_p = min(1.0, original_p + delta_p)
        modified_scenarios[i]['p_posterior'] = new_p


        # Recalculate SSE
        modified_result = calculate_sse_jpd(modified_scenarios, constraints, base_ivps)
        modified_e_ivps = modified_result['e_ivps']


        # Calculate sensitivity
        delta_e_ivps = modified_e_ivps - baseline_e_ivps
        actual_delta_p = new_p - original_p


        sensitivity_ratio = delta_e_ivps / actual_delta_p if actual_delta_p > EPSILON else 0.0


        sensitivities.append({
            'scenario_id': scenario_id,
            'original_p': original_p,
            'delta_p': actual_delta_p,
            'delta_e_ivps': delta_e_ivps,
            'sensitivity_ratio': sensitivity_ratio,
            'interpretation': f"+{actual_delta_p*100:.0f}% probability → ${delta_e_ivps:+.2f} E[IVPS]"
        })


    # Sort by absolute impact
    sensitivities.sort(key=lambda x: abs(x['delta_e_ivps']), reverse=True)


    return sensitivities


# ==========================================================================================
# 6. SCENARIO SUMMARY GENERATOR
# ==========================================================================================


def generate_scenario_summary(sse_result, scenarios, base_ivps, base_dr):
    """
    Generates a comprehensive summary of the scenario analysis.


    This function produces the core content for the probabilistic_valuation_summary
    section of A.10_SCENARIO_MODEL_OUTPUT.


    Parameters:
    -----------
    sse_result : dict
        Output from calculate_sse_jpd()
    scenarios : list
        Scenario definitions
    base_ivps : float
        Base case IVPS
    base_dr : float
        Base case discount rate


    Returns:
    --------
    dict : Summary suitable for A.10 artifact
    """
    dist_stats = sse_result['distribution_stats']


    # Generate visualization
    visualization = generate_distribution_visualization(dist_stats)


    # CVR State Bridge
    delta = sse_result['e_ivps'] - base_ivps
    delta_percent = (delta / base_ivps * 100) if base_ivps > EPSILON else 0.0


    # Risk assessment
    downside_prob = sum(
        s['p_final'] for s in sse_result['states']
        if s['feasibility_status'] == 'FEASIBLE' and s['ivps_final'] < base_ivps
    )


    upside_threshold = base_ivps * 1.25  # 25% above base
    upside_prob = sum(
        s['p_final'] for s in sse_result['states']
        if s['feasibility_status'] == 'FEASIBLE' and s['ivps_final'] > upside_threshold
    )


    # Count states with limited liability applied
    ll_states = sum(
        1 for s in sse_result['states']
        if s.get('limited_liability_applied', False)
    )


    return {
        'schema_version': 'G3_2.2S',
        'primary_output': {
            'e_ivps': sse_result['e_ivps'],
            'e_ivps_derivation': f"Sum of P(State) × IVPS(State) across {sse_result['feasible_state_count']} feasible states"
        },
        'distribution_statistics': {
            'median_p50': dist_stats['median_p50'],
            'p10': dist_stats['p10'],
            'p25': dist_stats['p25'],
            'p75': dist_stats['p75'],
            'p90': dist_stats['p90'],
            'min_ivps': dist_stats['min_ivps'],
            'max_ivps': dist_stats['max_ivps'],
            'range': dist_stats['range'],
            'standard_deviation': dist_stats['standard_deviation'],
            'coefficient_of_variation': dist_stats['coefficient_of_variation']
        },
        'distribution_shape': {
            'skewness': dist_stats['skewness'],
            'modality': dist_stats['modality']
        },
        'distribution_visualization': visualization,
        'cvr_state_bridge': {
            'state_2_ivps_deterministic': base_ivps,
            'state_3_e_ivps_probabilistic': sse_result['e_ivps'],
            'delta': delta,
            'delta_percent': delta_percent
        },
        'risk_metrics': {
            'downside_probability': downside_prob,
            'upside_probability': upside_prob,
            'limited_liability_states': ll_states
        },
        'sse_metadata': {
            'total_states': sse_result['total_state_count'],
            'feasible_states': sse_result['feasible_state_count'],
            'renormalization_factor': sse_result['renormalization_factor'],
            'probability_sum_validation': sse_result['probability_sum_validation']
        }
    }


# ==========================================================================================
# 7. CONVENIENCE WRAPPER FOR FULL SCENARIO EXECUTION
# ==========================================================================================


def execute_full_scenario_analysis(kg, dag, gim, dr_trace, base_ivps, scenario_definitions, constraints):
    """
    Convenience wrapper that executes the complete scenario analysis pipeline.


    This function:
    1. Executes each scenario intervention to get magnitude (M)
    2. Runs SSE integration to get JPD and E[IVPS]
    3. Calculates distribution statistics
    4. Generates summary for artifact construction


    Parameters:
    -----------
    kg : dict
        A.2_ANALYTIC_KG artifact
    dag : dict
        A.3_CAUSAL_DAG artifact
    gim : dict
        A.5_GESTALT_IMPACT_MAP artifact
    dr_trace : dict
        A.6_DR_DERIVATION_TRACE artifact
    base_ivps : float
        Base case IVPS from State 2
    scenario_definitions : list
        List of scenario definitions:
        [
            {
                'scenario_id': 'S1',
                'p_posterior': 0.25,
                'intervention': {
                    'gim_overlay': {...},
                    'structural_modifications': [...] (optional)
                },
                'dr_override': None (or float)
            },
            ...
        ]
    constraints : dict
        SSE constraints (see calculate_sse_jpd)


    Returns:
    --------
    dict : Complete analysis results for A.10 construction
    """
    # Extract base DR
    try:
        dr_data = dr_trace.get('derivation_trace', dr_trace)
        if isinstance(dr_data.get('DR_Static'), dict):
            base_dr = float(dr_data['DR_Static']['value'])
        else:
            base_dr = float(dr_data.get('DR_Static'))
    except:
        base_dr = 0.10  # Fallback


    # Phase 1: Execute scenario interventions
    scenario_results = []
    for scenario_def in scenario_definitions:
        intervention_result = execute_scenario_intervention(
            kg=kg,
            dag=dag,
            gim=gim,
            dr_trace=dr_trace,
            intervention_def=scenario_def.get('intervention', {}),
            dr_override=scenario_def.get('dr_override')
        )


        ivps_impact = intervention_result['ivps_scenario'] - base_ivps


        scenario_results.append({
            'scenario_id': scenario_def['scenario_id'],
            'p_posterior': scenario_def['p_posterior'],
            'ivps_impact': ivps_impact,
            'ivps_scenario': intervention_result['ivps_scenario'],
            'terminal_g': intervention_result['terminal_g'],
            'terminal_roic': intervention_result['terminal_roic'],
            'p2_status': intervention_result['p2_status'],
            'p2_message': intervention_result['p2_message'],
            'dr_used': intervention_result['dr_used']
        })


    # Phase 2: Execute SSE integration
    sse_scenarios = [
        {
            'scenario_id': s['scenario_id'],
            'p_posterior': s['p_posterior'],
            'ivps_impact': s['ivps_impact']
        }
        for s in scenario_results
    ]


    sse_result = calculate_sse_jpd(sse_scenarios, constraints, base_ivps)


    # Phase 3: Calculate probability sensitivities
    prob_sensitivities = calculate_probability_sensitivity(sse_scenarios, constraints, base_ivps)


    # Phase 4: Generate summary
    summary = generate_scenario_summary(sse_result, sse_scenarios, base_ivps, base_dr)


    return {
        'scenario_results': scenario_results,
        'sse_result': sse_result,
        'probability_sensitivities': prob_sensitivities,
        'summary': summary
    }


# ==========================================================================================
# END OF SCENARIO EXTENSION MODULE
# ==========================================================================================


# ==========================================================================================
# CVR KERNEL G3_2.2.4e_IRR
# ==========================================================================================
# FOR REFERENCE ONLY — DO NOT EXECUTE IN T1
# ==========================================================================================
#
# This kernel is embedded for contextual understanding of:
# - Function signatures and parameters
# - TF methodology implementation
# - CR layering mechanics (additive gap closure)
# - Fork generation logic
#
# T1: Use this reference to understand what inputs execute_irr_workflow() requires.
#     Populate A.13 with all necessary arguments. DO NOT call any kernel functions.
#
# T2: Load CVR_KERNEL_IRR_2_2_4e.py from attachments and execute.
#     The kernel file is identical to this reference.
#
# ==========================================================================================

KERNEL_VERSION = "G3_2.2.4e_IRR"


# IRR-specific constants
DEFAULT_CONVERGENCE_RATE = 0.20  # Base rate per B.13
MAX_CONVERGENCE_RATE_UNJUSTIFIED = 0.40
CORRELATION_FLAG_THRESHOLD = 0.10  # CV below this triggers flag


# ==========================================================================================
# 1. FUNDAMENTAL PROJECTION FUNCTIONS
# ==========================================================================================


def calculate_forward_fundamentals(forecast_df, horizon_year=1):
    """
    Extracts projected fundamentals at the specified horizon year.


    Parameters:
    -----------
    forecast_df : DataFrame
        Output from execute_scm() containing Y1-Y20 forecasts
    horizon_year : int
        The target year (1 = T+1, 2 = T+2, etc.)


    Returns:
    --------
    dict : Fundamental metrics at horizon
    """
    if horizon_year < 1 or horizon_year > len(forecast_df):
        raise ValueError(f"Horizon year {horizon_year} out of range [1, {len(forecast_df)}]")


    idx = horizon_year - 1  # Convert to 0-indexed
    row = forecast_df.iloc[idx]


    fundamentals = {}


    # Extract available metrics
    metric_mapping = {
        'Revenue': 'revenue',
        'EBITDA': 'ebitda',
        'EBIT': 'ebit',
        'NOPAT': 'nopat',
        'FCF_Unlevered': 'fcf',
        'Invested_Capital': 'invested_capital',
        'ROIC': 'roic'
    }


    for df_col, output_key in metric_mapping.items():
        if df_col in forecast_df.columns:
            fundamentals[output_key] = float(row[df_col])


    # Calculate margins if components available
    if 'revenue' in fundamentals and fundamentals['revenue'] > EPSILON:
        if 'ebitda' in fundamentals:
            fundamentals['ebitda_margin'] = fundamentals['ebitda'] / fundamentals['revenue']
        if 'ebit' in fundamentals:
            fundamentals['ebit_margin'] = fundamentals['ebit'] / fundamentals['revenue']


    # Calculate growth rate from Y0 to horizon
    if 'Revenue' in forecast_df.columns and idx > 0:
        y0_revenue = forecast_df['Revenue'].iloc[0]
        if y0_revenue > EPSILON:
            fundamentals['revenue_growth_to_horizon'] = (
                (fundamentals.get('revenue', 0) / y0_revenue) ** (1 / horizon_year) - 1
            )


    fundamentals['horizon_year'] = horizon_year


    return fundamentals


def apply_scenario_overlay_to_fundamentals(base_fundamentals, scenarios, fork_scenarios_active, rho_estimates):
    """
    Adjusts base fundamentals for active scenarios in a fork, scaled by resolution percentage.


    Parameters:
    -----------
    base_fundamentals : dict
        Output from calculate_forward_fundamentals() for base case
    scenarios : list
        Scenario definitions with 'scenario_id' and 'ivps_impact'
    fork_scenarios_active : list
        List of scenario_ids active in this fork
    rho_estimates : dict
        {scenario_id: rho} mapping resolution percentages


    Returns:
    --------
    dict : Adjusted fundamentals for the fork
    """
    adjusted = copy.deepcopy(base_fundamentals)


    # For now, we pass through fundamentals unchanged
    # The scenario impact flows through the multiple adjustment, not fundamentals
    # This function exists for future extension where scenarios modify operating metrics


    adjusted['scenarios_active'] = fork_scenarios_active
    adjusted['scenario_adjustments_applied'] = []


    return adjusted


# ==========================================================================================
# 2. MULTIPLE-BASED VALUATION FUNCTIONS
# ==========================================================================================


def select_valuation_multiples(fundamentals, company_profile=None):
    """
    Selects appropriate valuation multiple(s) based on company profile.
    Implements B.10 Multiple Selection guidelines.


    Parameters:
    -----------
    fundamentals : dict
        Contains ebitda_margin, revenue_growth, fcf, etc.
    company_profile : dict, optional
        Additional profile info (cyclical, sector, etc.)


    Returns:
    --------
    dict : {
        'primary': {'metric': str, 'weight': float},
        'secondary': {'metric': str, 'weight': float} | None,
        'rationale': str
    }
    """
    ebitda_margin = fundamentals.get('ebitda_margin', 0)
    growth = fundamentals.get('revenue_growth_to_horizon', 0)
    fcf = fundamentals.get('fcf', 0)
    ebitda = fundamentals.get('ebitda', 0)


    # FCF conversion proxy
    fcf_conversion = (fcf / ebitda) if ebitda > EPSILON else 0


    # Decision logic (B.10 guidelines)
    if ebitda_margin < 0.10 and growth > 0.20:
        return {
            'primary': {'metric': 'EV_Revenue', 'weight': 1.0},
            'secondary': None,
            'rationale': 'Pre-profit growth company; revenue is valuation anchor'
        }


    elif ebitda_margin >= 0.10 and ebitda_margin < 0.20 and growth > 0.15:
        return {
            'primary': {'metric': 'EV_Revenue', 'weight': 0.6},
            'secondary': {'metric': 'EV_EBITDA', 'weight': 0.4},
            'rationale': 'Transitional; growth dominates but profitability emerging'
        }


    elif ebitda_margin >= 0.20 and fcf_conversion > 0.50:
        return {
            'primary': {'metric': 'EV_EBITDA', 'weight': 0.5},
            'secondary': {'metric': 'EV_FCF', 'weight': 0.5},
            'rationale': 'Mature profitable company; cash generation focus'
        }


    else:
        return {
            'primary': {'metric': 'EV_EBITDA', 'weight': 1.0},
            'secondary': None,
            'rationale': 'Default for profitable companies'
        }


def calculate_current_multiple(market_data, fundamentals_y0, multiple_type):
    """
    Calculates the company's current trading multiple.


    Parameters:
    -----------
    market_data : dict
        Contains 'market_cap', 'net_debt', 'current_price', 'shares_outstanding'
    fundamentals_y0 : dict
        Y0 fundamental metrics (revenue, ebitda, fcf)
    multiple_type : str
        'EV_Revenue', 'EV_EBITDA', or 'EV_FCF'


    Returns:
    --------
    float : Current multiple
    """
    ev = market_data.get('market_cap', 0) + market_data.get('net_debt', 0)


    if ev <= 0:
        return None


    metric_map = {
        'EV_Revenue': fundamentals_y0.get('revenue', 0),
        'EV_EBITDA': fundamentals_y0.get('ebitda', 0),
        'EV_FCF': fundamentals_y0.get('fcf', 0)
    }


    denominator = metric_map.get(multiple_type, 0)


    if denominator <= EPSILON:
        return None


    return ev / denominator


def calculate_multiple_valuation(fundamentals_t1, multiple, market_data):
    """
    Calculates implied share price using multiple-based valuation.


    Parameters:
    -----------
    fundamentals_t1 : dict
        Projected fundamentals at T+1
    multiple : dict
        {'metric': str, 'value': float} or weighted combination
    market_data : dict
        Contains 'net_debt', 'shares_outstanding'


    Returns:
    --------
    dict : {
        'ev': float,
        'equity_value': float,
        'price_t1': float,
        'calculation_trace': str
    }
    """
    # Handle single or weighted multiple
    if isinstance(multiple, dict) and 'primary' in multiple:
        # Weighted multiple structure
        primary = multiple['primary']
        secondary = multiple.get('secondary')


        ev_primary = _calculate_ev_from_multiple(
            fundamentals_t1, 
            primary['metric'], 
            primary['value']
        )


        if secondary and secondary.get('value'):
            ev_secondary = _calculate_ev_from_multiple(
                fundamentals_t1,
                secondary['metric'],
                secondary['value']
            )
            ev = (primary['weight'] * ev_primary) + (secondary['weight'] * ev_secondary)
            trace = f"EV = {primary['weight']:.0%} × {primary['metric']} + {secondary['weight']:.0%} × {secondary['metric']}"
        else:
            ev = ev_primary
            trace = f"EV = {primary['metric']} × {primary['value']:.1f}x"
    else:
        # Simple {metric, value} structure
        ev = _calculate_ev_from_multiple(
            fundamentals_t1,
            multiple.get('metric'),
            multiple.get('value')
        )
        trace = f"EV = {multiple.get('metric')} × {multiple.get('value', 0):.1f}x"


    net_debt = market_data.get('net_debt', 0)
    shares = market_data.get('shares_outstanding', 1)


    equity_value = ev - net_debt
    price_t1 = equity_value / shares if shares > 0 else 0


    return {
        'ev': ev,
        'net_debt': net_debt,
        'equity_value': equity_value,
        'shares_outstanding': shares,
        'price_t1': max(0, price_t1),  # Limited liability
        'calculation_trace': trace
    }


def _calculate_ev_from_multiple(fundamentals, metric_type, multiple_value):
    """Helper to calculate EV from a single multiple."""
    metric_map = {
        'EV_Revenue': fundamentals.get('revenue', 0),
        'EV_EBITDA': fundamentals.get('ebitda', 0),
        'EV_FCF': fundamentals.get('fcf', 0),
        'EV_NOPAT': fundamentals.get('nopat', 0)
    }


    metric = metric_map.get(metric_type, 0)
    return metric * multiple_value if multiple_value else 0


# ==========================================================================================
# 2.5 TRANSITION FACTOR IMPLEMENTATION (Patch 2.2)
# ==========================================================================================
#
# The Transition Factor (TF) approach eliminates the cohort-based "fair multiple" anchor
# and instead uses DCF-implied multiples to determine how market multiples should evolve.
#
# Core Principle: The market price at T0 already incorporates the market's cohort analysis,
# growth expectations, and risk assessment. We don't need to separately derive "cohort fair."
# Instead, we use the ratio between market and DCF-implied multiples and preserve it at T+1.
#
# Key Equation:
#   Market_Multiple_T1 = Market_Multiple_T0 × TF
#   where TF = DCF_Multiple_T1 / DCF_Multiple_T0
#
# This ensures:
#   - If Market Price = IVPS at T0 → IRR ≈ DR (earn required return on fair value)
#   - If Market < DCF (undervalued) → IRR ≈ DR + undervaluation kicker
#   - If Market > DCF (overvalued) → IRR ≈ DR - overvaluation drag
# ==========================================================================================


def calculate_transition_factor(
    ivps_t0,
    dr_static,
    fcf_y1,
    net_debt_t0,
    fdso,
    metric_t0,
    metric_t1,
    capital_allocation='RETAIN_FCF'
):
    """
    Calculate the Transition Factor (TF) that maps T0 DCF-implied multiple
    to T+1 DCF-implied multiple.


    The TF captures how the company's "warranted" multiple should evolve based on
    its growth trajectory, margin expansion, capex requirements, and FCF conversion
    as embedded in the DCF model.


    Parameters:
    -----------
    ivps_t0 : float
        Intrinsic value per share at T0 (from State 4 E[IVPS])
    dr_static : float
        Static discount rate (e.g., 0.11 for 11%)
    fcf_y1 : float
        Year 1 free cash flow ($M) - used for cash accumulation
    net_debt_t0 : float
        Net debt at T0 ($M, negative = net cash)
    fdso : float
        Fully diluted shares outstanding (M)
    metric_t0 : float
        Valuation metric at T0 (Revenue or EBITDA, $M)
    metric_t1 : float
        Valuation metric at T+1 ($M)
    capital_allocation : str
        Capital allocation assumption:
        - 'RETAIN_FCF': FCF accumulates as cash (reduces net debt) - DEFAULT
        - 'DISTRIBUTE_FCF': FCF distributed to shareholders (net debt unchanged)
        - 'GUIDANCE_SPECIFIED': Use explicit guidance (requires separate handling)


    Returns:
    --------
    dict : {
        'transition_factor': float - TF ratio to apply to market multiple,
        'dcf_multiple_t0': float - DCF-implied multiple at T0,
        'dcf_multiple_t1': float - DCF-implied multiple at T+1,
        'net_debt_t1': float - Projected net debt at T+1,
        'ivps_t1': float - Projected IVPS at T+1,
        'dcf_ev_t0': float - DCF-implied enterprise value at T0,
        'dcf_ev_t1': float - DCF-implied enterprise value at T+1,
        'multiple_compression_pct': float - Percentage change in DCF multiple,
        'calculation_trace': str - Human-readable calculation trace
    }


    Raises:
    -------
    ValueError: If inputs are invalid (e.g., zero/negative IVPS, FDSO)


    Example:
    --------
    For DAVE at T0:
        IVPS = $240, DR = 11%, FCF_Y1 = $89.8M, Net_Debt = -$17M
        FDSO = 13.5M, Revenue_T0 = $347M, Revenue_T1 = $503.2M


    >>> tf_result = calculate_transition_factor(
    ...     ivps_t0=240, dr_static=0.11, fcf_y1=89.8,
    ...     net_debt_t0=-17, fdso=13.5, metric_t0=347, metric_t1=503.2
    ... )
    >>> tf_result['transition_factor']
    0.747  # DCF multiple compresses 25.3% because revenue grows faster than IVPS
    """
    # Input validation
    if ivps_t0 <= 0:
        raise ValueError(f"IVPS_T0 must be positive, got {ivps_t0}")
    if fdso <= 0:
        raise ValueError(f"FDSO must be positive, got {fdso}")
    if metric_t0 <= EPSILON:
        raise ValueError(f"Metric_T0 must be positive, got {metric_t0}")
    if metric_t1 <= EPSILON:
        raise ValueError(f"Metric_T1 must be positive, got {metric_t1}")
    if dr_static <= 0 or dr_static >= 1:
        raise ValueError(f"DR must be between 0 and 1, got {dr_static}")


    # -------------------------------------------------------------------------
    # T0 DCF Values
    # -------------------------------------------------------------------------
    equity_t0 = ivps_t0 * fdso
    # EV = Equity Value + Net Debt
    # Where Net Debt = Total Debt - Cash (positive = net debt, negative = net cash)
    # Standard formula: EV = Market Cap + Net Debt
    dcf_ev_t0 = equity_t0 + net_debt_t0
    dcf_multiple_t0 = dcf_ev_t0 / metric_t0


    # -------------------------------------------------------------------------
    # T+1 DCF Values
    # -------------------------------------------------------------------------
    # IVPS compounds at the discount rate (this is the definition of intrinsic value)
    ivps_t1 = ivps_t0 * (1 + dr_static)
    equity_t1 = ivps_t1 * fdso


    # Net debt evolution depends on capital allocation policy
    if capital_allocation == 'RETAIN_FCF':
        # FCF retained as cash → reduces net debt (or increases net cash)
        net_debt_t1 = net_debt_t0 - fcf_y1
    elif capital_allocation == 'DISTRIBUTE_FCF':
        # FCF distributed → net debt unchanged
        net_debt_t1 = net_debt_t0
    else:
        # Default to RETAIN_FCF for unrecognized values
        logger.warning(f"Unrecognized capital_allocation '{capital_allocation}'; defaulting to RETAIN_FCF")
        net_debt_t1 = net_debt_t0 - fcf_y1


    dcf_ev_t1 = equity_t1 + net_debt_t1
    dcf_multiple_t1 = dcf_ev_t1 / metric_t1


    # -------------------------------------------------------------------------
    # Transition Factor
    # -------------------------------------------------------------------------
    if dcf_multiple_t0 > EPSILON:
        tf = dcf_multiple_t1 / dcf_multiple_t0
    else:
        tf = 1.0
        logger.warning("DCF_Multiple_T0 near zero; defaulting TF to 1.0")


    # Calculate compression percentage for diagnostics
    multiple_compression_pct = (tf - 1.0)  # Negative means compression


    # Build calculation trace for transparency
    trace_lines = [
        f"T0: Equity=${equity_t0:.1f}M + Net_Debt=${net_debt_t0:.1f}M = EV=${dcf_ev_t0:.1f}M",
        f"T0: Metric=${metric_t0:.1f}M, DCF_Multiple={dcf_multiple_t0:.2f}x",
        f"T1: IVPS=${ivps_t1:.2f} (IVPS_T0 × {1+dr_static:.2f})",
        f"T1: Equity=${equity_t1:.1f}M, Net_Debt=${net_debt_t1:.1f}M (policy: {capital_allocation})",
        f"T1: EV=${dcf_ev_t1:.1f}M, Metric=${metric_t1:.1f}M, DCF_Multiple={dcf_multiple_t1:.2f}x",
        f"TF = {dcf_multiple_t1:.2f}x / {dcf_multiple_t0:.2f}x = {tf:.3f}",
        f"Multiple {'compresses' if tf < 1 else 'expands'} by {abs(multiple_compression_pct)*100:.1f}%"
    ]


    return {
        'transition_factor': tf,
        'dcf_multiple_t0': dcf_multiple_t0,
        'dcf_multiple_t1': dcf_multiple_t1,
        'net_debt_t0': net_debt_t0,
        'net_debt_t1': net_debt_t1,
        'ivps_t0': ivps_t0,
        'ivps_t1': ivps_t1,
        'dcf_ev_t0': dcf_ev_t0,
        'dcf_ev_t1': dcf_ev_t1,
        'equity_t0': equity_t0,
        'equity_t1': equity_t1,
        'multiple_compression_pct': multiple_compression_pct,
        'capital_allocation': capital_allocation,
        'calculation_trace': '\n'.join(trace_lines)
    }


def calculate_market_multiple_t0(market_data, fundamentals_y0, metric_type):
    """
    Calculate the current market-implied multiple at T0.


    This is the multiple the market is currently paying, which serves as the
    starting point for the Transition Factor approach.


    Parameters:
    -----------
    market_data : dict
        Must contain: 'current_price', 'shares_outstanding', 'net_debt'
    fundamentals_y0 : dict
        Must contain the relevant metric (revenue, ebitda, etc.)
    metric_type : str
        One of: 'EV_Revenue', 'EV_EBITDA', 'EV_FCF', 'EV_NOPAT'


    Returns:
    --------
    dict : {
        'market_multiple_t0': float,
        'market_ev': float,
        'metric_value': float,
        'calculation_trace': str
    }
    """
    price = market_data.get('current_price', 0)
    shares = market_data.get('shares_outstanding', 0)
    net_debt = market_data.get('net_debt', 0)


    if price <= 0 or shares <= 0:
        return {
            'market_multiple_t0': None,
            'market_ev': None,
            'metric_value': None,
            'calculation_trace': 'ERROR: Invalid price or shares'
        }


    market_cap = price * shares
    market_ev = market_cap + net_debt


    # Get metric value
    metric_map = {
        'EV_Revenue': fundamentals_y0.get('revenue', 0),
        'EV_EBITDA': fundamentals_y0.get('ebitda', 0),
        'EV_FCF': fundamentals_y0.get('fcf', 0),
        'EV_NOPAT': fundamentals_y0.get('nopat', 0)
    }
    metric_value = metric_map.get(metric_type, 0)


    if metric_value <= EPSILON:
        return {
            'market_multiple_t0': None,
            'market_ev': market_ev,
            'metric_value': metric_value,
            'calculation_trace': f'ERROR: Metric {metric_type} is zero or negative'
        }


    market_multiple = market_ev / metric_value


    trace = (
        f"Market Cap = ${price:.2f} × {shares:.1f}M = ${market_cap:.1f}M\n"
        f"Market EV = ${market_cap:.1f}M + ${net_debt:.1f}M = ${market_ev:.1f}M\n"
        f"{metric_type} = ${metric_value:.1f}M\n"
        f"Market Multiple = ${market_ev:.1f}M / ${metric_value:.1f}M = {market_multiple:.2f}x"
    )


    return {
        'market_multiple_t0': market_multiple,
        'market_ev': market_ev,
        'metric_value': metric_value,
        'calculation_trace': trace
    }


def calculate_scenario_multiple_impacts_from_ivps(scenarios, fdso, base_metric_t1):
    """
    Derive multiple impact from IVPS impact for each scenario.


    This replaces the cohort-proportional mapping approach (Issue B fix).
    Instead of using cohort spread, we derive the multiple impact directly
    from the IVPS impact, which is already computed in the DCF framework.


    Formula: Multiple_Impact = (IVPS_Impact × FDSO) / Metric_T1


    This ensures consistency between the DCF valuation and the multiple-based
    IRR calculation.


    Parameters:
    -----------
    scenarios : list
        Scenario definitions containing 'scenario_id' and 'ivps_impact'
    fdso : float
        Fully diluted shares outstanding (M)
    base_metric_t1 : float
        Base case valuation metric at T+1 (Revenue or EBITDA, $M)


    Returns:
    --------
    dict : {scenario_id: multiple_impact}


    Example:
    --------
    For scenario S4 with IVPS impact of -$78.07:
        EV Impact = -$78.07 × 13.5M = -$1,054M
        Multiple Impact = -$1,054M / $503.2M = -2.1x
    """
    impacts = {}


    if base_metric_t1 <= EPSILON:
        logger.warning("Base metric T1 is zero/negative; cannot calculate multiple impacts")
        return impacts


    if fdso <= EPSILON:
        logger.warning("FDSO is zero/negative; cannot calculate multiple impacts")
        return impacts


    for s in scenarios:
        scenario_id = s.get('scenario_id')
        ivps_impact = s.get('ivps_impact', 0)


        # Convert IVPS impact to EV impact
        ev_impact = ivps_impact * fdso


        # Convert EV impact to multiple impact
        multiple_impact = ev_impact / base_metric_t1


        impacts[scenario_id] = multiple_impact


        logger.debug(f"Scenario {scenario_id}: IVPS_Impact=${ivps_impact:.2f}, "
                    f"EV_Impact=${ev_impact:.1f}M, Multiple_Impact={multiple_impact:.2f}x")


    return impacts


def calculate_fork_market_multiple(
    market_multiple_t0,
    transition_factor,
    active_scenarios,
    scenario_multiple_impacts,
    rho_estimates,
    convergence_velocity=0.0,
    dcf_multiple_t1=None
):
    """
    Calculate T+1 market multiple for a fork using the Transition Factor approach.


    This implements the core of Patch 2.3, replacing the cohort-based convergence
    model with DCF-anchored evolution.


    Base Evolution:
        Market_Multiple_T1 = Market_Multiple_T0 × TF


    Plus scenario adjustments (ρ-weighted):
        Adjusted_Multiple = Base_Multiple + Σ(ρ_i × Multiple_Impact_i)


    Optional convergence overlay (CV, default 0):
        Final_Multiple = Adjusted_Multiple + CV × (DCF_Multiple_T1 - Adjusted_Multiple)


    Parameters:
    -----------
    market_multiple_t0 : float
        Current market-implied multiple
    transition_factor : float
        TF from calculate_transition_factor()
    active_scenarios : list
        Scenario IDs active in this fork
    scenario_multiple_impacts : dict
        {scenario_id: multiple_delta} from calculate_scenario_multiple_impacts_from_ivps()
    rho_estimates : dict
        {scenario_id: rho} resolution percentages
    convergence_velocity : float, optional
        CV ∈ [0, 1], default 0 (no convergence toward DCF)
        - CV = 0: Market maintains current view (default)
        - CV = 1: Full convergence to DCF-implied
    dcf_multiple_t1 : float, optional
        DCF-implied multiple at T+1 (required if CV > 0)


    Returns:
    --------
    dict : {
        'market_multiple_t1': float - Final T+1 market multiple for this fork,
        'base_multiple_t1': float - Multiple before scenario adjustments,
        'scenario_adjustment': float - Total adjustment from active scenarios,
        'convergence_adjustment': float - Adjustment from CV (if applied),
        'convergence_applied': bool - Whether CV was applied,
        'calculation_trace': str - Human-readable trace
    }
    """
    # Base evolution via transition factor
    base_multiple_t1 = market_multiple_t0 * transition_factor


    # Scenario adjustments (ρ-weighted)
    scenario_adjustment = 0.0
    adjustment_details = []


    for scenario_id in active_scenarios:
        impact = scenario_multiple_impacts.get(scenario_id, 0)
        rho = rho_estimates.get(scenario_id, 0)


        if abs(impact) > EPSILON and rho > EPSILON:
            adj = impact * rho
            scenario_adjustment += adj
            adjustment_details.append(f"{scenario_id}: {impact:+.2f}x × ρ={rho:.2f} = {adj:+.2f}x")


    market_multiple_t1 = base_multiple_t1 + scenario_adjustment


    # Optional convergence overlay
    convergence_adjustment = 0.0
    convergence_applied = False


    if convergence_velocity > EPSILON and dcf_multiple_t1 is not None:
        gap = dcf_multiple_t1 - market_multiple_t1
        convergence_adjustment = convergence_velocity * gap
        market_multiple_t1 = market_multiple_t1 + convergence_adjustment
        convergence_applied = True


    # Floor at minimum sensible multiple
    market_multiple_t1 = max(0.5, market_multiple_t1)


    # Build trace
    trace_lines = [
        f"Base: {market_multiple_t0:.2f}x × TF={transition_factor:.3f} = {base_multiple_t1:.2f}x"
    ]
    if adjustment_details:
        trace_lines.append(f"Scenario adjustments: {', '.join(adjustment_details)}")
        trace_lines.append(f"Post-scenario: {base_multiple_t1:.2f}x + {scenario_adjustment:+.2f}x = {base_multiple_t1 + scenario_adjustment:.2f}x")
    if convergence_applied:
        trace_lines.append(f"Convergence (CV={convergence_velocity:.2f}): +{convergence_adjustment:+.2f}x")
    trace_lines.append(f"Final Market Multiple T1: {market_multiple_t1:.2f}x")


    return {
        'market_multiple_t1': market_multiple_t1,
        'base_multiple_t1': base_multiple_t1,
        'scenario_adjustment': scenario_adjustment,
        'convergence_adjustment': convergence_adjustment,
        'convergence_applied': convergence_applied,
        'calculation_trace': '\n'.join(trace_lines)
    }


# ==========================================================================================
# 3. CONVERGENCE AND MULTIPLE ASSIGNMENT
# ==========================================================================================


def calculate_fair_multiple(cohort_multiples, inside_view_adjustments=None):
    """
    Calculates fair multiple from cohort anchor plus inside view adjustments.
    Implements B.11 Cohort Protocol.


    Parameters:
    -----------
    cohort_multiples : dict
        {'p25': float, 'p50': float, 'p75': float}
    inside_view_adjustments : list, optional
        [{'factor': str, 'adjustment': float, 'rationale': str}, ...]


    Returns:
    --------
    dict : {
        'cohort_anchor': float,
        'adjustments': list,
        'fair_multiple': float
    }
    """
    anchor = cohort_multiples.get('p50', 0)


    total_adjustment = 0
    adjustments_applied = []


    if inside_view_adjustments:
        for adj in inside_view_adjustments:
            adjustment = adj.get('adjustment', 0)
            total_adjustment += adjustment
            adjustments_applied.append({
                'factor': adj.get('factor'),
                'adjustment': adjustment,
                'rationale': adj.get('rationale')
            })


    # Cap extreme adjustments (rarely exceed ±3x per B.11)
    if abs(total_adjustment) > 3.0:
        logger.warning(f"Total adjustment {total_adjustment:.1f}x exceeds ±3x guidance")


    fair_multiple = anchor + total_adjustment


    return {
        'cohort_anchor': anchor,
        'adjustments': adjustments_applied,
        'total_adjustment': total_adjustment,
        'fair_multiple': max(0.5, fair_multiple)  # Floor at 0.5x to avoid negative
    }


def calculate_convergence_multiple(current_multiple, fair_multiple, convergence_rate):
    """
    Calculates the expected multiple at T+1 given convergence rate.
    Implements B.13 Convergence Rate Framework (CR calibration per B.13.3-B.13.4).


    Parameters:
    -----------
    current_multiple : float
    fair_multiple : float
    convergence_rate : float (0 to 1)


    Returns:
    --------
    float : Expected multiple at T+1
    """
    if convergence_rate < 0 or convergence_rate > 1:
        raise ValueError(f"Convergence rate {convergence_rate} must be in [0, 1]")


    gap = fair_multiple - current_multiple
    expected_multiple = current_multiple + (convergence_rate * gap)


    return expected_multiple


def adjust_multiple_for_fork(base_fair_multiple, fork_scenarios_active, scenario_multiple_impacts, rho_estimates):
    """
    Adjusts the fair multiple for a specific fork based on active scenarios,
    scaled by resolution percentage (rho) to reflect partial T+1 resolution.


    Parameters:
    -----------
    base_fair_multiple : float
        Fair multiple from null case
    fork_scenarios_active : list
        Scenario IDs active in this fork
    scenario_multiple_impacts : dict
        {scenario_id: multiple_delta} - how each scenario affects the multiple
    rho_estimates : dict
        {scenario_id: rho} - resolution percentage [0,1] for each scenario.
        Scenarios resolve partially by T+1; impact is scaled by rho.


    Returns:
    --------
    dict : {
        'base_multiple': float,
        'adjustment': float,
        'fork_multiple': float,
        'rationale': str,
        'rho_scaling_applied': bool
    }
    """
    total_adjustment = 0
    adjustments = []
    rho_scaling_applied = False


    for scenario_id in fork_scenarios_active:
        if scenario_id in scenario_multiple_impacts:
            base_delta = scenario_multiple_impacts[scenario_id]


            # Apply rho-scaling: partial resolution at T+1
            rho = rho_estimates.get(scenario_id, 1.0)
            if rho < 1.0:
                rho_scaling_applied = True
            if scenario_id not in rho_estimates:
                logger.warning(f"Missing rho for {scenario_id}; defaulting to 1.0 (full resolution)")


            scaled_delta = base_delta * rho
            total_adjustment += scaled_delta
            adjustments.append(f"{scenario_id}: {base_delta:+.2f}x × ρ={rho:.2f} → {scaled_delta:+.2f}x")


    fork_multiple = base_fair_multiple + total_adjustment


    return {
        'base_multiple': base_fair_multiple,
        'adjustment': total_adjustment,
        'fork_multiple': max(0.5, fork_multiple),
        'rationale': ', '.join(adjustments) if adjustments else 'No scenario adjustments',
        'rho_scaling_applied': rho_scaling_applied
    }


# ==========================================================================================
# 4. IRR CALCULATION FUNCTIONS
# ==========================================================================================


def calculate_fork_irr(price_t0, price_t1, horizon_years=1):
    """
    Calculates IRR for a single fork.


    For single-period: IRR = (P1/P0)^(1/H) - 1


    Parameters:
    -----------
    price_t0 : float
        Current price (entry)
    price_t1 : float
        Expected price at horizon (exit)
    horizon_years : int
        Investment horizon in years


    Returns:
    --------
    float : IRR (as decimal, e.g., 0.15 for 15%)
    """
    if price_t0 <= 0:
        raise ValueError("Entry price must be positive")


    if price_t1 <= 0:
        return -1.0  # Total loss


    if horizon_years <= 0:
        raise ValueError("Horizon must be positive")


    irr = (price_t1 / price_t0) ** (1 / horizon_years) - 1


    return irr


def calculate_null_case_irr(
    price_t0,
    fundamentals_y0,
    fundamentals_t1,
    current_multiple,
    fair_multiple,
    convergence_rate,
    market_data,
    multiple_selection
):
    """
    DEPRECATED (Patch 2.4): This function implements the legacy cohort-based approach.


    For Transition Factor methodology (default in v2.2.3), null case IRR is calculated
    directly in execute_irr_workflow() using:
        null_market_multiple_t1 = market_multiple_t0 × transition_factor
        null_irr = (price_t1 / price_t0) - 1


    This function is retained for backward compatibility with use_transition_factor=False.


    Legacy behavior: Calculates the null case IRR with 3-component decomposition.
    Implements B.14 IRR Decomposition.


    Parameters:
    -----------
    price_t0 : float
        Current market price
    fundamentals_y0 : dict
        Y0 metrics
    fundamentals_t1 : dict
        T+1 projected metrics
    current_multiple : float
    fair_multiple : float
        From cohort P50 + inside view adjustments
    convergence_rate : float
    market_data : dict
    multiple_selection : dict
        Output from select_valuation_multiples()


    Returns:
    --------
    dict : Full null case analysis with legacy decomposition


    DEPRECATED FIELDS:
    - irr_decomposition.fundamental_growth_irr
    - irr_decomposition.multiple_convergence_irr
    - convergence_dependency_ratio


    These fields are set to 0 in the TF approach (Patch 2.3+).
    """
    # Get the metric being used
    primary_metric = multiple_selection['primary']['metric']


    metric_map_y0 = {
        'EV_Revenue': fundamentals_y0.get('revenue', 0),
        'EV_EBITDA': fundamentals_y0.get('ebitda', 0),
        'EV_FCF': fundamentals_y0.get('fcf', 0)
    }


    metric_map_t1 = {
        'EV_Revenue': fundamentals_t1.get('revenue', 0),
        'EV_EBITDA': fundamentals_t1.get('ebitda', 0),
        'EV_FCF': fundamentals_t1.get('fcf', 0)
    }


    metric_y0 = metric_map_y0.get(primary_metric, 0)
    metric_t1 = metric_map_t1.get(primary_metric, 0)


    # Calculate fundamental growth
    if metric_y0 > EPSILON:
        fundamental_growth = (metric_t1 / metric_y0) - 1
    else:
        fundamental_growth = 0


    # Calculate expected multiple at T+1
    expected_multiple_t1 = calculate_convergence_multiple(
        current_multiple, fair_multiple, convergence_rate
    )


    # Build multiple structure for valuation
    valuation_multiple = {
        'primary': {
            'metric': primary_metric,
            'value': expected_multiple_t1,
            'weight': multiple_selection['primary']['weight']
        },
        'secondary': None
    }


    # Handle secondary multiple if present
    if multiple_selection.get('secondary'):
        sec = multiple_selection['secondary']
        # For simplicity, apply same convergence to secondary
        valuation_multiple['secondary'] = {
            'metric': sec['metric'],
            'value': expected_multiple_t1,  # Could be refined
            'weight': sec['weight']
        }


    # Calculate T+1 price
    valuation_result = calculate_multiple_valuation(
        fundamentals_t1, valuation_multiple, market_data
    )
    price_t1 = valuation_result['price_t1']


    # Calculate total IRR
    total_irr = calculate_fork_irr(price_t0, price_t1)


    # Decomposition
    # Fundamental Growth IRR: return if multiple stayed constant
    price_t1_constant_multiple = calculate_multiple_valuation(
        fundamentals_t1,
        {'metric': primary_metric, 'value': current_multiple},
        market_data
    )['price_t1']
    fundamental_growth_irr = calculate_fork_irr(price_t0, price_t1_constant_multiple)


    # Multiple Convergence IRR: residual
    multiple_convergence_irr = total_irr - fundamental_growth_irr


    # Convergence Dependency Ratio
    if abs(total_irr) > EPSILON:
        cdr = multiple_convergence_irr / total_irr if total_irr > 0 else 0
    else:
        cdr = 0


    return {
        'fundamentals_t1': fundamentals_t1,
        'current_multiple': current_multiple,
        'fair_multiple': fair_multiple,
        'convergence_rate': convergence_rate,
        'expected_multiple_t1': expected_multiple_t1,
        'valuation_t1': valuation_result,
        'price_t1': price_t1,
        'irr_decomposition': {
            'fundamental_growth_irr': fundamental_growth_irr,
            'multiple_convergence_irr': multiple_convergence_irr,
            'scenario_resolution_irr': 0,  # Null case has no scenario component
            'total_irr': total_irr
        },
        'convergence_dependency_ratio': cdr
    }


# ==========================================================================================
# 5. FORK GENERATION AND INTEGRATION
# ==========================================================================================


# -----------------------------------------------------------------------------
# 5.1 SCENARIO FUNDAMENTALS MAPPING (Patch 2.1)
# -----------------------------------------------------------------------------
# These functions extract and blend scenario-specific fundamentals for fork
# generation, addressing Issue A from the v2.2.3 patch specification:
# "Scenario Fundamentals Not Propagated to Forks"
# -----------------------------------------------------------------------------


def build_scenario_fundamentals_map(scenarios):
    """
    Extract fundamentals_y1_intervened from scenario definitions.


    This function builds a lookup map of scenario-specific Y1 fundamentals
    that were computed during scenario intervention in the SCENARIO/INTEGRATION
    stages and passed through via the CVR State 4 Bundle.


    Parameters:
    -----------
    scenarios : list
        Scenario definitions from state_4_active_inputs.scenarios_finalized
        Each scenario should contain 'fundamentals_y1_intervened' dict with:
        - revenue: float ($M)
        - ebitda: float ($M)
        - ebit: float ($M)
        - ebit_margin: float (0-1)
        - nopat: float ($M)
        - fcf_unlevered: float ($M)


    Returns:
    --------
    dict : {scenario_id: {revenue, ebitda, ebit, nopat, fcf, ...}}


    Example:
    --------
    >>> scenarios = [
    ...     {'scenario_id': 'S1', 'fundamentals_y1_intervened': {'revenue': 550.0, 'ebitda': 110.0}},
    ...     {'scenario_id': 'S4', 'fundamentals_y1_intervened': {'revenue': 428.5, 'ebitda': 85.2}}
    ... ]
    >>> sfm = build_scenario_fundamentals_map(scenarios)
    >>> sfm['S4']['revenue']
    428.5
    """
    scenario_fundamentals_map = {}


    for s in scenarios:
        scenario_id = s.get('scenario_id')
        if not scenario_id:
            continue


        fundamentals = s.get('fundamentals_y1_intervened', {})


        if fundamentals:
            # Normalize key names (handle both 'fcf_unlevered' and 'fcf')
            normalized = {
                'revenue': fundamentals.get('revenue', 0),
                'ebitda': fundamentals.get('ebitda', 0),
                'ebit': fundamentals.get('ebit', 0),
                'ebit_margin': fundamentals.get('ebit_margin', 0),
                'nopat': fundamentals.get('nopat', 0),
                'fcf': fundamentals.get('fcf_unlevered', fundamentals.get('fcf', 0))
            }
            scenario_fundamentals_map[scenario_id] = normalized
        else:
            # Log warning but don't fail - fork will use base fundamentals
            logger.warning(f"Scenario {scenario_id} missing fundamentals_y1_intervened; "
                          f"fork will use base case fundamentals")


    return scenario_fundamentals_map


def calculate_fork_fundamentals(
    base_fundamentals,
    active_scenarios,
    scenario_fundamentals_map,
    rho_estimates
):
    """
    Calculate ρ-weighted blend of base and scenario fundamentals for a fork.


    This implements the fix for Issue A: scenarios now affect both multiples
    AND fundamentals. A Credit Deterioration scenario (S4) with ρ=0.35 will
    now reflect 35% of its revenue impact, not just 35% of its multiple impact.


    The blending formula for each metric:
        fork_metric = base_metric + Σ(ρ_i × (scenario_metric_i - base_metric))


    This ensures:
    - ρ=0 → fork uses base fundamentals (no resolution)
    - ρ=1 → fork uses full scenario fundamentals (complete resolution)
    - 0<ρ<1 → fork uses proportional blend (partial resolution)


    Parameters:
    -----------
    base_fundamentals : dict
        Base case Y1 fundamentals from null case:
        {revenue, ebitda, fcf, nopat, ...}
    active_scenarios : list
        List of scenario IDs active in this fork (e.g., ['S1', 'S3'])
    scenario_fundamentals_map : dict
        Output from build_scenario_fundamentals_map():
        {scenario_id: {revenue, ebitda, ...}}
    rho_estimates : dict
        {scenario_id: rho} resolution percentages (0-1)


    Returns:
    --------
    dict : Fork-specific fundamentals with same structure as base_fundamentals,
           plus metadata about adjustments applied


    Example:
    --------
    >>> base = {'revenue': 503.2, 'ebitda': 120.0}
    >>> sfm = {'S4': {'revenue': 428.5, 'ebitda': 85.2}}
    >>> rho = {'S4': 0.35}
    >>> fork_funds = calculate_fork_fundamentals(base, ['S4'], sfm, rho)
    >>> fork_funds['revenue']
    477.06  # = 503.2 + 0.35 × (428.5 - 503.2)
    """
    # Start with copy of base fundamentals
    fork_fundamentals = dict(base_fundamentals)


    # Track adjustments for transparency
    adjustments_applied = []


    # Metrics to blend
    blend_metrics = ['revenue', 'ebitda', 'ebit', 'nopat', 'fcf']


    for scenario_id in active_scenarios:
        # Skip if no fundamentals available for this scenario
        if scenario_id not in scenario_fundamentals_map:
            logger.debug(f"No fundamentals map for {scenario_id}; skipping fundamental adjustment")
            continue


        # Get resolution percentage (default to 0 if not specified = no adjustment)
        rho = rho_estimates.get(scenario_id, 0)
        if rho <= EPSILON:
            continue  # No resolution = no adjustment


        scenario_funds = scenario_fundamentals_map[scenario_id]


        # Apply ρ-weighted adjustment for each metric
        for metric in blend_metrics:
            if metric not in fork_fundamentals:
                continue
            if metric not in scenario_funds:
                continue


            base_val = fork_fundamentals[metric]
            scenario_val = scenario_funds[metric]


            # Skip if base value is missing/zero (can't compute meaningful delta)
            if base_val is None:
                continue
            if scenario_val is None:
                continue


            # Calculate delta and apply ρ-weighted adjustment
            delta = scenario_val - base_val
            adjustment = rho * delta
            fork_fundamentals[metric] = base_val + adjustment


            # Track for transparency
            if abs(adjustment) > EPSILON:
                adjustments_applied.append({
                    'scenario_id': scenario_id,
                    'metric': metric,
                    'base_value': base_val,
                    'scenario_value': scenario_val,
                    'rho': rho,
                    'adjustment': adjustment,
                    'final_value': fork_fundamentals[metric]
                })


    # Recalculate derived metrics if needed
    if 'revenue' in fork_fundamentals and fork_fundamentals['revenue'] > EPSILON:
        if 'ebitda' in fork_fundamentals:
            fork_fundamentals['ebitda_margin'] = (
                fork_fundamentals['ebitda'] / fork_fundamentals['revenue']
            )
        if 'ebit' in fork_fundamentals:
            fork_fundamentals['ebit_margin'] = (
                fork_fundamentals['ebit'] / fork_fundamentals['revenue']
            )


    # Add metadata
    fork_fundamentals['_adjustments_applied'] = adjustments_applied
    fork_fundamentals['_scenarios_blended'] = list(active_scenarios)
    fork_fundamentals['_is_base_case'] = len(adjustments_applied) == 0


    return fork_fundamentals


# -----------------------------------------------------------------------------
# 5.2 FORK GENERATION
# -----------------------------------------------------------------------------


def generate_irr_forks(
    scenarios,
    jpd_states,
    rho_estimates,
    null_case,
    scenario_multiple_impacts,
    market_data,
    price_t0,
    multiple_selection,
    scenario_fundamentals_map=None  # Patch 2.1: Optional pre-built map
):
    """
    Generates all forks with IRR calculations.


    Patch 2.1 Enhancement: Now uses fork-specific fundamentals instead of
    holding fundamentals constant across all forks. This fixes Issue A where
    scenarios like Credit Deterioration would only affect multiples, not
    the underlying revenue/EBITDA used in valuation.


    Parameters:
    -----------
    scenarios : list
        Scenario definitions from A.10 / state_4_active_inputs.scenarios_finalized
        Should contain 'fundamentals_y1_intervened' for each scenario (Patch 1.1)
    jpd_states : list
        States from calculate_sse_jpd()
    rho_estimates : dict
        {scenario_id: rho} resolution percentages
    null_case : dict
        Output from calculate_null_case_irr()
    scenario_multiple_impacts : dict
        {scenario_id: multiple_delta}
    market_data : dict
    price_t0 : float
    multiple_selection : dict
        Output from select_valuation_multiples() specifying primary/secondary metrics
    scenario_fundamentals_map : dict, optional
        Pre-built map from build_scenario_fundamentals_map(). If not provided,
        will be built from scenarios parameter.


    Returns:
    --------
    list : Fork analysis for each state, now including fork-specific fundamentals
    """
    forks = []


    base_fundamentals = null_case['fundamentals_t1']
    base_fair_multiple = null_case['fair_multiple']
    convergence_rate = null_case['convergence_rate']
    current_multiple = null_case['current_multiple']


    # Patch 2.1: Build scenario fundamentals map if not provided
    if scenario_fundamentals_map is None:
        scenario_fundamentals_map = build_scenario_fundamentals_map(scenarios)


    # Track whether any scenarios have fundamentals available
    has_scenario_fundamentals = len(scenario_fundamentals_map) > 0
    if not has_scenario_fundamentals:
        logger.warning("No scenario fundamentals available; all forks will use base case fundamentals")


    # P3 Patch: Extract valuation metric from multiple_selection with fallback handling
    primary_metric = multiple_selection['primary']['metric']
    valuation_fallback_applied = False


    # Edge case: If EV_EBITDA selected but EBITDA ≤ 0, need fallback
    ebitda_t1 = base_fundamentals.get('ebitda', 0)
    if primary_metric == 'EV_EBITDA' and ebitda_t1 <= EPSILON:
        # Check for secondary metric first
        if multiple_selection.get('secondary') and multiple_selection['secondary'].get('metric'):
            fallback_metric = multiple_selection['secondary']['metric']
            logger.warning(f"Valuation Fallback: EBITDA ≤ 0, switching from EV_EBITDA to {fallback_metric}")
        else:
            fallback_metric = 'EV_Revenue'
            logger.warning(f"Valuation Fallback: EBITDA ≤ 0, no secondary metric defined, defaulting to EV_Revenue")
        primary_metric = fallback_metric
        valuation_fallback_applied = True


    for state in jpd_states:
        if state['feasibility_status'] != 'FEASIBLE':
            continue


        fork_id = state['state_id']
        scenarios_active = state['scenarios_active']
        fork_probability = state['p_final']


        # Skip extremely low probability forks
        if fork_probability < 0.001:
            continue


        # ---------------------------------------------------------------------
        # Patch 2.1: Calculate fork-specific fundamentals
        # ---------------------------------------------------------------------
        # This is the key fix for Issue A: fundamentals now vary by fork
        fork_fundamentals = calculate_fork_fundamentals(
            base_fundamentals=base_fundamentals,
            active_scenarios=scenarios_active,
            scenario_fundamentals_map=scenario_fundamentals_map,
            rho_estimates=rho_estimates
        )


        # Extract adjustment metadata for output (without polluting fundamentals dict)
        fundamentals_adjustments = fork_fundamentals.pop('_adjustments_applied', [])
        fork_fundamentals.pop('_scenarios_blended', None)
        is_base_fundamentals = fork_fundamentals.pop('_is_base_case', True)


        # Adjust multiple for this fork (with rho-scaling for partial resolution)
        multiple_adj = adjust_multiple_for_fork(
            base_fair_multiple,
            scenarios_active,
            scenario_multiple_impacts,
            rho_estimates
        )
        fork_fair_multiple = multiple_adj['fork_multiple']


        # Calculate expected multiple at T+1 for this fork
        fork_expected_multiple = calculate_convergence_multiple(
            current_multiple,
            fork_fair_multiple,
            convergence_rate
        )


        # ---------------------------------------------------------------------
        # Patch 2.1: Use fork_fundamentals instead of base_fundamentals
        # ---------------------------------------------------------------------
        # This ensures scenarios affect BOTH the multiple AND the fundamentals
        valuation = calculate_multiple_valuation(
            fork_fundamentals,  # Changed from base_fundamentals
            {'metric': primary_metric, 'value': fork_expected_multiple},
            market_data
        )


        # Calculate fork IRR
        fork_irr = calculate_fork_irr(price_t0, valuation['price_t1'])


        forks.append({
            'fork_id': fork_id,
            'scenarios_active': scenarios_active,
            'fork_probability': fork_probability,
            'multiple_assignment': {
                'base_fair_multiple': base_fair_multiple,
                'fork_adjustment': multiple_adj['adjustment'],
                'fork_fair_multiple': fork_fair_multiple,
                'expected_multiple_t1': fork_expected_multiple,
                'rationale': multiple_adj['rationale'],
                'valuation_metric': primary_metric,
                'valuation_fallback_flag': valuation_fallback_applied
            },
            # Patch 2.1: Include fork-specific fundamentals in output
            'fork_fundamentals': {
                'revenue': fork_fundamentals.get('revenue'),
                'ebitda': fork_fundamentals.get('ebitda'),
                'fcf': fork_fundamentals.get('fcf'),
                'is_base_case': is_base_fundamentals,
                'adjustments_applied': fundamentals_adjustments
            },
            'valuation_t1': valuation,
            'price_t1': valuation['price_t1'],
            'fork_irr': fork_irr
        })


    return forks


def generate_irr_forks_tf(
    scenarios,
    jpd_states,
    rho_estimates,
    null_case,
    scenario_multiple_impacts,
    market_data,
    price_t0,
    multiple_selection,
    scenario_fundamentals_map,
    transition_factor,
    market_multiple_t0,
    tf_result
):
    """
    Generate forks using Transition Factor approach (Patch 2.3).


    This replaces the cohort-based convergence model with DCF-anchored evolution.
    Key differences from generate_irr_forks():
    - Uses TF x Market_Multiple_T0 as base evolution (not convergence to cohort P50)
    - Scenario adjustments are derived from IVPS impacts
    - No "fair multiple" concept - DCF-implied is used for reference only


    Parameters:
    -----------
    scenarios : list
        Scenario definitions containing fundamentals_y1_intervened
    jpd_states : list
        JPD states from calculate_sse_jpd()
    rho_estimates : dict
        {scenario_id: rho} resolution percentages
    null_case : dict
        Null case analysis including transition_factor_analysis
    scenario_multiple_impacts : dict
        {scenario_id: multiple_delta} from calculate_scenario_multiple_impacts_from_ivps()
    market_data : dict
        Current market data (price, shares, net_debt)
    price_t0 : float
        Current stock price
    multiple_selection : dict
        Primary/secondary valuation metrics
    scenario_fundamentals_map : dict
        {scenario_id: fundamentals} from build_scenario_fundamentals_map()
    transition_factor : float
        TF from calculate_transition_factor()
    market_multiple_t0 : float
        Current market-implied multiple
    tf_result : dict
        Full output from calculate_transition_factor()


    Returns:
    --------
    list : Fork analysis using TF methodology
    """
    forks = []


    base_fundamentals = null_case['fundamentals_t1']
    shares_outstanding = market_data.get('shares_outstanding', 0)
    net_debt_t1 = tf_result.get('net_debt_t1', market_data.get('net_debt', 0))


    # Extract valuation metric
    primary_metric = multiple_selection['primary']['metric']
    valuation_fallback_applied = False


    # Fallback handling for EBITDA <= 0
    ebitda_t1 = base_fundamentals.get('ebitda', 0)
    if primary_metric == 'EV_EBITDA' and ebitda_t1 <= EPSILON:
        if multiple_selection.get('secondary') and multiple_selection['secondary'].get('metric'):
            fallback_metric = multiple_selection['secondary']['metric']
            logger.warning(f"Valuation Fallback: EBITDA <= 0, switching from EV_EBITDA to {fallback_metric}")
        else:
            fallback_metric = 'EV_Revenue'
            logger.warning(f"Valuation Fallback: EBITDA <= 0, defaulting to EV_Revenue")
        primary_metric = fallback_metric
        valuation_fallback_applied = True


    for state in jpd_states:
        if state['feasibility_status'] != 'FEASIBLE':
            continue


        fork_id = state['state_id']
        scenarios_active = state['scenarios_active']
        fork_probability = state['p_final']


        # Skip extremely low probability forks
        if fork_probability < 0.001:
            continue


        # ---------------------------------------------------------------------
        # Step 1: Calculate fork-specific fundamentals (Patch 2.1)
        # ---------------------------------------------------------------------
        fork_fundamentals = calculate_fork_fundamentals(
            base_fundamentals=base_fundamentals,
            active_scenarios=scenarios_active,
            scenario_fundamentals_map=scenario_fundamentals_map,
            rho_estimates=rho_estimates
        )


        # Extract metadata
        fundamentals_adjustments = fork_fundamentals.pop('_adjustments_applied', [])
        fork_fundamentals.pop('_scenarios_blended', None)
        is_base_fundamentals = fork_fundamentals.pop('_is_base_case', True)


        # ---------------------------------------------------------------------
        # Step 2: Calculate fork market multiple using TF approach (Patch 2.3)
        # ---------------------------------------------------------------------
        multiple_result = calculate_fork_market_multiple(
            market_multiple_t0=market_multiple_t0,
            transition_factor=transition_factor,
            active_scenarios=scenarios_active,
            scenario_multiple_impacts=scenario_multiple_impacts,
            rho_estimates=rho_estimates,
            convergence_velocity=0.2,  # Default: 20% convergence to DCF
            dcf_multiple_t1=tf_result.get('dcf_multiple_t1')
        )


        fork_market_multiple_t1 = multiple_result['market_multiple_t1']


        # ---------------------------------------------------------------------
        # Step 3: Calculate T+1 valuation using fork fundamentals and multiple
        # ---------------------------------------------------------------------
        # Get the metric value for this fork
        metric_map = {
            'EV_Revenue': fork_fundamentals.get('revenue', 0),
            'EV_EBITDA': fork_fundamentals.get('ebitda', 0),
            'EV_FCF': fork_fundamentals.get('fcf', 0)
        }
        fork_metric_t1 = metric_map.get(primary_metric, fork_fundamentals.get('revenue', 0))


        # Calculate EV and price
        fork_ev_t1 = fork_metric_t1 * fork_market_multiple_t1
        fork_equity_t1 = fork_ev_t1 - net_debt_t1
        fork_price_t1 = fork_equity_t1 / shares_outstanding if shares_outstanding > EPSILON else 0
        fork_price_t1 = max(0, fork_price_t1)  # Limited liability floor


        # Calculate IRR
        fork_irr = (fork_price_t1 / price_t0) - 1 if price_t0 > EPSILON else 0


        # ---------------------------------------------------------------------
        # Step 4: Build fork output structure
        # ---------------------------------------------------------------------
        forks.append({
            'fork_id': fork_id,
            'scenarios_active': scenarios_active,
            'fork_probability': fork_probability,
            # Patch 2.3: TF-based multiple assignment
            'multiple_assignment': {
                'market_multiple_t0': market_multiple_t0,
                'transition_factor': transition_factor,
                'base_multiple_t1': multiple_result['base_multiple_t1'],
                'scenario_adjustment': multiple_result['scenario_adjustment'],
                'fork_market_multiple_t1': fork_market_multiple_t1,
                'calculation_trace': multiple_result['calculation_trace'],
                'valuation_metric': primary_metric,
                'valuation_fallback_flag': valuation_fallback_applied
            },
            # Patch 2.1: Fork-specific fundamentals
            'fork_fundamentals': {
                'revenue': fork_fundamentals.get('revenue'),
                'ebitda': fork_fundamentals.get('ebitda'),
                'fcf': fork_fundamentals.get('fcf'),
                'metric_used': fork_metric_t1,
                'is_base_case': is_base_fundamentals,
                'adjustments_applied': fundamentals_adjustments
            },
            'valuation_t1': {
                'ev': fork_ev_t1,
                'net_debt': net_debt_t1,
                'equity_value': fork_equity_t1,
                'shares_outstanding': shares_outstanding,
                'price_t1': fork_price_t1
            },
            'price_t1': fork_price_t1,
            'fork_irr': fork_irr
        })


    return forks


def _interpret_null_irr(null_irr, dr_static, market_dcf_ratio):
    """
    Generate human-readable interpretation of null case IRR.


    This helps users understand whether the null IRR is sensible given
    the relationship between market price and DCF value.


    Parameters:
    -----------
    null_irr : float
        Null case IRR (no scenario resolution)
    dr_static : float
        Discount rate used in DCF
    market_dcf_ratio : float
        Market_Multiple / DCF_Multiple at T0


    Returns:
    --------
    str : Interpretation text
    """
    # Market at fair value: IRR should approximate DR
    if 0.95 <= market_dcf_ratio <= 1.05:
        if abs(null_irr - dr_static) < 0.02:
            return (f"Market priced near DCF fair value (ratio={market_dcf_ratio:.2f}). "
                   f"Null IRR of {null_irr:.1%} appropriately approximates DR of {dr_static:.1%}.")
        else:
            return (f"Market priced near DCF fair value (ratio={market_dcf_ratio:.2f}). "
                   f"Null IRR of {null_irr:.1%} differs from DR ({dr_static:.1%}); "
                   f"review fundamentals growth assumptions.")


    # Market undervalued relative to DCF
    elif market_dcf_ratio < 0.95:
        expected_premium = (1 / market_dcf_ratio - 1) * dr_static  # Rough approximation
        if null_irr > dr_static:
            return (f"Market undervalued vs DCF (ratio={market_dcf_ratio:.2f}). "
                   f"Null IRR of {null_irr:.1%} exceeds DR ({dr_static:.1%}) as expected - "
                   f"reflects potential for multiple expansion if market re-rates toward DCF.")
        else:
            return (f"Market undervalued vs DCF (ratio={market_dcf_ratio:.2f}) but "
                   f"null IRR ({null_irr:.1%}) does not exceed DR ({dr_static:.1%}). "
                   f"Review: fundamental growth may be offsetting undervaluation.")


    # Market overvalued relative to DCF
    else:
        if null_irr < dr_static:
            return (f"Market overvalued vs DCF (ratio={market_dcf_ratio:.2f}). "
                   f"Null IRR of {null_irr:.1%} below DR ({dr_static:.1%}) as expected - "
                   f"reflects potential for multiple compression.")
        else:
            return (f"Market overvalued vs DCF (ratio={market_dcf_ratio:.2f}) but "
                   f"null IRR ({null_irr:.1%}) exceeds DR ({dr_static:.1%}). "
                   f"Review: strong fundamental growth may be offsetting overvaluation.")


def calculate_irr_distribution(forks, null_case_irr):
    """
    Calculates E[IRR] and distribution statistics from forks.


    Parameters:
    -----------
    forks : list
        Output from generate_irr_forks()
    null_case_irr : float
        IRR from null case (for decomposition)


    Returns:
    --------
    dict : IRR integration results
    """
    if not forks:
        return {'error': 'No feasible forks'}


    # E[IRR]
    e_irr = sum(f['fork_probability'] * f['fork_irr'] for f in forks)


    # Sort by IRR for percentile calculation
    sorted_forks = sorted(forks, key=lambda x: x['fork_irr'])


    # Calculate cumulative probabilities
    cumulative = 0
    for fork in sorted_forks:
        cumulative += fork['fork_probability']
        fork['cumulative_probability'] = cumulative


    # Percentiles
    def get_percentile(target):
        for fork in sorted_forks:
            if fork['cumulative_probability'] >= target:
                return fork['fork_irr']
        return sorted_forks[-1]['fork_irr']


    p10 = get_percentile(0.10)
    p25 = get_percentile(0.25)
    p50 = get_percentile(0.50)
    p75 = get_percentile(0.75)
    p90 = get_percentile(0.90)


    # Standard deviation
    variance = sum(
        f['fork_probability'] * (f['fork_irr'] - e_irr) ** 2
        for f in forks
    )
    std_dev = math.sqrt(variance) if variance > 0 else 0


    # Scenario resolution component
    scenario_resolution_irr = e_irr - null_case_irr


    return {
        'e_irr': e_irr,
        'irr_distribution': {
            'p10': p10,
            'p25': p25,
            'p50_median': p50,
            'p75': p75,
            'p90': p90,
            'standard_deviation': std_dev
        },
        'scenario_resolution_contribution': scenario_resolution_irr,
        'fork_count': len(forks),
        'sorted_forks': sorted_forks
    }


# ==========================================================================================
# 6. SANITY CHECKS
# ==========================================================================================


def run_value_trap_test(null_case, price_t0, market_data, multiple_selection, hurdle_rate=0.15):
    """
    Tests IRR under zero convergence assumption.


    Parameters:
    -----------
    null_case : dict
        Output from calculate_null_case_irr()
    price_t0 : float
    market_data : dict
    multiple_selection : dict
        Output from select_valuation_multiples() specifying primary/secondary metrics
    hurdle_rate : float


    Returns:
    --------
    dict : Value trap test results
    """
    # Calculate price at T+1 with ZERO convergence (multiple stays at current)
    fundamentals_t1 = null_case['fundamentals_t1']
    current_multiple = null_case['current_multiple']


    # Use dynamically selected metric (consistent with fork generation)
    primary_metric = multiple_selection['primary']['metric']


    # Apply same fallback logic as fork generation
    ebitda_t1 = fundamentals_t1.get('ebitda', 0)
    if primary_metric == 'EV_EBITDA' and ebitda_t1 <= EPSILON:
        if multiple_selection.get('secondary') and multiple_selection['secondary'].get('metric'):
            primary_metric = multiple_selection['secondary']['metric']
        else:
            primary_metric = 'EV_Revenue'


    valuation_zero_conv = calculate_multiple_valuation(
        fundamentals_t1,
        {'metric': primary_metric, 'value': current_multiple},
        market_data
    )


    irr_zero_convergence = calculate_fork_irr(price_t0, valuation_zero_conv['price_t1'])
    passes_hurdle = irr_zero_convergence >= hurdle_rate


    if passes_hurdle:
        interpretation = "PASS: Returns exceed hurdle even without multiple expansion"
    elif irr_zero_convergence > 0:
        interpretation = "CAUTION: Positive returns but below hurdle without convergence"
    else:
        interpretation = "WARNING: Negative returns without multiple expansion - convergence dependent"


    return {
        'irr_zero_convergence': irr_zero_convergence,
        'hurdle_rate': hurdle_rate,
        'passes_hurdle': passes_hurdle,
        'interpretation': interpretation
    }


def run_fork_independence_check(forks):
    """
    Checks for correlation bias in fork estimates.


    Parameters:
    -----------
    forks : list
        Output from generate_irr_forks()


    Returns:
    --------
    dict : Independence check results
    """
    if len(forks) < 2:
        return {
            'multiple_cv': None,
            'irr_cv': None,
            'correlation_flag': False,
            'interpretation': 'Insufficient forks for independence check'
        }


    # Extract multiples and IRRs
    multiples = [f['multiple_assignment']['expected_multiple_t1'] for f in forks]
    irrs = [f['fork_irr'] for f in forks]


    # Coefficient of Variation for multiples
    mult_mean = np.mean(multiples)
    mult_std = np.std(multiples)
    multiple_cv = mult_std / mult_mean if mult_mean > EPSILON else 0


    # CV for IRRs
    irr_mean = np.mean(irrs)
    irr_std = np.std(irrs)
    irr_cv = irr_std / abs(irr_mean) if abs(irr_mean) > EPSILON else 0


    # Flag if multiples cluster too tightly
    correlation_flag = multiple_cv < CORRELATION_FLAG_THRESHOLD


    if correlation_flag:
        interpretation = f"WARNING: Fork multiples cluster tightly (CV={multiple_cv:.3f}). Possible correlation bias."
    else:
        interpretation = f"PASS: Fork multiples show adequate dispersion (CV={multiple_cv:.3f})"


    return {
        'multiple_cv': multiple_cv,
        'irr_cv': irr_cv,
        'correlation_flag': correlation_flag,
        'interpretation': interpretation
    }


def run_diagnostic_flags(forks, rho_estimates, convergence_rate):
    """
    Generates diagnostic flags for review.


    Parameters:
    -----------
    forks : list
    rho_estimates : dict
    convergence_rate : float


    Returns:
    --------
    dict : Diagnostic flags
    """
    flags = []


    # Average rho check
    if rho_estimates:
        avg_rho = np.mean(list(rho_estimates.values()))
        rho_above_50 = avg_rho > 0.50
        if rho_above_50:
            flags.append(f"Average ρ = {avg_rho:.2f} exceeds 0.50 (narrative bias risk)")
    else:
        avg_rho = None
        rho_above_50 = False


    # All positive IRRs check
    all_positive = all(f['fork_irr'] > 0 for f in forks)
    if all_positive:
        flags.append("All fork IRRs positive (optimism check)")


    # Convergence above 40% check
    convergence_above_40 = convergence_rate > MAX_CONVERGENCE_RATE_UNJUSTIFIED
    if convergence_above_40:
        flags.append(f"Convergence rate {convergence_rate:.0%} exceeds 40% threshold")


    return {
        'average_rho': avg_rho,
        'average_rho_above_50': rho_above_50,
        'all_fork_irrs_positive': all_positive,
        'convergence_above_40': convergence_above_40,
        'flags_triggered': flags
    }


def run_sanity_checks(null_case, forks, rho_estimates, price_t0, market_data, multiple_selection, hurdle_rate=0.15):
    """
    Runs all sanity checks and returns consolidated results.


    Parameters:
    -----------
    null_case : dict
    forks : list
    rho_estimates : dict
    price_t0 : float
    market_data : dict
    multiple_selection : dict
        Output from select_valuation_multiples() specifying primary/secondary metrics
    hurdle_rate : float


    Returns:
    --------
    dict : All sanity check results
    """
    value_trap = run_value_trap_test(null_case, price_t0, market_data, multiple_selection, hurdle_rate)
    independence = run_fork_independence_check(forks)
    diagnostics = run_diagnostic_flags(forks, rho_estimates, null_case['convergence_rate'])


    return {
        'value_trap_test': value_trap,
        'fork_independence_check': independence,
        'diagnostic_flags': diagnostics
    }


# ==========================================================================================
# 7. MAIN IRR WORKFLOW ORCHESTRATOR
# ==========================================================================================


def _generate_confidence_assessment(pipeline_fit_grade, pipeline_fit_caveat, sanity_checks, null_case, irr_integration, cr):
    """
    Generates the confidence_assessment section for A.13, incorporating Pipeline Fit grade
    and sanity check results.


    Parameters:
    -----------
    pipeline_fit_grade : str
        Grade from Integration stage (A/B/C/D/F/UNKNOWN)
    pipeline_fit_caveat : str or None
        Grade-specific caveat text
    sanity_checks : dict
        Output from run_sanity_checks()
    null_case : dict
        Null case analysis results
    irr_integration : dict
        IRR integration results
    cr : float
        Convergence rate used


    Returns:
    --------
    dict : confidence_assessment section for A.13
    """
    # Determine overall confidence based on Pipeline Fit and sanity checks
    diagnostic_flags = sanity_checks.get('diagnostic_flags', {})
    flags_triggered = diagnostic_flags.get('flags_triggered', [])
    value_trap_result = sanity_checks.get('value_trap_test', {})


    # Grade-based confidence mapping
    grade_confidence = {
        'A': 'HIGH',
        'B': 'HIGH',
        'C': 'MEDIUM',
        'D': 'LOW',
        'F': 'VERY_LOW',
        'UNKNOWN': 'MEDIUM'
    }
    base_confidence = grade_confidence.get(pipeline_fit_grade, 'MEDIUM')


    # Downgrade confidence if sanity checks flagged issues
    if len(flags_triggered) >= 2 and base_confidence == 'HIGH':
        base_confidence = 'MEDIUM'
    elif len(flags_triggered) >= 3:
        base_confidence = 'LOW'


    # Identify key uncertainties
    key_uncertainties = []


    if pipeline_fit_grade in ['C', 'D', 'F']:
        key_uncertainties.append(f"Pipeline Fit Grade {pipeline_fit_grade}: Upstream valuation has material blind spots")


    if 'convergence_above_40' in flags_triggered:
        key_uncertainties.append(f"Convergence rate ({cr:.0%}) exceeds conservative threshold")


    if 'average_rho_above_50' in flags_triggered:
        key_uncertainties.append("High average resolution percentage may overstate T+1 scenario certainty")


    if value_trap_result.get('interpretation', '').startswith('WARNING'):
        key_uncertainties.append("Value trap risk: Returns dependent on multiple expansion")


    cdr = null_case.get('convergence_dependency_ratio', 0)
    if cdr > 0.5:
        key_uncertainties.append(f"Convergence dependency ratio ({cdr:.0%}): Returns heavily reliant on re-rating")


    # Identify highest-leverage assumptions
    highest_leverage = []


    highest_leverage.append({
        'assumption': 'Convergence Rate',
        'current_value': f"{cr:.0%}",
        'sensitivity': 'Direct impact on multiple expansion component of return'
    })


    highest_leverage.append({
        'assumption': 'Fair Multiple Estimate',
        'current_value': f"{null_case.get('fair_multiple', 0):.1f}x",
        'sensitivity': 'Determines magnitude of re-rating opportunity'
    })


    e_irr = irr_integration.get('e_irr', 0)
    highest_leverage.append({
        'assumption': 'Scenario Probabilities',
        'current_value': 'Per A.10/A.12',
        'sensitivity': f"Scenario resolution contributes {irr_integration.get('scenario_resolution_contribution', 0):.1%} to E[IRR]"
    })


    # Generate recommendation summary
    if pipeline_fit_grade == 'F':
        recommendation = "BLOCK RECOMMENDATION: Do not rely on this IRR analysis for investment decisions. Alternative analytical approach recommended."
    elif pipeline_fit_grade == 'D':
        recommendation = "CAUTION: IRR analysis may not be reliable. Recommend human review of Integration stage blind spots before any investment action."
    elif base_confidence == 'LOW':
        recommendation = "LOW CONFIDENCE: Multiple risk factors identified. Use IRR figures as directional guidance only."
    elif base_confidence == 'MEDIUM':
        recommendation = "MEDIUM CONFIDENCE: Some uncertainties present. Consider IRR distribution range rather than point estimate."
    else:
        recommendation = "HIGH CONFIDENCE: IRR analysis appears robust. Standard position sizing considerations apply."


    return {
        'overall_confidence': base_confidence,
        'pipeline_fit_grade': pipeline_fit_grade,
        'pipeline_fit_caveat': pipeline_fit_caveat,
        'key_uncertainties': key_uncertainties if key_uncertainties else ['No major uncertainties identified'],
        'highest_leverage_assumptions': highest_leverage,
        'flags_triggered_count': len(flags_triggered),
        'recommendation_summary': recommendation
    }


def execute_irr_workflow(
    kg,
    a7_summary,
    a9_scenario_output,
    a11_integration_trace,
    rho_estimates,
    cohort_multiples=None,  # Patch 2.3: Now optional (deprecated for TF approach)
    inside_view_adjustments=None,  # Patch 2.3: Deprecated
    scenario_multiple_impacts=None,
    hurdle_rate=0.15,
    capital_allocation='RETAIN_FCF',
    use_transition_factor=True,  # Patch 2.3: Enable TF approach (default True)
    *,  # Keyword-only after this point (preserves backward compat)
    convergence_rate=0.20,      # From A.13.convergence_rate_assessment.cr_final
    multiple_selection=None     # From A.13.multiple_selection; if None, kernel derives
):
    """
    Main API for the IRR Kernel Extension.


    Executes the full IRR analysis workflow and returns A.14_IRR_ANALYSIS artifact.


    Patch 2.3 Update: Now uses Transition Factor (TF) approach by default instead of
    cohort-based fair multiple convergence. The TF approach:
    - Uses DCF-implied multiples as the reference (not cohort P50)
    - Preserves the market-to-DCF ratio at T+1
    - Derives scenario multiple impacts from IVPS impacts
    - Produces IRR ≈ DR for fairly-valued stocks


    Parameters:
    -----------
    kg : dict
        A.2_ANALYTIC_KG artifact
    a7_summary : dict
        A.7_LIGHTWEIGHT_VALUATION_SUMMARY artifact (must contain Y0-Y3 trajectory checkpoints)
    a9_scenario_output : dict
        A.10_SCENARIO_MODEL_OUTPUT artifact (note: parameter name is legacy)
    a11_integration_trace : dict
        A.12_INTEGRATION_TRACE artifact (note: parameter name is legacy)
    rho_estimates : dict
        {scenario_id: rho} - resolution percentages (from LLM analysis)
    cohort_multiples : dict, optional
        DEPRECATED with TF approach. Only used if use_transition_factor=False.
        {'p25': float, 'p50': float, 'p75': float} - from cohort analysis
    inside_view_adjustments : list, optional
        DEPRECATED with TF approach. Only used if use_transition_factor=False.
    scenario_multiple_impacts : dict, optional
        {scenario_id: multiple_delta} - If not provided, derived from IVPS impacts
    hurdle_rate : float
        Target return rate (default 15%)
    capital_allocation : str
        Capital allocation assumption for Transition Factor calculation:
        - 'RETAIN_FCF': FCF accumulates as cash (default)
        - 'DISTRIBUTE_FCF': FCF distributed to shareholders
    use_transition_factor : bool
        If True (default), use TF approach. If False, use legacy cohort approach.
    convergence_rate : float, keyword-only
        From A.13.convergence_rate_assessment.cr_final. CR layers on top of TF 
        using additive gap closure: Adjusted_Multiple = TF_Multiple + CR × Gap.
        Range [0.10, 0.40]. Default 0.20.
    multiple_selection : dict, keyword-only
        From A.13.multiple_selection. If None, kernel derives from fundamentals.


    Returns:
    --------
    dict : A.14_IRR_ANALYSIS artifact
    """
    # CR validation
    if convergence_rate is None:
        convergence_rate = 0.20  # Default to base rate
    if not (0.10 <= convergence_rate <= 0.40):
        raise ValueError(
            f"convergence_rate must be in [0.10, 0.40], got {convergence_rate}. "
            f"Values outside this range require variance justification in A.13."
        )

    print(f"IRR Kernel Execution Started (Version: {KERNEL_VERSION})...")


    # -------------------------------------------------------------------------
    # Phase 0: Extract inputs from CVR State 4 Bundle
    # -------------------------------------------------------------------------
    print("Phase 0: Extracting from State 4 Bundle...")


    # Primary source: state_4_active_inputs (pre-merged by Integration)
    state_4_inputs = a11_integration_trace.get('state_4_active_inputs', {})


    # Market data from bundle (preferred) with kg fallback
    market_snapshot = state_4_inputs.get('market_data_snapshot', {})
    price_t0 = market_snapshot.get('current_price') or kg.get('market_context', {}).get('Current_Stock_Price')
    shares_outstanding = market_snapshot.get('shares_outstanding_fdso') or kg.get('share_data', {}).get('shares_out_diluted_tsm')
    net_debt = market_snapshot.get('net_debt_y0')


    if net_debt is None:
        # Fallback to kg capital structure
        capital_structure = kg.get('capital_structure', {}).get('net_debt_y0', {})
        net_debt = capital_structure.get('gross_debt', 0) - capital_structure.get('cash_equivalents', 0)


    market_cap = price_t0 * shares_outstanding if price_t0 and shares_outstanding else 0


    market_data = {
        'current_price': price_t0,
        'shares_outstanding': shares_outstanding,
        'market_cap': market_cap,
        'net_debt': net_debt
    }


    # Valuation anchor from bundle
    valuation_anchor = state_4_inputs.get('valuation_anchor', {})
    e_ivps_state4 = valuation_anchor.get('e_ivps_state4')
    dr_static = valuation_anchor.get('dr_static')
    base_case_ivps_state2 = valuation_anchor.get('base_case_ivps_state2')


    # Fallback to A.7 if bundle incomplete
    if e_ivps_state4 is None:
        ivps_summary = a7_summary.get('ivps_summary', {})
        e_ivps_state4 = ivps_summary.get('IVPS', 0)
        logger.warning("e_ivps_state4 missing from bundle; using A.7 IVPS")


    if dr_static is None:
        dr_static = a7_summary.get('ivps_summary', {}).get('DR_Static', 0.10)
        if isinstance(dr_static, dict):
            dr_static = dr_static.get('value', 0.10)
        logger.warning("dr_static missing from bundle; using A.7")


    # Fundamentals from bundle trajectory
    fundamentals_trajectory = state_4_inputs.get('fundamentals_trajectory', {})
    y0_data = fundamentals_trajectory.get('Y0', {})
    y1_data = fundamentals_trajectory.get('Y1')


    # Fallback to A.7 if bundle trajectory incomplete
    if not y1_data:
        trajectory = a7_summary.get('forecast_trajectory_checkpoints', {})
        y1_data = trajectory.get('Y1')
        if y1_data:
            logger.warning("Using A.7 trajectory; prefer state_4_active_inputs.fundamentals_trajectory")


    if not y1_data:
        raise ValueError("Y1 fundamentals required but missing from bundle and A.7")


    # Fallback Y0 to kg if bundle incomplete
    if not y0_data:
        y0_data = kg.get('core_data', {}).get('Y0_data', {})


    # Normalize Y0 fundamentals
    fundamentals_y0 = {
        'revenue': y0_data.get('Revenue', 0),
        'ebitda': y0_data.get('EBITDA', 0),
        'fcf': y0_data.get('FCF_Unlevered', 0)
    }


    # Normalize Y1 fundamentals
    fundamentals_t1 = {
        'revenue': y1_data.get('Revenue', 0),
        'ebitda': y1_data.get('EBITDA', 0),
        'fcf': y1_data.get('FCF_Unlevered', 0),
        'nopat': y1_data.get('NOPAT', 0)
    }


    # Input validation
    if price_t0 is None or price_t0 <= 0:
        raise ValueError(f"Invalid price_t0: {price_t0}")
    if shares_outstanding is None or shares_outstanding <= 0:
        raise ValueError(f"Invalid shares_outstanding: {shares_outstanding}")
    if e_ivps_state4 is None or e_ivps_state4 <= 0:
        raise ValueError(f"Invalid e_ivps_state4: {e_ivps_state4}")
    if fundamentals_t1.get('revenue', 0) <= 0:
        raise ValueError(f"Invalid Y1 revenue: {fundamentals_t1.get('revenue')}")


    # Calculate growth and margins
    if fundamentals_y0['revenue'] > EPSILON:
        fundamentals_t1['revenue_growth'] = (
            fundamentals_t1['revenue'] / fundamentals_y0['revenue'] - 1
        )
    if fundamentals_t1['revenue'] > EPSILON:
        fundamentals_t1['ebitda_margin'] = (
            fundamentals_t1['ebitda'] / fundamentals_t1['revenue']
        )


    # Extract scenarios from State 4 Bundle (preferred) or A.10 fallback
    # Bundle path: state_4_active_inputs.scenarios_finalized (post-adjudication)
    # A.10 path: scenario_definitions (pre-adjudication)
    # Note: state_4_inputs already extracted in Phase 0 above
    scenarios = state_4_inputs.get('scenarios_finalized')


    if not scenarios:
        # Fallback to A.10 schema path
        scenarios = a9_scenario_output.get('scenario_definitions', [])
        if scenarios:
            logger.warning("Using scenario_definitions from A.10; prefer scenarios_finalized from bundle")


    if not scenarios:
        raise ValueError("No scenarios found in state_4_active_inputs.scenarios_finalized or A.10.scenario_definitions")


    # Multiple selection
    multiple_selection = select_valuation_multiples(fundamentals_t1)
    primary_metric = multiple_selection['primary']['metric']


    # -------------------------------------------------------------------------
    # Phase 1: Transition Factor Calculation (Patch 2.3)
    # -------------------------------------------------------------------------
    print("Phase 1: Calculating Transition Factor and null case...")


    # Calculate current market multiple
    market_multiple_result = calculate_market_multiple_t0(
        market_data, fundamentals_y0, primary_metric
    )
    market_multiple_t0 = market_multiple_result.get('market_multiple_t0', 0)


    if market_multiple_t0 is None or market_multiple_t0 <= EPSILON:
        logger.warning("Could not calculate market multiple T0; using fallback")
        market_multiple_t0 = 5.0  # Fallback


    # Get base metric values for TF calculation
    metric_map_y0 = {
        'EV_Revenue': fundamentals_y0.get('revenue', 0),
        'EV_EBITDA': fundamentals_y0.get('ebitda', 0),
        'EV_FCF': fundamentals_y0.get('fcf', 0)
    }
    metric_map_t1 = {
        'EV_Revenue': fundamentals_t1.get('revenue', 0),
        'EV_EBITDA': fundamentals_t1.get('ebitda', 0),
        'EV_FCF': fundamentals_t1.get('fcf', 0)
    }
    metric_t0 = metric_map_y0.get(primary_metric, fundamentals_y0.get('revenue', 0))
    metric_t1 = metric_map_t1.get(primary_metric, fundamentals_t1.get('revenue', 0))


    # Calculate Transition Factor
    tf_result = calculate_transition_factor(
        ivps_t0=e_ivps_state4,
        dr_static=dr_static,
        fcf_y1=fundamentals_t1.get('fcf', 0),
        net_debt_t0=net_debt,
        fdso=shares_outstanding,
        metric_t0=metric_t0,
        metric_t1=metric_t1,
        capital_allocation=capital_allocation
    )


    transition_factor = tf_result['transition_factor']
    dcf_multiple_t0 = tf_result['dcf_multiple_t0']
    dcf_multiple_t1 = tf_result['dcf_multiple_t1']


    # Calculate market-to-DCF ratio (diagnostic)
    market_dcf_ratio = market_multiple_t0 / dcf_multiple_t0 if dcf_multiple_t0 > EPSILON else 1.0


    # Calculate null case market multiple at T+1 (no scenario resolution)
    null_market_multiple_t1 = market_multiple_t0 * transition_factor

    # -------------------------------------------------------------------------
    # CR Layering: Additive Gap Closure
    # -------------------------------------------------------------------------
    # CR determines what fraction of the market-to-DCF gap closes by T+1
    gap_t1 = dcf_multiple_t1 - null_market_multiple_t1
    cr_contribution = convergence_rate * gap_t1
    adjusted_market_multiple_t1 = null_market_multiple_t1 + cr_contribution

    # Use adjusted multiple for null case price calculation
    null_ev_t1 = metric_t1 * adjusted_market_multiple_t1
    null_equity_t1 = null_ev_t1 - tf_result['net_debt_t1']
    null_price_t1 = null_equity_t1 / shares_outstanding if shares_outstanding > EPSILON else 0
    null_price_t1 = max(0, null_price_t1)  # Limited liability


    null_irr = (null_price_t1 / price_t0) - 1 if price_t0 > EPSILON else 0


    # Build null case structure (compatible with existing code)
    # Note: For TF approach, "fair_multiple" is the DCF-implied multiple, not cohort-based
    null_case = {
        'fundamentals_t1': fundamentals_t1,
        'current_multiple': market_multiple_t0,
        'fair_multiple': dcf_multiple_t1,  # DCF-implied, not cohort
        'convergence_rate': convergence_rate,  # From A.13 CR assessment
        'expected_multiple_t1': null_market_multiple_t1,
        'price_t1': null_price_t1,
        'irr_decomposition': {
            'fundamental_growth_irr': 0,  # Deprecated decomposition
            'multiple_convergence_irr': 0,  # Deprecated decomposition  
            'scenario_resolution_irr': 0,
            'total_irr': null_irr
        },
        'convergence_dependency_ratio': 0,  # Not applicable for TF
        'valuation_t1': {
            'ev': null_ev_t1,
            'net_debt': tf_result['net_debt_t1'],
            'equity_value': null_equity_t1,
            'shares_outstanding': shares_outstanding,
            'price_t1': null_price_t1
        },
        # Patch 2.3: TF-specific fields
        'transition_factor_analysis': {
            'market_multiple_t0': market_multiple_t0,
            'dcf_multiple_t0': dcf_multiple_t0,
            'market_dcf_ratio': market_dcf_ratio,
            'transition_factor': transition_factor,
            'market_multiple_t1_null': null_market_multiple_t1,
            'dcf_multiple_t1': dcf_multiple_t1,
            'ivps_t0': e_ivps_state4,
            'ivps_t1': tf_result['ivps_t1'],
            'dr_static': dr_static,
            'calculation_trace': tf_result['calculation_trace'],
            'convergence_rate_applied': convergence_rate,
            'gap_t1': gap_t1,
            'cr_contribution': cr_contribution,
            'adjusted_market_multiple_t1': adjusted_market_multiple_t1
        }
    }


    # -------------------------------------------------------------------------
    # Phase 2 & 3: Fork generation
    # -------------------------------------------------------------------------
    print("Phase 2-3: Generating forks...")


    # Reconstruct JPD states
    scenario_ids = [s.get('scenario_id') for s in scenarios]


    # Build constraints from A.10
    constraints = {
        'mutual_exclusivity_groups': a9_scenario_output.get('constraints', {}).get(
            'mutual_exclusivity_groups', []
        ),
        'economic_incompatibilities': a9_scenario_output.get('constraints', {}).get(
            'economic_incompatibilities', []
        ),
        'causal_dependencies': []
    }


    # P4 Patch: Extract Pipeline Fit grade from A.11
    integration_summary = a11_integration_trace.get('metadata', {}).get('integration_summary', {})
    pipeline_fit_grade = integration_summary.get('pipeline_fit_grade', 'UNKNOWN')


    pipeline_fit_caveats = {
        'A': None,
        'B': None,
        'C': "Material blind spots identified in upstream valuation; interpret IRR distribution with caution.",
        'D': "WARNING: Multiple severe blind spots flagged in Integration stage. IRR figures may not be reliable for investment decisions.",
        'F': "BLOCK RECOMMENDATION PROPAGATED: DCF+SSE methodology deemed inappropriate for this security. IRR analysis provided for completeness only—do not use for investment decisions.",
        'UNKNOWN': "Pipeline Fit grade not available from Integration stage; interpret with caution."
    }
    pipeline_fit_caveat = pipeline_fit_caveats.get(pipeline_fit_grade, pipeline_fit_caveats['UNKNOWN'])


    # Recalculate JPD for fork generation
    sse_result = calculate_sse_jpd(scenarios, constraints, e_ivps_state4)
    jpd_states = sse_result['states']


    # Patch 2.3: Calculate scenario multiple impacts from IVPS (not cohort spread)
    if scenario_multiple_impacts is None:
        scenario_multiple_impacts = calculate_scenario_multiple_impacts_from_ivps(
            scenarios=scenarios,
            fdso=shares_outstanding,
            base_metric_t1=metric_t1
        )


    # Build scenario fundamentals map (Patch 2.1)
    scenario_fundamentals_map = build_scenario_fundamentals_map(scenarios)


    # Generate forks using TF-based approach
    forks = generate_irr_forks_tf(
        scenarios=scenarios,
        jpd_states=jpd_states,
        rho_estimates=rho_estimates,
        null_case=null_case,
        scenario_multiple_impacts=scenario_multiple_impacts,
        market_data=market_data,
        price_t0=price_t0,
        multiple_selection=multiple_selection,
        scenario_fundamentals_map=scenario_fundamentals_map,
        transition_factor=transition_factor,
        market_multiple_t0=market_multiple_t0,
        tf_result=tf_result
    )


    # -------------------------------------------------------------------------
    # Phase 4: Integration
    # -------------------------------------------------------------------------
    print("Phase 4: Integrating IRR distribution...")


    irr_integration = calculate_irr_distribution(forks, null_irr)


    # P(IRR > hurdle)
    prob_above_hurdle = sum(
        f['fork_probability'] for f in forks
        if f['fork_irr'] >= hurdle_rate
    )


    # P(loss)
    prob_of_loss = sum(
        f['fork_probability'] for f in forks
        if f['fork_irr'] < 0
    )


    # -------------------------------------------------------------------------
    # Phase 5: Sanity checks
    # -------------------------------------------------------------------------
    print("Phase 5: Running sanity checks...")


    sanity_checks = run_sanity_checks(
        null_case=null_case,
        forks=forks,
        rho_estimates=rho_estimates,
        price_t0=price_t0,
        market_data=market_data,
        multiple_selection=multiple_selection,
        hurdle_rate=hurdle_rate
    )


    # -------------------------------------------------------------------------
    # Compile A.14 artifact (Patch 2.3: Updated structure)
    # -------------------------------------------------------------------------
    print("Compiling A.14_IRR_ANALYSIS artifact...")


    a14_artifact = {
        'schema_version': KERNEL_VERSION,
        'metadata': {
            'company_name': kg.get('company_name', ''),
            'ticker': kg.get('ticker', ''),
            'analysis_date': a11_integration_trace.get('metadata', {}).get('valuation_date'),
            'current_price_p0': price_t0,
            'horizon': 'T+1',
            'source_cvr_state': 'STATE_4',
            'hurdle_rate': hurdle_rate,
            'pipeline_fit_grade': pipeline_fit_grade,
            'pipeline_fit_caveat': pipeline_fit_caveat,
            'methodology': 'TRANSITION_FACTOR'  # Patch 2.3
        },
        # Patch 2.3: New transition_factor_analysis section replaces anchor_establishment
        'transition_factor_analysis': null_case['transition_factor_analysis'],
        'null_case_analysis': {
            'fundamentals_t1': fundamentals_t1,
            'market_multiple_t0': market_multiple_t0,
            'dcf_implied_multiple_t0': dcf_multiple_t0,
            'market_dcf_ratio_t0': market_dcf_ratio,
            'transition_factor': transition_factor,
            'market_multiple_t1_null': null_market_multiple_t1,
            'dcf_implied_multiple_t1': dcf_multiple_t1,
            'null_case_irr': null_irr,
            'expected_price_t1_null': null_price_t1,
            'interpretation': _interpret_null_irr(null_irr, dr_static, market_dcf_ratio)
        },
        'fork_analysis': {
            'multiple_selection': multiple_selection,
            'scenario_multiple_impacts': scenario_multiple_impacts,
            'forks': forks
        },
        'irr_integration': {
            'e_irr': irr_integration['e_irr'],
            'irr_distribution': irr_integration['irr_distribution'],
            'probability_above_hurdle': prob_above_hurdle,
            'probability_of_loss': prob_of_loss,
            # Patch 2.3: Simplified decomposition
            'return_attribution': {
                'null_case_irr': null_irr,
                'scenario_resolution_contribution': irr_integration['scenario_resolution_contribution'],
                'total_e_irr': irr_integration['e_irr']
            }
        },
        'sanity_checks': sanity_checks,
        'confidence_assessment': _generate_confidence_assessment(
            pipeline_fit_grade=pipeline_fit_grade,
            pipeline_fit_caveat=pipeline_fit_caveat,
            sanity_checks=sanity_checks,
            null_case=null_case,
            irr_integration=irr_integration,
            cr=convergence_rate
        )
    }


    print("IRR Kernel Execution Completed.")
    return a14_artifact


# ==========================================================================================
# END OF IRR EXTENSION MODULE
# ==========================================================================================