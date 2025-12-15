import time
import threading
from collections import deque

class MetricsStore:
    def __init__(self):
        self._lock = threading.Lock()
        self.start_time = time.time()

        self.latencies_ms = deque(maxlen=500)
        self.error_timestamps = deque(maxlen=500)

        self.last_request_ts = None

    def record_request(self, latency_ms: float, is_error: bool):
        with self._lock:
            self.latencies_ms.append(latency_ms)
            self.last_request_ts = time.time()

            if is_error:
                self.error_timestamps.append(self.last_request_ts)

    def uptime_sec(self) -> float:
        return time.time() - self.start_time

    def latency_p95(self) -> float | None:
        with self._lock:
            if not self.latencies_ms:
                return None
            data = sorted(self.latencies_ms)
            idx = int(0.95 * len(data)) - 1
            return round(data[max(idx, 0)], 2)

    def error_rate_last_min(self) -> float:
        with self._lock:
            if not self.error_timestamps:
                return 0.0
            now = time.time()
            errors = [e for e in self.error_timestamps if now - e <= 60]
            return round(len(errors) / max(1, len(self.latencies_ms)), 4)

    def seconds_since_last_request(self) -> float | None:
        if not self.last_request_ts:
            return None
        return time.time() - self.last_request_ts


metrics = MetricsStore()
