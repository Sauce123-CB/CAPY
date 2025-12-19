# A.8 Research Plan Validator

## Purpose

Validate and repair the A.8_RESEARCH_STRATEGY_MAP artifact before passing to RQ_ASK execution. This validator attempts to fix malformed JSON before failing.

## Input

You receive text that should be a JSON object conforming to the A.8 schema from RQ_GEN.

---

## STEP 0: JSON Parsing and Repair (MANDATORY FIRST STEP)

Before any validation, attempt to parse the input as JSON. If parsing fails, attempt repairs.

### Common Issues and Repairs

| Issue | Repair |
|-------|--------|
| Markdown code fences (```json ... ```) | Strip the fences, extract JSON content |
| Trailing commas in arrays/objects | Remove trailing commas |
| Single quotes instead of double quotes | Replace with double quotes |
| Unescaped quotes in strings | Escape them |
| Missing closing braces/brackets | Add them based on structure |
| JavaScript-style comments (// or /* */) | Remove comments |
| Unquoted keys | Add quotes around keys |
| Truncated JSON (incomplete) | If >80% complete, attempt to close structures |

### Repair Procedure

1. **Try direct parse** - If it works, proceed to validation
2. **Strip markdown** - Remove ```json and ``` wrappers if present
3. **Fix common syntax errors** - Apply repairs from table above
4. **Re-attempt parse** - Try parsing the repaired JSON
5. **If still failing** - Report FAIL with specific parse error location

### Repair Output

If repairs were made, include in output:
```json
{
  "json_repair": {
    "required": true,
    "repairs_applied": ["stripped markdown fences", "removed trailing comma"],
    "original_error": "Unexpected token at position 1523"
  }
}
```

---

## STEP 1: Schema Conformance

Check that the following structure exists:

```json
{
  "A.8_RESEARCH_STRATEGY_MAP": {
    "schema_version": "G3_2.2.3",
    "Uncertainty_Nexus_Analysis": {
      "Lynchpins": [...]
    },
    "Scenario_Candidates": {
      "Mainline": [...],
      "Tail_Blue_Sky": [...],
      "Tail_Black_Swan": [...]
    },
    "Research_Plan": [...],
    "Platform_Summary": {
      "Total_Queries": 7,
      "Mandatory_Count": 4,
      "Dynamic_Count": 3,
      "Execution_Mode": "parallel"
    }
  }
}
```

**Required fields per Research_Plan item:**
- `RQ_ID` (string, format: "RQ1" through "RQ7")
- `Allocation_Type` (string, value: "MANDATORY" or "DYNAMIC")
- `Coverage_Objective` (string, e.g., "M-1", "M-2", "M-3a", "M-3b", or Lynchpin ID)
- `Platform` (string, "CLAUDE" or "GDR")
- `Platform_Rationale` (string, non-empty)
- `A7_Linkage` (string, non-empty)
- `Prompt_Text` (string, non-empty, >50 characters)

---

## STEP 2: Count Validation

- [ ] Exactly 7 items in Research_Plan array
- [ ] Exactly 4 MANDATORY allocations (M-1, M-2, M-3a, M-3b)
- [ ] Exactly 3 DYNAMIC allocations
- [ ] Platform values are either "CLAUDE" or "GDR"

---

## STEP 3: Mandatory Coverage Check

- [ ] M-1 (Integrity Check) is present
- [ ] M-2 (Adversarial Synthesis) is present
- [ ] M-3a (Mainline Scenario H.A.D.) is present
- [ ] M-3b (Tail Scenario H.A.D.) is present

---

## STEP 4: Scenario Candidate Validation

- [ ] Scenario_Candidates.Mainline has exactly 4 items
- [ ] Scenario_Candidates.Tail_Blue_Sky has exactly 2 items
- [ ] Scenario_Candidates.Tail_Black_Swan has exactly 2 items
- [ ] Each scenario has ID, Description, and Source fields

---

## STEP 5: Retrieval-Only Mandate

Scan each `Prompt_Text` for forbidden analytic verbs. Flag if found:

**Forbidden verbs:** analyze, assess, evaluate, predict, interpret, determine, conclude, estimate probability, judge, recommend

**Acceptable verbs:** retrieve, extract, list, find, identify, locate, compile, quote, search, gather, research, compare

---

## STEP 6: Query Quality

For each Prompt_Text:
- [ ] Length > 100 characters (substantive query)
- [ ] Contains company name or ticker
- [ ] Contains time constraint or scope limitation
- [ ] Does not ask for opinions or predictions

---

## Output Format

```json
{
  "validation_result": "PASS" | "FAIL",
  "timestamp": "ISO-8601",
  "schema_version": "G3_2.2.3",
  "json_repair": {
    "required": true | false,
    "repairs_applied": ["list of repairs"] | [],
    "original_error": "string" | null
  },
  "repaired_json": { ... } | null,
  "checks": {
    "json_parseable": true | false,
    "schema_conformance": true | false,
    "count_validation": true | false,
    "mandatory_coverage": true | false,
    "scenario_candidates": true | false,
    "retrieval_only": true | false,
    "query_quality": true | false
  },
  "issues": [
    {
      "severity": "ERROR" | "WARNING",
      "check": "string",
      "message": "string",
      "rq_id": "string (optional)"
    }
  ],
  "summary": "string (1-2 sentence summary)"
}
```

**IMPORTANT:** If repairs were made and JSON is now valid, include the `repaired_json` field with the corrected A.8. This repaired version should be used for RQ_ASK execution.

---

## Decision Logic

- **PASS**: JSON parseable (after repairs if needed), all checks pass or only WARNING-level issues
- **FAIL**: JSON unparseable after repair attempts, OR any ERROR-level issue in validation

---

## Examples

### PASS with Repair Example
```json
{
  "validation_result": "PASS",
  "schema_version": "G3_2.2.3",
  "json_repair": {
    "required": true,
    "repairs_applied": ["stripped markdown fences", "removed trailing comma on line 45"],
    "original_error": "Unexpected token '}' at position 1847"
  },
  "repaired_json": { "A.8_RESEARCH_STRATEGY_MAP": { ... } },
  "checks": {
    "json_parseable": true,
    "schema_conformance": true,
    "count_validation": true,
    "mandatory_coverage": true,
    "scenario_candidates": true,
    "retrieval_only": true,
    "query_quality": true
  },
  "issues": [],
  "summary": "A.8 required JSON repair (trailing comma). After repair, all checks pass. 7 queries ready for execution."
}
```

### PASS (No Repair Needed) Example
```json
{
  "validation_result": "PASS",
  "schema_version": "G3_2.2.3",
  "json_repair": {
    "required": false,
    "repairs_applied": [],
    "original_error": null
  },
  "repaired_json": null,
  "checks": {
    "json_parseable": true,
    "schema_conformance": true,
    "count_validation": true,
    "mandatory_coverage": true,
    "scenario_candidates": true,
    "retrieval_only": true,
    "query_quality": true
  },
  "issues": [],
  "summary": "A.8 is valid. 7 queries ready for parallel execution."
}
```

### FAIL (Unrepairable JSON) Example
```json
{
  "validation_result": "FAIL",
  "schema_version": "G3_2.2.3",
  "json_repair": {
    "required": true,
    "repairs_applied": ["stripped markdown fences", "attempted brace matching"],
    "original_error": "Unterminated string starting at position 892"
  },
  "repaired_json": null,
  "checks": {
    "json_parseable": false,
    "schema_conformance": false,
    "count_validation": false,
    "mandatory_coverage": false,
    "scenario_candidates": false,
    "retrieval_only": false,
    "query_quality": false
  },
  "issues": [
    {
      "severity": "ERROR",
      "check": "json_parseable",
      "message": "JSON repair failed. Unterminated string in Prompt_Text for RQ3. Content appears truncated."
    }
  ],
  "summary": "A.8 JSON is malformed and could not be repaired. RQ_GEN output may have been truncated."
}
```

### FAIL (Valid JSON, Failed Validation) Example
```json
{
  "validation_result": "FAIL",
  "schema_version": "G3_2.2.3",
  "json_repair": {
    "required": false,
    "repairs_applied": [],
    "original_error": null
  },
  "repaired_json": null,
  "checks": {
    "json_parseable": true,
    "schema_conformance": true,
    "count_validation": false,
    "mandatory_coverage": true,
    "scenario_candidates": false,
    "retrieval_only": false,
    "query_quality": true
  },
  "issues": [
    {
      "severity": "ERROR",
      "check": "count_validation",
      "message": "Research_Plan contains 6 items, expected 7"
    },
    {
      "severity": "ERROR",
      "check": "scenario_candidates",
      "message": "Scenario_Candidates.Mainline has 3 items, expected 4"
    },
    {
      "severity": "ERROR",
      "check": "retrieval_only",
      "message": "RQ4 Prompt_Text contains forbidden verb 'analyze'",
      "rq_id": "RQ4"
    }
  ],
  "summary": "A.8 validation failed. 3 errors must be fixed before RQ_ASK execution."
}
```

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 2.2.3 | 2024-12-19 | Updated for 7-slot architecture; Added M-3a/M-3b mandatory coverage; Added Scenario_Candidates validation; Updated examples |
| 2.2.2 | 2024-12-17 | Initial 6-slot validator with M-1/M-2/M-3 coverage |
