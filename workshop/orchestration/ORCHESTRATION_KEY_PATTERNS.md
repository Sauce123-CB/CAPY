# CAPY Orchestration Key Patterns

> **Version:** 1.0.0
> **Last reviewed:** 2024-12-20
> **Scope:** Patterns that propagate across all pipeline stages (BASE → RQ → ENRICH → SCENARIO → INTEGRATION → IRR)

This document defines the canonical orchestration patterns for Claude Code execution of the CAPY pipeline. These patterns must be consistently applied across all stages.

---

## Pattern 1: Subagent Direct-Write Protocol

**Problem:** Orchestrator token limits cause truncation when subagents return full outputs.

**Solution:** Subagents write output directly to disk, return only confirmation.

```
Orchestrator                              Subagent
    │                                        │
    ├─ Spawns subagent with prompt ────────► │
    │                                        ├─ Executes analysis
    │                                        ├─ Writes output to disk (Write tool)
    │                                        ├─ Returns: "Complete. File: {path}"
    ◄────────────────────────────────────────┤
    ├─ Verifies file exists
    ├─ Reports to user
```

**Implementation:**
- Subagent prompt MUST include explicit output path
- Subagent MUST use Write tool before returning
- Subagent returns confirmation + filepath only (not full content)
- Orchestrator verifies file exists after completion

---

## Pattern 2: Source of Truth Chain

**Problem:** Each stage needs complete inputs from prior stages; incomplete inputs cause artifact truncation.

**Solution:** Explicit source-of-truth mapping for each stage.

| Stage | Source of Truth Input | Contains |
|-------|----------------------|----------|
| BASE_T1 | `00_source/*.extracted.md` | Company documents |
| BASE_REFINE | `01_T1/{TICKER}_BASE_T1.md` | T1 artifacts + narratives |
| BASE_T2 | `02_REFINE/{TICKER}_BASE_REFINE.md` | Complete A.1-A.6 (9-driver GIM) |
| RQ_GEN | `02_REFINE` + `03_T2` | REFINE artifacts + State 1 IVPS |
| ENRICH_T1 | `02_REFINE` + `03_T2` + `04_RQ/RQ*.md` | BASE artifacts + RQ evidence |
| ENRICH_T2 | `05_ENRICH/{TICKER}_ENRICH_T1.md` | ENRICH T1 artifacts |
| SCENARIO | `05_ENRICH/{TICKER}_ENRICH_T2.md` | State 2 artifacts |

**Critical:** REFINE output (not T1) is the source of truth for artifacts A.1-A.6. T2 output contains A.7 only.

---

## Pattern 3: Two-Shot Architecture

**Problem:** Single-turn execution causes context pollution, attention degradation, and conflation of synthesis with computation.

**Solution:** Separate T1 (synthesis) and T2 (execution) into distinct subagent instances.

**Turn 1 (Analytical Synthesis):**
- Deep reasoning, evidence integration, Bayesian synthesis
- Produces narratives (N1-N5) and artifacts (A.1-A.6)
- Kernel provided for REFERENCE CONTEXT ONLY (semantic alignment)
- Does NOT compute A.7 or execute kernel

**Turn 2 (Validation & Execution):**
- Validates JSON integrity
- Repairs malformed JSON if needed
- Executes kernel via Bash
- Produces A.7 (valuation summary)
- Emits unified MRC State N report

**Rationale:**
- Turn 1 focuses on reasoning without computational overhead
- Turn 2 provides validation layer before deterministic execution
- Fresh instances prevent context pollution

---

## Pattern 4: Orchestrator Embed vs Subagent Read

**Problem:** Large documents overflow orchestrator context; small documents waste subagent file I/O.

**Solution:** Orchestrator embeds prompts and prior-stage artifacts; subagent reads source documents.

**Orchestrator EMBEDS (small, structured):**
- Prompt files (atomized: PROMPT, SCHEMAS, NORMDEFS)
- Kernel file (.py)
- Prior-stage outputs (T1.md, REFINE.md, T2.md)
- Research plan (A.8 JSON)

**Subagent READS from disk (large, unstructured):**
- Source documents (`*.extracted.md`)
- Visual data (`*_pages/*.png`)
- RQ research outputs (`RQ*.md`)

**Implementation:**
- Orchestrator reads and embeds small files in subagent prompt
- Orchestrator provides file PATHS for large files
- Subagent uses Read tool to load large files itself

---

## Pattern 5: T2 JSON Repair

**Problem:** T1 may produce malformed JSON due to context limits or attention issues.

**Solution:** T2 has explicit authority to repair JSON before kernel execution.

**T2 Validation Responsibilities:**
1. Parse all JSON artifacts from T1
2. If parse fails: Repair malformation (missing brackets, trailing commas, etc.)
3. Verify internal consistency:
   - DAG coverage (all GIM drivers appear in DAG)
   - GIM-KG alignment (driver params reference valid KG fields)
   - DR consistency (X components sum correctly)
4. Write validated/repaired artifacts as individual JSON files
5. Execute kernel with validated inputs

