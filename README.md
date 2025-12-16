# Intelligent Deploy — Self-Healing CI/CD (Level 2)

## Overview
This repository demonstrates an export-ready **Self-Healing CI/CD system**
built around an intelligent health contract, CI guard, and automatic rollback.

The goal is to provide a **machine-decision health model** suitable for
production-grade deployment pipelines.

## Architecture
- FastAPI application
- Intelligent health evaluation (latency, error rate, idleness)
- Docker-based build and execution
- GitHub Actions CI pipeline with guard and rollback

## Intelligent Health Model
The system exposes a decision-ready health endpoint used by CI/CD,
not by humans.

Key signals:
- P95 latency tracking
- Error-rate evaluation
- Idle traffic awareness (non-degraded)
- Deterministic degradation decisions

## CI / CD Flow
1. Build Docker image
2. Run container as canary
3. Call `/health/intelligent`
4. Block pipeline if health is degraded
5. Auto-rollback to `stable` on failure
6. Promote `latest` to `stable` on success

## Self-Healing Behavior
- Failed health → automatic rollback
- Successful health → stable promotion
- No vendor-specific dependencies (jq-free, portable CI)

## Release
- Stable export-ready release: **v2.0.0-self-healing**
- Maturity level: **Level 2 – Self-Healing System**
