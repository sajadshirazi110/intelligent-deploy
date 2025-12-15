import time
from fastapi import FastAPI, Request
from app.metrics import metrics
from app.health import intelligent_health

# -----------------------------------------------------------------------------
# App Init
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Intelligent Deploy",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Metrics Middleware
# -----------------------------------------------------------------------------
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)

    latency_ms = (time.time() - start) * 1000
    is_error = response.status_code >= 500

    metrics.record_request(latency_ms, is_error)
    return response

# -----------------------------------------------------------------------------
# Health Endpoints
# -----------------------------------------------------------------------------
@app.get("/health", tags=["health"])
def health():
    """
    Liveness check (Alive / Dead)
    Used by Docker, K8s liveness probes.
    """
    return {
        "status": "ok",
        "uptime_sec": round(metrics.uptime_sec(), 2),
        "version": "0.1.0",
    }


@app.get("/health/intelligent", tags=["health"])
def health_intelligent():
    """
    Decision‑ready health endpoint.
    Used by CI/CD, Progressive Delivery, Auto‑Rollback.
    """
    return intelligent_health()