**Documentation:** Any repairs MUST be noted in output (what was fixed, why).

---

## Pattern 6: Kernel Execution via Bash

**Problem:** Subagents fabricate kernel output instead of executing Python.

**Solution:** T2 subagent executes kernel via Bash tool, not manual calculation.

**Implementation:**
```python
# T2 subagent runs this via Bash tool:
python -c "
import json
import importlib.util

spec = importlib.util.spec_from_file_location(
    'kernel', 'kernels/CVR_KERNEL_{STAGE}_{VERSION}.py')
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)

# Load validated artifacts
kg = json.load(open('{output_dir}/A2_ANALYTIC_KG.json'))
dag = json.load(open('{output_dir}/A3_CAUSAL_DAG.json'))
gim = json.load(open('{output_dir}/A5_GESTALT_IMPACT_MAP.json'))
dr = json.load(open('{output_dir}/A6_DR_DERIVATION_TRACE.json'))

result = kernel.execute_cvr_workflow(kg, dag, gim, dr, sensitivity_scenarios)

json.dump(result, open('{output_dir}/A7_kernel_output.json', 'w'), indent=2)
print(json.dumps(result, indent=2))
"
```

**Prohibited:**
- Manual DCF calculations
- Inventing kernel output
- Skipping Python execution

**Error Handling:** If Bash fails, report error - do not fabricate results.

---

## Pattern 7: Validator Agents

**Problem:** Errors propagate across stages without detection.

**Solution:** Opus validator subagent after each T1 and T2.

**Validator Responsibilities:**
1. Output structure (non-empty, has headers, not truncated)
2. Artifacts present (all required artifacts for stage)
3. JSON valid (all JSON blocks parse)
4. Sanity bounds (DR 5-16%, IVPS > 0, g < DR)
5. No fabrication (T1/REFINE don't contain kernel-computed values)
6. Cross-stage consistency (values persist correctly)

**Output:** JSON with `"proceed": true/false` and detailed check results.

**Pipeline Behavior:**
- `"proceed": true` → Continue to next stage
- `"proceed": false` → HALT pipeline, report issues to user

**Model Selection:** Always use Opus (Haiku misses subtle fabrication issues).

---

## Pattern 8: Atomized Prompt Files

**Problem:** Monolithic prompts cause missing-middle attention issues.

**Solution:** Split each stage prompt into 3-4 atomic files.

**Standard Atomization:**
| File | Purpose | Content |
|------|---------|---------|
| `{STAGE}_{VERSION}_PROMPT.md` | Core instructions | Sections I-V (mission, workflow, output mandate) |
| `{STAGE}_{VERSION}_SCHEMAS.md` | JSON schemas | Appendix A (all artifact schemas) |
| `{STAGE}_{VERSION}_NORMDEFS.md` | DSL definitions | Appendix B (driver modes, financial defs) |
| `CVR_KERNEL_{STAGE}_{VERSION}.py` | Computation kernel | Python code for deterministic execution |

**Loading:** Orchestrator embeds all 4 files in subagent prompt.

---

## Pattern 9: Pipeline State Tracking

**Problem:** Multi-stage pipelines lose track of completed work.

**Solution:** `pipeline_state.json` as single source of truth.

**State File Structure:**
```json
{
  "ticker": "DAVE",
  "company_name": "Dave Inc.",
  "run_id": "DAVE_CAPY_20241220_143022",
  "completed_turns": ["T1", "REFINE", "T2", "RQ_GEN", "RQ_ASK", "ENRICH_T1", "ENRICH_T2"],
  "current_turn": null,
  "validation_results": {
    "T1": "PASS",
    "REFINE": "PASS",
    "T2": "WARN"
  },
  "outputs": {
    "T1": "01_T1/DAVE_BASE_T1.md",
    "REFINE": "02_REFINE/DAVE_BASE_REFINE.md"
  }
}
```

**Rules:**
- Update after each stage completion
- Read before executing any command
- Never lose track of state

---

## Stage-Specific Applications

### BASE Stage
- T1: Subagent reads source docs, writes T1.md
- REFINE: Subagent reads T1 + source docs, writes REFINE.md (SOURCE OF TRUTH for A.1-A.6)
- T2: Orchestrator extracts artifacts → JSON, executes kernel via Bash, formats T2.md

### RQ Stage
- RQ_GEN: Subagent reads REFINE + T2, writes A.8 JSON
- RQ_ASK: 7 parallel subagents, each writes RQ{N}.md directly to disk

### ENRICH Stage
- T1: Subagent reads REFINE + T2 + A.8 + RQ*.md, writes ENRICH_T1.md
- Validator: Opus validator checks T1 output
- T2: Subagent repairs JSON, executes kernel via Bash, writes ENRICH_T2.md
- Validator: Opus validator checks T2 output

### SCENARIO / INTEGRATION / IRR
- Same patterns apply
- Source of truth chains forward from prior stage

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2024-12-20 | Initial extraction from production/CLAUDE.md and session learnings |
