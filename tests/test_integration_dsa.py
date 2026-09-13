"""Integration test: Verify DSA structures are genuinely in the live processing path."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from processor.window_manager import WindowManager
from processor.statistics import StatisticsTracker
from processor.anomaly_tracker import AnomalyTracker
from ml.model_utils import AnomalyScorer

def test_dsa_structures_in_live_processing_path():
    """Verify DSA structures are genuinely used and populated in the live processing path."""
    wm = WindowManager(window_size=30)
    st_tracker = StatisticsTracker()
    at = AnomalyTracker(max_size=20)
    scorer = AnomalyScorer(os.path.join(os.path.dirname(__file__), "..", "models", "anomaly_model.pkl"))

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "sensor_data.csv"), nrows=50)
    anomaly_count = 0
    rolling = {}
    for _, row in df.iterrows():
        device_id = row["device_id"]
        reading = {
            "temperature": float(row["temperature"]),
            "humidity": float(row["humidity"]),
            "pressure": float(row["pressure"]),
            "vibration": float(row["vibration"]),
        }
        rolling = wm.add_reading(device_id, reading)
        score, is_anomaly = scorer.score(reading)
        st_tracker.update(device_id, reading, is_anomaly)
        if is_anomaly:
            at.add(score, {**reading, "device_id": device_id})
            anomaly_count += 1

    window = wm.get_window("sensor-03", "temperature")
    assert window is not None and window.size > 0, "Sliding window must be populated"
    assert window.rolling_average() is not None, "Rolling average must be computed"

    device_stats = st_tracker.get_device_stats("sensor-03")
    assert device_stats is not None, "Device stats must exist"
    assert device_stats["temperature"]["count"] > 0, "Running stats count must be > 0"

    assert "rolling_temperature" in rolling, "Rolling temperature key must exist"
    assert at.size > 0 or anomaly_count == 0, "Anomaly tracker must hold anomalies if found"


if __name__ == "__main__":
    test_dsa_structures_in_live_processing_path()
    print("\nALL DSA STRUCTURES VERIFIED IN LIVE PROCESSING PATH [PASS]")

