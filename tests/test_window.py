"""Tests for SlidingWindow and WindowManager."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from processor.window_manager import SlidingWindow, WindowManager


class TestSlidingWindow:
    def test_empty_window(self):
        w = SlidingWindow(5)
        assert w.size == 0
        assert w.rolling_average() is None
        assert w.rolling_min() is None
        assert w.rolling_max() is None

    def test_add_single(self):
        w = SlidingWindow(5)
        w.add(10.0)
        assert w.size == 1
        assert w.rolling_average() == 10.0
        assert w.rolling_min() == 10.0
        assert w.rolling_max() == 10.0

    def test_rolling_average(self):
        w = SlidingWindow(5)
        for v in [10, 20, 30, 40, 50]:
            w.add(v)
        assert w.rolling_average() == 30.0

    def test_window_eviction(self):
        """When window is full, oldest element is evicted (O(1) via deque maxlen)."""
        w = SlidingWindow(3)
        w.add(1)
        w.add(2)
        w.add(3)
        assert w.size == 3
        w.add(4)  # evicts 1
        assert w.size == 3
        assert w.get_values() == [2, 3, 4]
        assert w.rolling_average() == 3.0
        assert w.rolling_min() == 2
        assert w.rolling_max() == 4

    def test_is_full(self):
        w = SlidingWindow(2)
        assert not w.is_full
        w.add(1)
        assert not w.is_full
        w.add(2)
        assert w.is_full

    def test_clear(self):
        w = SlidingWindow(5)
        w.add(1)
        w.add(2)
        w.clear()
        assert w.size == 0


class TestWindowManager:
    def test_add_reading(self):
        wm = WindowManager(window_size=5)
        reading = {"temperature": 25.0, "humidity": 60.0, "pressure": 1013.0, "vibration": 0.5}
        result = wm.add_reading("sensor-01", reading)
        assert "rolling_temperature" in result
        assert result["rolling_temperature"] == 25.0

    def test_multiple_readings(self):
        wm = WindowManager(window_size=3)
        for temp in [20, 25, 30]:
            wm.add_reading("sensor-01", {"temperature": temp, "humidity": 60, "pressure": 1013, "vibration": 0.5})
        result = wm.add_reading("sensor-01", {"temperature": 35, "humidity": 60, "pressure": 1013, "vibration": 0.5})
        # Window: [25, 30, 35]  (20 evicted)
        assert abs(result["rolling_temperature"] - 30.0) < 0.001

    def test_multiple_devices(self):
        wm = WindowManager(window_size=5)
        wm.add_reading("sensor-01", {"temperature": 20, "humidity": 50, "pressure": 1010, "vibration": 0.3})
        wm.add_reading("sensor-02", {"temperature": 30, "humidity": 70, "pressure": 1020, "vibration": 1.0})
        s1 = wm.get_device_stats("sensor-01")
        s2 = wm.get_device_stats("sensor-02")
        assert s1["temperature"]["avg"] == 20.0
        assert s2["temperature"]["avg"] == 30.0
