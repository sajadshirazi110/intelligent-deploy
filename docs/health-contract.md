# Intelligent Health Contract

## Purpose
Provide a deterministic health decision for machines (CI/CD),
not humans.

## Endpoint
GET /health/intelligent

## Response Fields
- status
- degraded
- decision_ready
- reasons

## Decision Rules
- P95 latency > threshold → degraded
- Error rate > threshold → degraded
- No recent traffic → idle=true, degraded=false

## Design Principles
- Fail fast
- Machine-readable
- Backward compatible
