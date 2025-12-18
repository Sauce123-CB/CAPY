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
    "schema_version": "G3_2.2.2",
    "Uncertainty_Nexus_Analysis": {
      "Lynchpins": [...]
    },
    "Research_Plan": [...],
    "Platform_Summary": {
      "GDR_Count": 6,
      "Execution_Mode": "parallel"
    }
  }
}
```

**Required fields per Research_Plan item:**
- `RQ_ID` (string, format: "RQ1" through "RQ6")
- `Allocation_Type` (string, value: "MANDATORY" or "DYNAMIC")
- `Coverage_Objective` (string, e.g., "M-1", "M-2", "M-3", or Lynchpin ID)
- `Platform` (string, must be "GDR")
- `Platform_Rationale` (string, non-empty)
- `A7_Linkage` (string, non-empty)
- `Prompt_Text` (string, non-empty, >50 characters)

---

## STEP 2: Count Validation

- [ ] Exactly 6 items in Research_Plan array
- [ ] Exactly 3 MANDATORY allocations (M-1, M-2, M-3)
- [ ] Exactly 3 DYNAMIC allocations
- [ ] All Platform values are "GDR"

---

## STEP 3: Mandatory Coverage Check

- [ ] M-1 (Integrity Check) is present
- [ ] M-2 (Adversarial Synthesis) is present
- [ ] M-3 (Scenario H.A.D.) is present

---

## STEP 4: Retrieval-Only Mandate

Scan each `Prompt_Text` for forbidden analytic verbs. Flag if found:

**Forbidden verbs:** analyze, assess, evaluate, predict, interpret, determine, conclude, estimate probability, judge, recommend

**Acceptable verbs:** retrieve, extract, list, find, identify, locate, compile, quote, search, gather, research, compare

---

## STEP 5: Query Quality

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
    "retrieval_only": true,
    "query_quality": true
  },
  "issues": [],
  "summary": "A.8 required JSON repair (trailing comma). After repair, all checks pass. 6 GDR queries ready for execution."
}
```

### PASS (No Repair Needed) Example
```json
{
  "validation_result": "PASS",
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
    "retrieval_only": true,
    "query_quality": true
  },
  "issues": [],
  "summary": "A.8 is valid. 6 GDR queries ready for execution."
}
```

### FAIL (Unrepairable JSON) Example
```json
{
  "validation_result": "FAIL",
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
    "retrieval_only": false,
    "query_quality": true
  },
  "issues": [
    {
      "severity": "ERROR",
      "check": "count_validation",
      "message": "Research_Plan contains 5 items, expected 6"
    },
    {
      "severity": "ERROR",
      "check": "retrieval_only",
      "message": "RQ4 Prompt_Text contains forbidden verb 'analyze'",
      "rq_id": "RQ4"
    }
  ],
  "summary": "A.8 validation failed. 2 errors must be fixed before RQ_ASK execution."
}
```
