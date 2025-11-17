import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, client_ip: str):
        now = time.time()
        window_start = now - self.window_seconds
        request_times = self.requests[client_ip]

        # Remove outdated timestamps
        self.requests[client_ip] = [t for t in request_times if t > window_start]

        if len(self.requests[client_ip]) < self.max_requests:
            self.requests[client_ip].append(now)
            return True
        return False

rate_limiter = RateLimiter()
