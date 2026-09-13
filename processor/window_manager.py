"""
Sliding Window Manager (Deque-based)
=====================================
Implements a fixed-size sliding window using collections.deque for each
sensor metric per device.

DSA Concept: Deque / Sliding Window
-------------------------------------
A deque (double-ended queue) is used because:
  • append()    is O(1) – adding new readings is constant time.
  • popleft()   is O(1) – removing the oldest reading is constant time
                          (happens automatically with maxlen).
  • Memory is bounded – maxlen ensures we never exceed the window size.

A list would require O(n) for pop(0); a deque gives O(1) for both ends.

Complexity Analysis:
  Operation                | Time      | Space
  -------------------------+-----------+-------
  Add reading              | O(1)      | O(w)  where w = window size
  Remove oldest            | O(1)      | –
  Calculate rolling avg    | O(w)      | O(1)
  Calculate rolling min    | O(w)      | O(1)
  Calculate rolling max    | O(w)      | O(1)
  Get window contents      | O(w)      | O(w)
  Space per device/metric  |           | O(w)
"""

from collections import deque
from typing import Optional


class SlidingWindow:
    """
    Fixed-size sliding window backed by collections.deque.

    Parameters
    ----------
    max_size : int
        Maximum number of elements in the window (default 30).
    """

    def __init__(self, max_size: int = 30):
        self._window: deque[float] = deque(maxlen=max_size)
        self._max_size = max_size

    def add(self, value: float) -> None:
        """Append a new value. O(1). Old values are auto-evicted."""
        self._window.append(value)

    @property
    def size(self) -> int:
        return len(self._window)

    @property
    def is_full(self) -> bool:
        return len(self._window) == self._max_size

    def rolling_average(self) -> Optional[float]:
        """Return the mean of the current window. O(w)."""
        if not self._window:
            return None
        return sum(self._window) / len(self._window)

    def rolling_min(self) -> Optional[float]:
        """Return the minimum of the current window. O(w)."""
        if not self._window:
            return None
        return min(self._window)

    def rolling_max(self) -> Optional[float]:
        """Return the maximum of the current window. O(w)."""
        if not self._window:
            return None
        return max(self._window)

    def get_values(self) -> list[float]:
        """Return a copy of the current window as a list. O(w)."""
        return list(self._window)

    def clear(self) -> None:
        """Clear the window."""
        self._window.clear()

    def __repr__(self) -> str:
        return f"SlidingWindow(size={self.size}/{self._max_size})"


class WindowManager:
    """
    Manages sliding windows for multiple devices × multiple metrics.

    DSA Concept: Hash Map / Dictionary
    -----------------------------------
    Uses a nested dict  {device_id: {metric: SlidingWindow}}  so that
    looking up or creating a window for any device/metric is O(1) average.

    Complexity:
      Lookup device window  : O(1) average (dict)
      Create new window     : O(1)
      Total space           : O(d × m × w) where d=devices, m=metrics, w=window size
    """

    METRICS = ["temperature", "humidity", "pressure", "vibration"]

    def __init__(self, window_size: int = 30):
        self._window_size = window_size
        # {device_id: {metric_name: SlidingWindow}}
        self._windows: dict[str, dict[str, SlidingWindow]] = {}

    def _ensure_device(self, device_id: str) -> None:
        """Lazily create windows for a device if not yet tracked."""
        if device_id not in self._windows:
            self._windows[device_id] = {
                m: SlidingWindow(self._window_size) for m in self.METRICS
            }

    def add_reading(self, device_id: str, reading: dict) -> dict:
        """
        Add a reading and return rolling averages.

        Parameters
        ----------
        device_id : str
        reading : dict
            Must contain keys for each metric.

        Returns
        -------
        dict with rolling_<metric> values.
        """
        self._ensure_device(device_id)
        result = {}
        for metric in self.METRICS:
            value = reading.get(metric)
            if value is not None:
                self._windows[device_id][metric].add(float(value))
            window = self._windows[device_id][metric]
            result[f"rolling_{metric}"] = window.rolling_average()
        return result

    def get_window(self, device_id: str, metric: str) -> Optional[SlidingWindow]:
        """Return the SlidingWindow for a device/metric, or None."""
        return self._windows.get(device_id, {}).get(metric)

    def get_device_stats(self, device_id: str) -> dict:
        """Return min/max/avg for every metric of a device."""
        if device_id not in self._windows:
            return {}
        stats = {}
        for metric, window in self._windows[device_id].items():
            stats[metric] = {
                "avg": window.rolling_average(),
                "min": window.rolling_min(),
                "max": window.rolling_max(),
                "count": window.size,
            }
        return stats
