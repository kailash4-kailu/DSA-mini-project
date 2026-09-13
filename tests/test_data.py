"""Tests for the IoT dataset generator."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
from data.generate_data import generate_dataset, generate_normal_reading, inject_anomaly
import numpy as np


class TestDataGenerator:
    def test_generate_dataset_shape(self):
        df = generate_dataset(n_records=100, anomaly_fraction=0.1, seed=1)
        assert len(df) == 100
        assert list(df.columns) == ["timestamp", "device_id", "temperature", "humidity", "pressure", "vibration"]

    def test_all_numeric_columns(self):
        df = generate_dataset(n_records=50, seed=2)
        for col in ["temperature", "humidity", "pressure", "vibration"]:
            assert pd.api.types.is_float_dtype(df[col])

    def test_device_ids_exist(self):
        df = generate_dataset(n_records=200, seed=3)
        assert df["device_id"].nunique() > 1

    def test_normal_reading_ranges(self):
        rng = np.random.default_rng(42)
        for _ in range(100):
            r = generate_normal_reading(rng)
            assert 20 <= r["temperature"] <= 35
            assert 40 <= r["humidity"] <= 80
            assert 1000 <= r["pressure"] <= 1025
            assert 0.1 <= r["vibration"] <= 1.5

    def test_anomaly_injection_changes_values(self):
        rng = np.random.default_rng(42)
        # Run enough times to see at least one change
        changed = False
        for _ in range(50):
            r = generate_normal_reading(rng)
            original_temp = r["temperature"]
            r = inject_anomaly(r, rng)
            if r["temperature"] != original_temp:
                changed = True
                break
        assert changed, "Anomaly injection should change at least some values"

    def test_reproducibility(self):
        from datetime import datetime
        fixed_time = datetime(2024, 1, 1, 0, 0, 0)
        df1 = generate_dataset(n_records=50, seed=999, start_time=fixed_time)
        df2 = generate_dataset(n_records=50, seed=999, start_time=fixed_time)
        pd.testing.assert_frame_equal(df1, df2)

    def test_timestamp_format(self):
        df = generate_dataset(n_records=5, seed=1)
        for ts in df["timestamp"]:
            # Should parse without error
            pd.Timestamp(ts)
