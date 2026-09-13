"""
IoT Sensor Data Generator
==========================
Generates realistic sensor data with controlled anomalies for the DSA project.

Normal ranges:
  temperature : 20 – 35 °C
  humidity    : 40 – 80 %
  pressure    : 1000 – 1025 hPa
  vibration   : 0.1 – 1.5 mm/s

Anomaly injection (~5 % of records):
  temperature spike, humidity drop, pressure drop, vibration spike,
  or random combinations.
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEVICE_IDS = ["sensor-01", "sensor-02", "sensor-03", "sensor-04", "sensor-05"]

# Normal operating ranges
NORMAL = {
    "temperature": (20.0, 35.0),
    "humidity":    (40.0, 80.0),
    "pressure":    (1000.0, 1025.0),
    "vibration":   (0.1, 1.5),
}

# Anomaly range extensions
ANOMALY = {
    "temperature_spike": (50.0, 80.0),
    "humidity_drop":     (5.0, 20.0),
    "pressure_drop":     (950.0, 980.0),
    "vibration_spike":   (5.0, 15.0),
}


def generate_normal_reading(rng: np.random.Generator) -> dict:
    """Generate a single normal sensor reading."""
    return {
        "temperature": round(rng.uniform(*NORMAL["temperature"]), 2),
        "humidity":    round(rng.uniform(*NORMAL["humidity"]), 2),
        "pressure":    round(rng.uniform(*NORMAL["pressure"]), 2),
        "vibration":   round(rng.uniform(*NORMAL["vibration"]), 3),
    }


def inject_anomaly(reading: dict, rng: np.random.Generator) -> dict:
    """Modify a reading to contain one or more anomalies."""
    anomaly_type = rng.choice(
        ["temperature_spike", "humidity_drop", "pressure_drop", "vibration_spike", "combo"]
    )
    if anomaly_type == "temperature_spike" or anomaly_type == "combo":
        reading["temperature"] = round(rng.uniform(*ANOMALY["temperature_spike"]), 2)
    if anomaly_type == "humidity_drop" or anomaly_type == "combo":
        reading["humidity"] = round(rng.uniform(*ANOMALY["humidity_drop"]), 2)
    if anomaly_type == "pressure_drop" or anomaly_type == "combo":
        reading["pressure"] = round(rng.uniform(*ANOMALY["pressure_drop"]), 2)
    if anomaly_type == "vibration_spike" or anomaly_type == "combo":
        reading["vibration"] = round(rng.uniform(*ANOMALY["vibration_spike"]), 3)
    return reading


def generate_dataset(
    n_records: int = 5000,
    anomaly_fraction: float = 0.05,
    seed: int = 42,
    start_time: datetime | None = None,
) -> pd.DataFrame:
    """
    Generate a complete IoT sensor dataset.

    Parameters
    ----------
    n_records : int
        Total number of records to generate.
    anomaly_fraction : float
        Fraction of records that are anomalies (0-1).
    seed : int
        Random seed for reproducibility.
    start_time : datetime, optional
        Timestamp of the first reading. Defaults to now minus n_records seconds.

    Returns
    -------
    pd.DataFrame
    """
    rng = np.random.default_rng(seed)
    if start_time is None:
        start_time = datetime.now() - timedelta(seconds=n_records)

    records = []
    for i in range(n_records):
        reading = generate_normal_reading(rng)
        is_anomaly = rng.random() < anomaly_fraction
        if is_anomaly:
            reading = inject_anomaly(reading, rng)

        reading["timestamp"] = (start_time + timedelta(seconds=i)).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]  # millisecond precision
        reading["device_id"] = rng.choice(DEVICE_IDS)
        records.append(reading)

    df = pd.DataFrame(records)
    # Reorder columns
    df = df[["timestamp", "device_id", "temperature", "humidity", "pressure", "vibration"]]
    return df


def main():
    parser = argparse.ArgumentParser(description="Generate IoT sensor dataset")
    parser.add_argument("--records", type=int, default=5000, help="Number of records")
    parser.add_argument("--anomaly-fraction", type=float, default=0.05, help="Anomaly fraction (0-1)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, default=None, help="Output CSV path")
    args = parser.parse_args()

    # Determine output path
    if args.output:
        out_path = args.output
    else:
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        out_path = os.path.join(data_dir, "sensor_data.csv")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print(f"Generating {args.records} records (anomaly fraction={args.anomaly_fraction}) …")
    df = generate_dataset(
        n_records=args.records,
        anomaly_fraction=args.anomaly_fraction,
        seed=args.seed,
    )
    df.to_csv(out_path, index=False)
    anomaly_estimate = int(args.records * args.anomaly_fraction)
    print(f"Saved to {out_path}  ({len(df)} rows, ~{anomaly_estimate} anomalies)")


if __name__ == "__main__":
    main()
