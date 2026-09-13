"""
Isolation Forest – Offline Training Script
============================================
Trains an Isolation Forest model on the generated sensor dataset and saves
the fitted model + scaler to disk for real-time scoring.

Why Isolation Forest?
  • Designed for anomaly / outlier detection.
  • Works well with high-dimensional, unsupervised data.
  • Efficient: O(n·t·log(ψ)) training where t = number of trees, ψ = subsample size.
  • Low-latency scoring: O(t·log(ψ)) per sample – ideal for streaming.

Contamination parameter:
  The expected proportion of anomalies in the dataset.  We set it to 0.05
  (5 %) to match our data generator's anomaly fraction.

Training process:
  1.  Load historical CSV data.
  2.  Select numeric features: temperature, humidity, pressure, vibration.
  3.  Standard-scale the features (important for stable scoring).
  4.  Fit IsolationForest.
  5.  Save both the scaler and the model as a single joblib artifact.

Live scoring process:
  1.  Load scaler + model once at processor start-up.
  2.  For each incoming event, scale features → model.decision_function().
  3.  decision_function returns a score; lower (more negative) = more anomalous.
  4.  model.predict returns -1 for anomaly, 1 for normal.
"""

import os
import sys
import argparse
import logging

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

FEATURES = ["temperature", "humidity", "pressure", "vibration"]


def train(data_path: str, model_path: str, contamination: float = 0.05, seed: int = 42):
    """Train IsolationForest and persist model + scaler."""
    logger.info("Loading data from %s", data_path)
    df = pd.read_csv(data_path)

    # Validate columns
    for col in FEATURES:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    X = df[FEATURES].dropna().values
    logger.info("Training on %d samples, %d features", X.shape[0], X.shape[1])

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train
    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        max_samples="auto",
        random_state=seed,
        n_jobs=-1,
    )
    model.fit(X_scaled)

    # Quick evaluation on training data
    preds = model.predict(X_scaled)
    n_anomalies = (preds == -1).sum()
    logger.info(
        "Training complete – detected %d anomalies out of %d (%.2f%%)",
        n_anomalies,
        len(preds),
        100 * n_anomalies / len(preds),
    )

    # Save
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    artifact = {"model": model, "scaler": scaler, "features": FEATURES}
    joblib.dump(artifact, model_path)
    logger.info("Model saved to %s", model_path)


def main():
    parser = argparse.ArgumentParser(description="Train Isolation Forest anomaly model")
    parser.add_argument(
        "--data",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "..", "data", "sensor_data.csv"),
        help="Path to training CSV",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "..", "models", "anomaly_model.pkl"),
        help="Output model path",
    )
    parser.add_argument("--contamination", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    train(args.data, args.model, args.contamination, args.seed)


if __name__ == "__main__":
    main()
