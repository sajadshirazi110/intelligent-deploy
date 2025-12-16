# Intelligent Deploy — Self-Healing CI/CD (Level 2)

## Overview
This project demonstrates an export-ready, self-healing CI/CD system
with intelligent health evaluation, CI guard, and automatic rollback.

## Architecture
- FastAPI application
- Intelligent Health Contract
- Docker-based deployment
- GitHub Actions CI pipeline

## Health Model
- Real-time latency tracking (P95)
- Error-rate evaluation
- Idle traffic awareness
- Decision-ready health responses

## CI/CD Flow
1. Build image
2. Run container (canary)
3. Evaluate /health/intelligent
4. Block pipeline if degraded
5. Auto-rollback to stable on failure
6. Promote latest to stable on success

## Release
- Current stable release: v2.0.0-self-healing
