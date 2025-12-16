# Intelligent Health Contract — v1

## Purpose
Provide a **deterministic, machine-enforceable health decision**
consumed by CI/CD and deployment automation.

This contract is **not designed for human observability**.

---

## Endpoint
```
GET /health/intelligent
```

---

## Contract Versioning
- This document defines **Contract v1**
- Backward-compatible changes are allowed
- Breaking changes require a new endpoint:
  `/health/v2/intelligent`

---

## Response Schema

```json
{
  "status": "ok | degraded | unhealthy",
  "degraded": false,
  "decision_ready": true,
  "reasons": [
    "idle_no_recent_traffic"
  ]
}
```

---

## Field Semantics

### status
High-level qualitative state.

- `ok` → system appears healthy
- `degraded` → service quality is reduced
- `unhealthy` → immediate failure condition

⚠️ **Status is informational. It MUST NOT be used alone.**

---

### degraded
**Primary decision signal for CI/CD.**

Rules:
- `true` → block promotion or trigger rollback
- `false` → deployment allowed

`degraded` takes precedence over `status`.

---

### decision_ready
Indicates whether **sufficient runtime data exists**
to make a safe deployment decision.

Rules:
- `false` → CI MUST fail closed
- `true` → decision is enforceable

---

### reasons
Human-readable explanations intended for:
- CI logs
- Incident review
- Post-mortem analysis

---

## Decision Rules

The following rules are applied deterministically:

- P95 latency > threshold → `degraded = true`
- Error rate > threshold → `degraded = true`
- No recent traffic detected:
  - `idle = true`
  - `degraded = false`

Idle is treated as **neutral**, not failure.

---

## CI/CD Expectations

CI systems MUST:
- Trust `degraded` over `status`
- Fail closed when `decision_ready == false`
- Never infer health from HTTP status code alone

---

## Design Principles
- Fail fast, fail closed
- Machine-first semantics
- Deterministic decisions
- Backward-compatible evolution
