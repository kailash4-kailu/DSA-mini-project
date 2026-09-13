"""Tests for RunningStats and StatisticsTracker."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from processor.statistics import RunningStats, StatisticsTracker


class TestRunningStats:
    def test_empty(self):
        rs = RunningStats()
        assert rs.count == 0
        assert rs.average is None
        assert rs.minimum is None
        assert rs.maximum is None

    def test_single_update(self):
        rs = RunningStats()
        rs.update(10.0)
        assert rs.count == 1
        assert rs.average == 10.0
        assert rs.minimum == 10.0
        assert rs.maximum == 10.0

    def test_multiple_updates(self):
        rs = RunningStats()
        for v in [10, 20, 30, 40, 50]:
            rs.update(v)
        assert rs.count == 5
        assert rs.total == 150.0
        assert rs.average == 30.0
        assert rs.minimum == 10.0
        assert rs.maximum == 50.0

    def test_negative_values(self):
        rs = RunningStats()
        rs.update(-5)
        rs.update(5)
        assert rs.minimum == -5
        assert rs.maximum == 5
        assert rs.average == 0.0

    def test_to_dict(self):
        rs = RunningStats()
        rs.update(10)
        rs.update(20)
        d = rs.to_dict()
        assert d["count"] == 2
        assert d["average"] == 15.0


class TestStatisticsTracker:
    def test_update_creates_device(self):
        st = StatisticsTracker()
        st.update("dev-01", {"temperature": 25, "humidity": 60, "pressure": 1013, "vibration": 0.5})
        stats = st.get_device_stats("dev-01")
        assert stats["temperature"]["count"] == 1
        assert stats["temperature"]["average"] == 25.0

    def test_anomaly_count(self):
        st = StatisticsTracker()
        reading = {"temperature": 25, "humidity": 60, "pressure": 1013, "vibration": 0.5}
        st.update("dev-01", reading, is_anomaly=False)
        st.update("dev-01", reading, is_anomaly=True)
        st.update("dev-01", reading, is_anomaly=True)
        stats = st.get_device_stats("dev-01")
        assert stats["anomaly_count"] == 2
        assert stats["total_readings"] == 3

    def test_metrics_for_db(self):
        st = StatisticsTracker()
        reading = {"temperature": 25, "humidity": 60, "pressure": 1013, "vibration": 0.5}
        st.update("dev-01", reading, is_anomaly=False)
        m = st.get_metrics_for_db("dev-01", reading, -0.1)
        assert m["device_id"] == "dev-01"
        assert m["total_readings"] == 1
        assert m["latest_temperature"] == 25
        assert m["latest_anomaly_score"] == -0.1
