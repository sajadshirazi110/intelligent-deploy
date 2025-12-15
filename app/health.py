from app.metrics import metrics

LATENCY_P95_THRESHOLD_MS = 500
ERROR_RATE_THRESHOLD = 0.02
NO_TRAFFIC_THRESHOLD_SEC = 10
WARMUP_UPTIME_SEC = 30


def intelligent_health():
    reasons = []
    degraded = False

    uptime = metrics.uptime_sec()
    latency_p95 = metrics.latency_p95()
    error_rate = metrics.error_rate_last_min()
    idle_sec = metrics.seconds_since_last_request()

    if uptime < WARMUP_UPTIME_SEC:
        reasons.append("warming_up")

    if latency_p95 is not None and latency_p95 > LATENCY_P95_THRESHOLD_MS:
        degraded = True
        reasons.append(f"high_latency_p95:{latency_p95}ms")

    if error_rate > ERROR_RATE_THRESHOLD:
        degraded = True
        reasons.append(f"high_error_rate:{error_rate}")

    idle = False

    if idle_sec is not None and idle_sec > NO_TRAFFIC_THRESHOLD_SEC:
         idle = True
         reasons.append("idle_no_recent_traffic")


    return {
        "status": "degraded" if degraded else "ok",
        "degraded": degraded,
        "uptime_sec": round(uptime, 2),
        "latency_p95_ms": latency_p95,
        "error_rate_1m": error_rate,
        "decision_ready": uptime >= WARMUP_UPTIME_SEC,
        "reasons": reasons,
    }
