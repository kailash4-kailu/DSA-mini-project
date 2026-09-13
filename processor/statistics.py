"""
Running Statistics Tracker
============================
Maintains streaming count, sum, average, minimum, and maximum for each
sensor metric per device WITHOUT reprocessing the entire history.

DSA Concept: Running / Online Statistics
------------------------------------------
As each new event arrives, we update accumulators in O(1) time:
  count += 1
  sum   += value
  avg    = sum / count
  min    = min(current_min, value)
  max    = max(current_max, value)

This avoids O(n) re-scans of historical data, which is crucial for
streaming systems where n grows unboundedly.

Complexity Analysis:
  Operation            | Time  | Space
  ---------------------+-------+------
  Update statistics    | O(1)  | O(1) per metric
  Read any statistic   | O(1)  | –
  Space per device     | O(m)  | where m = number of metrics
  Total space          | O(d·m)| d = devices, m = metrics
"""

from typing import Optional


class RunningStats:
    """
    O(1)-update running statistics for a single metric stream.
    """

    def __init__(self):
        self.count: int = 0
        self.total: float = 0.0
        self._min: Optional[float] = None
        self._max: Optional[float] = None

    def update(self, value: float) -> None:
        """Update all accumulators with a new value. O(1)."""
        self.count += 1
        self.total += value
        if self._min is None or value < self._min:
            self._min = value
        if self._max is None or value > self._max:
            self._max = value

    @property
    def average(self) -> Optional[float]:
        if self.count == 0:
            return None
        return self.total / self.count

    @property
    def minimum(self) -> Optional[float]:
        return self._min

    @property
    def maximum(self) -> Optional[float]:
        return self._max

    def to_dict(self) -> dict:
        return {
            "count": self.count,
            "sum": round(self.total, 4),
            "average": round(self.average, 4) if self.average is not None else None,
            "min": self._min,
            "max": self._max,
        }


class StatisticsTracker:
    """
    Manages RunningStats for multiple devices × metrics.

    DSA Concept: Hash Map / Dictionary
    -----------------------------------
    Nested dict {device_id: {metric: RunningStats}} provides O(1) lookup.
    """

    METRICS = ["temperature", "humidity", "pressure", "vibration"]

    def __init__(self):
        # {device_id: {metric: RunningStats}}
        self._stats: dict[str, dict[str, RunningStats]] = {}
        # Global anomaly counter per device
        self._anomaly_counts: dict[str, int] = {}

    def _ensure_device(self, device_id: str) -> None:
        if device_id not in self._stats:
            self._stats[device_id] = {m: RunningStats() for m in self.METRICS}
            self._anomaly_counts[device_id] = 0

    def update(self, device_id: str, reading: dict, is_anomaly: bool = False) -> None:
        """Update statistics for all metrics of a device. O(m) = O(1) since m is constant."""
        self._ensure_device(device_id)
        for metric in self.METRICS:
            value = reading.get(metric)
            if value is not None:
                self._stats[device_id][metric].update(float(value))
        if is_anomaly:
            self._anomaly_counts[device_id] += 1

    def get_device_stats(self, device_id: str) -> dict:
        """Return all statistics for a device."""
        self._ensure_device(device_id)
        result = {}
        for metric in self.METRICS:
            result[metric] = self._stats[device_id][metric].to_dict()
        result["anomaly_count"] = self._anomaly_counts.get(device_id, 0)
        total = self._stats[device_id][self.METRICS[0]].count
        result["total_readings"] = total
        return result

    def get_metrics_for_db(self, device_id: str, reading: dict, anomaly_score: float) -> dict:
        """Build a dict suitable for database.upsert_metrics()."""
        self._ensure_device(device_id)
        s = self._stats[device_id]
        return {
            "device_id": device_id,
            "total_readings": s["temperature"].count,
            "anomaly_count": self._anomaly_counts.get(device_id, 0),
            "latest_temperature": reading.get("temperature"),
            "latest_humidity": reading.get("humidity"),
            "latest_pressure": reading.get("pressure"),
            "latest_vibration": reading.get("vibration"),
            "avg_temperature": s["temperature"].average,
            "avg_humidity": s["humidity"].average,
            "avg_pressure": s["pressure"].average,
            "avg_vibration": s["vibration"].average,
            "min_temperature": s["temperature"].minimum,
            "max_temperature": s["temperature"].maximum,
            "min_humidity": s["humidity"].minimum,
            "max_humidity": s["humidity"].maximum,
            "min_pressure": s["pressure"].minimum,
            "max_pressure": s["pressure"].maximum,
            "min_vibration": s["vibration"].minimum,
            "max_vibration": s["vibration"].maximum,
            "latest_anomaly_score": anomaly_score,
        }
