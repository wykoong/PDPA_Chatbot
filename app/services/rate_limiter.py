import time
from typing import List

class RateLimiter:
    """Simple rate limiter implementation."""

    def __init__(self, max_requests: int, time_window: int) -> None:
        """
        Initialize the rate limiter.

        Args:
            max_requests (int): Maximum allowed requests.
            time_window (int): Time window in seconds.
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: List[float] = []

    def is_allowed(self) -> bool:
        """
        Check if the current request is allowed.

        Returns:
            bool: True if allowed, False otherwise.
        """
        now = time.time()
        self.requests = [req for req in self.requests if now - req < self.time_window]
        if len(self.requests) >= self.max_requests:
            return False
        self.requests.append(now)
        return True
