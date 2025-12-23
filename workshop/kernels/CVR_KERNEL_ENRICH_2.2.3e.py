# ==========================================================================================
# CVR KERNEL G3_2.2.2e_ENRICH (ENRICHMENT Implementation)
# Extended from G3_2.2.2e BASE with S_CURVE and MULTI_STAGE_FADE DSL support
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
# Patch 2.2.3e: Terminal g derived from topline growth (not ROIC/NOPAT)
#               Reinvestment uses ROIC_anchor from A.1 (not modeled ROIC)
#               See: PATCH-2024-12-22-001 Section 7
FORECAST_YEARS = 20
EPSILON = 1e-9
KERNEL_VERSION = "G3_2.2.3e_ENRICH"
SENSITIVITY_TORNADO_TOP_N = 5
TERMINAL_G_RFR_CAP = True  # If True, Terminal g is also capped at RFR

# Terminal g derived from topline growth, capped at GDP × multiplier
GDP_PROXY = 0.025  # 2.5% long-term GDP growth
GDP_MULTIPLIER = 1.4  # Allow up to 1.4× GDP for share-gainers
DEFAULT_ROIC_ANCHOR = 0.15  # Industry median ROIC if not in A.1
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
            fade_steps = np.linspace(start_value, end_value, fade_years)
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
            cagr_steps = np.linspace(start_cagr, end_cagr, interp_years)
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
def calculate_apv(forecast_df, dr, kg, unit_multiplier=1):
    """Calculates the Intrinsic Value Per Share (IVPS) using the APV methodology.

    Args:
        forecast_df: DataFrame with forecasted financials
        dr: Discount rate
        kg: Analytic Knowledge Graph (A.2)
        unit_multiplier: Scale factor for GIM units (1000 for 'thousands', etc.)
                        Applied to equity_value before dividing by FDSO.
    """
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
    # 4. Determine Terminal Growth (g) and ROIC Anchor (r)
    # PATCH 2.2.3e: Derive g from TOPLINE growth (revenue/EBIT), NOT from ROIC/NOPAT.
    # Revenue and EBIT growth are modeled reliably; IC is accounting-dependent.
    # Use ROIC_anchor from A.1 epistemic anchors for reinvestment calculation.

    # === TERMINAL GROWTH DERIVATION (from topline) ===
    revenue_growth_rates = forecast_df['Revenue'].pct_change().values[1:]
    ebit_growth_rates = forecast_df['EBIT'].pct_change().values[1:]

    # Use average of last 3 years to smooth volatility
    revenue_g = np.mean(revenue_growth_rates[-3:]) if len(revenue_growth_rates) >= 3 else np.mean(revenue_growth_rates)
    ebit_g = np.mean(ebit_growth_rates[-3:]) if len(ebit_growth_rates) >= 3 else np.mean(ebit_growth_rates)

    # Use average of the two (not min - avoid over-conservatism)
    terminal_g_estimate = (revenue_g + ebit_g) / 2

    # Apply cap: GDP × 1.4 (allows above-GDP growth, prevents excess)
    terminal_g_cap = GDP_PROXY * GDP_MULTIPLIER  # 3.5%

    # Also respect RFR if available (natural ceiling)
    if TERMINAL_G_RFR_CAP and rfr is not None:
        terminal_g_cap = min(terminal_g_cap, rfr)

    terminal_g = min(terminal_g_estimate, terminal_g_cap)
    terminal_g = max(terminal_g, 0)  # Floor at 0

    # Final sanity check against DR
    if terminal_g >= dr:
        logger.warning(f"Terminal g ({terminal_g:.4f}) >= DR ({dr:.4f}). Capping at 80% of DR.")
        terminal_g = dr * 0.80

    logger.info(f"Terminal g: estimate={terminal_g_estimate:.4f}, cap={terminal_g_cap:.4f}, final={terminal_g:.4f}")

    # === ROIC ANCHOR (from A.1, not modeled) ===
    roic_anchor = core_data.get('ROIC_anchor', DEFAULT_ROIC_ANCHOR)
    terminal_roic_r = roic_anchor  # For output compatibility

    # === REINVESTMENT RATE ===
    if abs(roic_anchor) > EPSILON:
        reinvestment_rate_terminal = terminal_g / roic_anchor
    else:
        reinvestment_rate_terminal = 0

    # Cap reinvestment at 100% (can't reinvest more than you earn)
    reinvestment_rate_terminal = min(reinvestment_rate_terminal, 1.0)
    reinvestment_rate_terminal = max(reinvestment_rate_terminal, 0.0)

    logger.info(f"Reinvestment: g={terminal_g:.4f}, ROIC_anchor={roic_anchor:.4f}, rate={reinvestment_rate_terminal:.4f}")

    # 5. Calculate Terminal Value (Value Driver Formula)
    nopat_T_plus_1 = nopat_T * (1 + terminal_g)
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
    # PATCH 2.2.3e: Apply unit_multiplier to convert GIM-denominated equity to actual currency
    # e.g., if GIM is in thousands, equity_value is in thousands → multiply by 1000 before per-share
    ivps = (equity_value * unit_multiplier) / fdso
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
def run_sensitivity_analysis(kg, dag, seq, gim, dr, base_results, scenarios, schema_version=KERNEL_VERSION, unit_multiplier=1):
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
                valuation_results = calculate_apv(forecast_df, temp_dr, kg, unit_multiplier)
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
    The main API for the CVR Kernel G3_2.2.2e (ENRICHMENT).
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

    # Handle both wrapped {"A.5_GESTALT_IMPACT_MAP": {...}} and unwrapped {...} formats
    inner_a5 = gim_artifact.get('A.5_GESTALT_IMPACT_MAP', gim_artifact)
    gim = inner_a5.get('GIM', {})

    # PATCH 2.2.3e: Extract unit multiplier for per-share calculations
    # GIM values (Revenue, EBIT, etc.) may be in thousands/millions - must scale before dividing by share count
    unit_str = inner_a5.get('unit', 'units').lower()
    UNIT_MULTIPLIERS = {'thousands': 1000, 'millions': 1_000_000, 'billions': 1_000_000_000}
    unit_multiplier = UNIT_MULTIPLIERS.get(unit_str, 1)
    if unit_multiplier != 1:
        logger.info(f"GIM unit='{unit_str}' → multiplier={unit_multiplier:,}")
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
        valuation_results = calculate_apv(forecast_df, dr, kg, unit_multiplier)
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
                kg, dag, seq, gim, dr, valuation_results, sensitivity_scenarios, schema_version, unit_multiplier
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
# END OF CVR KERNEL G3_2.2.2e_ENRICH
# ==========================================================================================
