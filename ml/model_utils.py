"""
Model utilities for loading and scoring with the trained Isolation Forest.
"""

import os
import logging
import numpy as np
import joblib

logger = logging.getLogger(__name__)

FEATURES = ["temperature", "humidity", "pressure", "vibration"]


class AnomalyScorer:
    """
    Wraps the trained Isolation Forest model for real-time scoring.

    Usage
    -----
    scorer = AnomalyScorer("models/anomaly_model.pkl")
    score, is_anomaly = scorer.score({"temperature": 60, "humidity": 30,
                                       "pressure": 970, "vibration": 8.0})
    """

    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        artifact = joblib.load(model_path)
        self.model = artifact["model"]
        self.scaler = artifact["scaler"]
        self.features = artifact.get("features", FEATURES)
        logger.info("Loaded anomaly model from %s", model_path)

    def score(self, reading: dict) -> tuple[float, bool]:
        """
        Score a single sensor reading.

        Parameters
        ----------
        reading : dict
            Must contain keys for each feature (temperature, humidity, etc.).

        Returns
        -------
        (anomaly_score, is_anomaly)
            anomaly_score : float – lower is more anomalous
            is_anomaly    : bool
        """
        try:
            values = np.array([[reading[f] for f in self.features]])
        except KeyError as e:
            logger.warning("Missing feature %s – returning neutral score", e)
            return 0.0, False

        scaled = self.scaler.transform(values)
        score = float(self.model.decision_function(scaled)[0])
        prediction = int(self.model.predict(scaled)[0])
        is_anomaly = prediction == -1
        return score, is_anomaly
