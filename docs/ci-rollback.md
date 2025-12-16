# CI Guard & Auto Rollback

## CI Guard
Pipeline is blocked if health endpoint reports:
- degraded = true
- decision_ready = false

## Auto Rollback Logic
- On failed health check → rollback to stable image
- On success → promote latest to stable

## Why No jq?
To keep the pipeline fully portable and vendor-agnostic.
