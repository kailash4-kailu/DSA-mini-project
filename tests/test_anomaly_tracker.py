"""Tests for AnomalyTracker (heap-based top-N)."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from processor.anomaly_tracker import AnomalyTracker


class TestAnomalyTracker:
    def test_empty_tracker(self):
        at = AnomalyTracker(max_size=5)
        assert at.size == 0
        assert at.get_top_anomalies() == []
        assert at.peek_threshold() is None

    def test_add_below_capacity(self):
        at = AnomalyTracker(max_size=5)
        at.add(-0.5, {"device_id": "d1", "temperature": 60})
        assert at.size == 1

    def test_maintains_top_n(self):
        at = AnomalyTracker(max_size=3)
        # Lower score = more anomalous
        at.add(-0.1, {"id": "a"})   # least anomalous
        at.add(-0.5, {"id": "b"})
        at.add(-0.8, {"id": "c"})
        at.add(-0.2, {"id": "d"})   # should NOT replace anything more anomalous
        at.add(-0.9, {"id": "e"})   # most anomalous, should replace -0.1

        assert at.size == 3
        top = at.get_top_anomalies()
        scores = [t["anomaly_score"] for t in top]
        # Should contain -0.9, -0.8, -0.5 (most anomalous)
        assert -0.9 in scores
        assert -0.8 in scores
        assert -0.5 in scores

    def test_sorted_output(self):
        at = AnomalyTracker(max_size=5)
        at.add(-0.3, {"id": "a"})
        at.add(-0.7, {"id": "b"})
        at.add(-0.1, {"id": "c"})
        top = at.get_top_anomalies()
        scores = [t["anomaly_score"] for t in top]
        # Most anomalous (lowest score) first
        assert scores == sorted(scores)

    def test_clear(self):
        at = AnomalyTracker(max_size=5)
        at.add(-0.5, {"id": "a"})
        at.clear()
        assert at.size == 0

    def test_peek_threshold(self):
        at = AnomalyTracker(max_size=2)
        at.add(-0.5, {"id": "a"})
        at.add(-0.8, {"id": "b"})
        # Threshold = score of least anomalous in top-N
        threshold = at.peek_threshold()
        assert threshold == -0.5
