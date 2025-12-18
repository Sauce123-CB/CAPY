# A.9 Research Results Validator

## Purpose

Validate the A.9_RESEARCH_RESULTS artifact after RQ_ASK execution. This checks that Gemini Deep Research returned substantive results that can feed the ENRICH stage.

## Input

You receive a JSON object produced by the RQ_ASK kernel.

## Validation Checklist

### 1. Schema Conformance

Check that the following structure exists:

```json
{
  "ticker": "string",
  "execution_timestamp": "ISO-8601",
  "total_queries": 6,
  "successful_queries": integer,
  "failed_queries": integer,
  "results": [...],
  "execution_time_seconds": float
}
```

**Required fields per result item:**
- `rq_id` (string)
- `status` (string: "SUCCESS" | "ERROR" | "TIMEOUT")
- `query_text` (string)
- `response_text` (string)
- `execution_time_seconds` (float)
- `timestamp` (string)

### 2. Success Rate Check

| Threshold | Result |
|-----------|--------|
| 6/6 SUCCESS | PASS |
| 5/6 SUCCESS | PASS with WARNING |
| 4/6 SUCCESS | WARN (review failures) |
| <4/6 SUCCESS | FAIL (too many failures) |

### 3. Response Length Sanity

For each SUCCESS result, check `response_text` length:

| Length | Assessment |
|--------|------------|
| > 2000 chars | Good (substantive research) |
| 500-2000 chars | Acceptable (brief but usable) |
| < 500 chars | WARNING (suspiciously short) |
| 0 chars | ERROR (empty response) |

### 4. Content Quality Spot-Check

For each SUCCESS result, verify:
- [ ] Response is not an error message or refusal
- [ ] Response contains factual content (not just "I cannot..." or "As an AI...")
- [ ] Response is relevant to the query topic

**Red flag phrases to detect:**
- "I cannot access"
- "I don't have access to"
- "As an AI language model"
- "I'm unable to browse"
- "Error:"
- "Rate limit"

### 5. Coverage Completeness

Map results back to A.8 allocation:
- [ ] M-1 (Integrity Check) has substantive response
- [ ] M-2 (Adversarial Synthesis) has substantive response
- [ ] M-3 (Scenario H.A.D.) has substantive response
- [ ] At least 2/3 Dynamic queries succeeded

### 6. Execution Metrics

- [ ] No ERROR or TIMEOUT with empty error_message
- [ ] If total execution time > 900 seconds (15 min), note as INFO (Deep Research can be slow)

**Note:** Deep Research queries can legitimately take 5-10+ minutes each. Long execution times are not failures - only flag as INFO for awareness.

## Output Format

```json
{
  "validation_result": "PASS" | "WARN" | "FAIL",
  "timestamp": "ISO-8601",
  "metrics": {
    "total_queries": 6,
    "successful": integer,
    "failed": integer,
    "avg_response_length": integer,
    "total_execution_time": float
  },
  "checks": {
    "schema_conformance": true | false,
    "success_rate": true | false,
    "response_length": true | false,
    "content_quality": true | false,
    "coverage_completeness": true | false
  },
  "issues": [
    {
      "severity": "ERROR" | "WARNING" | "INFO",
      "check": "string",
      "message": "string",
      "rq_id": "string (optional)"
    }
  ],
  "per_query_summary": [
    {
      "rq_id": "RQ1",
      "status": "SUCCESS",
      "response_length": 3500,
      "assessment": "Good - substantive research on governance"
    }
  ],
  "summary": "string (2-3 sentence summary)",
  "recommendation": "PROCEED" | "REVIEW" | "RETRY"
}
```

## Decision Logic

### PASS
- 5-6/6 queries succeeded
- All SUCCESS responses > 500 chars
- No red flag phrases detected
- Mandatory coverage complete

**Recommendation:** PROCEED to ENRICH

### WARN
- 4/6 queries succeeded, OR
- 1-2 responses suspiciously short, OR
- Minor content quality concerns

**Recommendation:** REVIEW results before proceeding

### FAIL
- <4/6 queries succeeded, OR
- Mandatory coverage incomplete (M-1, M-2, or M-3 failed), OR
- Multiple empty or error responses

**Recommendation:** RETRY with different query formulation

## Examples

### PASS Example
```json
{
  "validation_result": "PASS",
  "metrics": {
    "total_queries": 6,
    "successful": 6,
    "failed": 0,
    "avg_response_length": 4200,
    "total_execution_time": 187.3
  },
  "checks": {
    "schema_conformance": true,
    "success_rate": true,
    "response_length": true,
    "content_quality": true,
    "coverage_completeness": true
  },
  "issues": [],
  "summary": "All 6 queries completed successfully with substantive responses. Average response length 4200 chars. Ready for ENRICH stage.",
  "recommendation": "PROCEED"
}
```

### WARN Example
```json
{
  "validation_result": "WARN",
  "metrics": {
    "total_queries": 6,
    "successful": 5,
    "failed": 1,
    "avg_response_length": 3100,
    "total_execution_time": 245.8
  },
  "issues": [
    {
      "severity": "WARNING",
      "check": "success_rate",
      "message": "RQ4 failed with TIMEOUT after 300s",
      "rq_id": "RQ4"
    },
    {
      "severity": "INFO",
      "check": "coverage_completeness",
      "message": "RQ4 was Dynamic allocation (D-1), not Mandatory"
    }
  ],
  "summary": "5/6 queries succeeded. RQ4 (Dynamic) timed out but Mandatory coverage is complete. Results usable with reduced dynamic coverage.",
  "recommendation": "REVIEW"
}
```

### FAIL Example
```json
{
  "validation_result": "FAIL",
  "metrics": {
    "total_queries": 6,
    "successful": 3,
    "failed": 3
  },
  "issues": [
    {
      "severity": "ERROR",
      "check": "success_rate",
      "message": "Only 3/6 queries succeeded (below 4/6 threshold)"
    },
    {
      "severity": "ERROR",
      "check": "coverage_completeness",
      "message": "M-3 (Scenario H.A.D.) failed - critical for SCENARIO stage"
    }
  ],
  "summary": "Execution failed with 3/6 success rate. Mandatory coverage incomplete. Cannot proceed to ENRICH.",
  "recommendation": "RETRY"
}
```
