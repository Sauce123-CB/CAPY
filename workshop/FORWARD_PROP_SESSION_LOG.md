# Forward Propagation Session Log

> **Purpose:** Compaction-resilient reference for forward propagation work
> **Created:** 2024-12-23
> **Status:** In Progress

---

## Critical Reference Files (READ THESE AFTER COMPACTION)

### Pattern Sources (already patched - copy patterns from these)
1. `workshop/kernels/BASE_CVR_KERNEL_2.2.3e.py` - lines 26-30 (constants), 411-455 (terminal g fix)
2. `workshop/kernels/CVR_KERNEL_ENRICH_2.2.3e.py` - same pattern
3. `workshop/prompts/base/G3BASE_2.2.3e_PROMPT.md` - Section V atomized output pattern
4. `workshop/prompts/enrich/G3ENRICH_2.2.3e_PROMPT.md` - Section V atomized output pattern

### Target Files (need patching)
1. `workshop/kernels/CVR_KERNEL_SCEN_2_2_2e.py` → 2.2.3e
2. `workshop/kernels/CVR_KERNEL_INT_2_2_2e.py` → 2.2.3e
3. `workshop/kernels/CVR_KERNEL_IRR_2.2.5e.py` → 2.2.6e
4. `workshop/prompts/scenario/G3_SCENARIO_2.2.2e_PROMPT.md` → 2.2.3e
5. `workshop/prompts/integration/G3_INTEGRATION_2.2.3e_PROMPT.md` (verify/update)
6. `workshop/prompts/irr/G3_IRR_2.2.5e_PROMPT.md` → 2.2.6e

### Guides
1. `~/.claude/plans/snuggly-skipping-feigenbaum.md` - mega-patch plan (Section 7 = terminal g fix)
2. `workshop/FORWARD_PROPAGATION_CHECKLIST.md` - itemized checklist

---

## Kernel Patch Template (apply to SCEN, INT, IRR)

### 1. Add constants after KERNEL_VERSION line:
```python
# Terminal g derived from topline growth, capped at GDP × multiplier
GDP_PROXY = 0.025  # 2.5% long-term GDP growth
GDP_MULTIPLIER = 1.4  # Allow up to 1.4× GDP for share-gainers
DEFAULT_ROIC_ANCHOR = 0.15  # Industry median ROIC if not in A.1
```

### 2. Replace terminal g calculation (find `nopat_growth_rates` and replace block):
```python
# === TERMINAL GROWTH DERIVATION (from topline) ===
revenue_growth_rates = forecast_df['Revenue'].pct_change().values[1:]
ebit_growth_rates = forecast_df['EBIT'].pct_change().values[1:]

revenue_g = np.mean(revenue_growth_rates[-3:]) if len(revenue_growth_rates) >= 3 else np.mean(revenue_growth_rates)
ebit_g = np.mean(ebit_growth_rates[-3:]) if len(ebit_growth_rates) >= 3 else np.mean(ebit_growth_rates)

terminal_g_estimate = (revenue_g + ebit_g) / 2

terminal_g_cap = GDP_PROXY * GDP_MULTIPLIER  # 3.5%

if TERMINAL_G_RFR_CAP and rfr is not None:
    terminal_g_cap = min(terminal_g_cap, rfr)

terminal_g = min(terminal_g_estimate, terminal_g_cap)
terminal_g = max(terminal_g, 0)

if terminal_g >= dr:
    logger.warning(f"Terminal g ({terminal_g:.4f}) >= DR ({dr:.4f}). Capping at 80% of DR.")
    terminal_g = dr * 0.80

# === ROIC ANCHOR (from A.1, not modeled) ===
core_data_y0 = kg.get('core_data', {}).get('Y0_data', {})
roic_anchor = core_data_y0.get('ROIC_anchor', DEFAULT_ROIC_ANCHOR)
terminal_roic_r = roic_anchor

if abs(roic_anchor) > EPSILON:
    reinvestment_rate_terminal = terminal_g / roic_anchor
else:
    reinvestment_rate_terminal = 0

reinvestment_rate_terminal = min(reinvestment_rate_terminal, 1.0)
reinvestment_rate_terminal = max(reinvestment_rate_terminal, 0.0)
```

---

## Progress Log

| Time | Action | Status |
|------|--------|--------|
| Start | Created session log | Done |
| | Reading reference docs | In Progress |
