# CI Guard & Auto Rollback — v1

## Purpose
Define deterministic CI/CD guardrails
based on the **Intelligent Health Contract v1**.

This document specifies **when** a deployment is blocked,
rolled back, or promoted.

---

## Health Dependency
CI behavior is driven exclusively by:

```
GET /health/intelligent
```

As defined in `docs/health-contract.md`.

---

## CI Guard Rules

The pipeline MUST be blocked when:

- `degraded == true`
- `decision_ready == false`

These checks are **authoritative** and fail closed.

HTTP status codes alone MUST NOT be used.

---

## Auto Rollback Logic

### Failure Path
Triggered when:
- Health check fails
- Guard rules are violated

Actions:
1. Roll back to `intelligent-deploy:stable`
2. Mark deployment as failed
3. Preserve container logs for analysis

---

### Success Path
Triggered when:
- `degraded == false`
- `decision_ready == true`

Actions:
1. Promote `intelligent-deploy:latest`
2. Tag it as `intelligent-deploy:stable`
3. Mark deployment as successful

---

## Safety Guarantees

- Rollback is **idempotent**
- Promotion occurs only after **positive health confirmation**
- No partial or ambiguous states are permitted

---

## Tooling Considerations

### Why No `jq`
- Ensures CI portability
- Avoids OS‑specific dependencies
- Keeps pipelines vendor-agnostic and deterministic

---

## CI/CD Principles
- Fail fast
- Fail closed
- Health-driven decisions
- Zero human intervention

