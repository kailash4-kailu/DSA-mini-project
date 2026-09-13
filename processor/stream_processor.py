"""
Stream Processor
==================
Consumes sensor events from Kafka, applies DSA data structures, scores
with the Isolation Forest model, and writes results to MySQL.

Pipeline per event:
  1. Deserialize & validate JSON
  2. Update sliding windows (deque)       → rolling averages
  3. Update running statistics            → count / sum / avg / min / max
  4. Score with Isolation Forest           → anomaly_score, is_anomaly
  5. Update heap anomaly tracker          → top-N most anomalous
  6. Insert reading into MySQL            → sensor_readings
  7. Upsert device metrics in MySQL       → sensor_metrics
"""

import os
import sys
import json
import time
import logging
import argparse

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from dotenv import load_dotenv

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from processor.window_manager import WindowManager
from processor.statistics import StatisticsTracker
from processor.anomaly_tracker import AnomalyTracker
from ml.model_utils import AnomalyScorer
from database.db import insert_reading, upsert_metrics

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("stream.processor")

REQUIRED_FIELDS = ["timestamp", "device_id", "temperature", "humidity", "pressure", "vibration"]


def validate_event(event: dict) -> bool:
    """Validate that an event has all required fields and numeric values."""
    for field in REQUIRED_FIELDS:
        if field not in event:
            logger.warning("Missing field '%s' in event: %s", field, event)
            return False
    for field in ["temperature", "humidity", "pressure", "vibration"]:
        try:
            float(event[field])
        except (ValueError, TypeError):
            logger.warning("Non-numeric value for '%s': %s", field, event.get(field))
            return False
    return True


def create_consumer(bootstrap_servers: str, topic: str, retries: int = 10, wait: float = 3.0):
    """Create a KafkaConsumer with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                group_id="iot-stream-processor",
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                consumer_timeout_ms=-1,  # block forever
            )
            logger.info("Connected to Kafka consumer on topic '%s'", topic)
            return consumer
        except NoBrokersAvailable:
            logger.warning("Kafka not available (attempt %d/%d). Retrying in %.1fs…", attempt, retries, wait)
            time.sleep(wait)
    raise ConnectionError(f"Could not connect to Kafka after {retries} attempts")


def run_processor(bootstrap_servers: str, topic: str, model_path: str):
    """Main processing loop."""
    # ── Initialise DSA structures ──
    window_mgr = WindowManager(window_size=30)
    stats_tracker = StatisticsTracker()
    anomaly_tracker = AnomalyTracker(max_size=20)

    # ── Load ML model ──
    scorer = AnomalyScorer(model_path)
    logger.info("Anomaly scorer loaded.")

    # ── Connect to Kafka ──
    consumer = create_consumer(bootstrap_servers, topic)

    processed = 0
    logger.info("Waiting for events on topic '%s'…", topic)

    try:
        for message in consumer:
            event = message.value

            # 1. Validate
            if not validate_event(event):
                continue

            device_id = event["device_id"]

            # Cast numerics
            reading = {
                "temperature": float(event["temperature"]),
                "humidity": float(event["humidity"]),
                "pressure": float(event["pressure"]),
                "vibration": float(event["vibration"]),
            }

            # 2. Sliding window → rolling averages  (Deque – O(1) append)
            rolling = window_mgr.add_reading(device_id, reading)

            # 3. ML scoring  (O(t·log ψ) per event)
            anomaly_score, is_anomaly = scorer.score(reading)

            # 4. Running statistics  (O(1) update)
            stats_tracker.update(device_id, reading, is_anomaly)

            # 5. Top-N anomaly heap  (O(log N) insertion)
            if is_anomaly:
                heap_entry = {**reading, "device_id": device_id, "timestamp": event["timestamp"]}
                anomaly_tracker.add(anomaly_score, heap_entry)

            # 6. Write to MySQL: sensor_readings
            db_row = {
                "timestamp": event["timestamp"],
                "device_id": device_id,
                **reading,
                **rolling,
                "anomaly_score": round(anomaly_score, 6),
                "is_anomaly": 1 if is_anomaly else 0,
            }
            try:
                insert_reading(db_row)
            except Exception as e:
                logger.error("DB insert failed: %s", e)

            # 7. Upsert device metrics
            try:
                metrics_row = stats_tracker.get_metrics_for_db(device_id, reading, anomaly_score)
                upsert_metrics(metrics_row)
            except Exception as e:
                logger.error("DB upsert_metrics failed: %s", e)

            processed += 1
            if processed % 50 == 0:
                logger.info(
                    "Processed %d events | last device=%s anomaly=%s score=%.4f",
                    processed, device_id, is_anomaly, anomaly_score,
                )
                # Log top anomaly threshold
                thresh = anomaly_tracker.peek_threshold()
                if thresh is not None:
                    logger.info("Top-anomaly heap size=%d  threshold_score=%.4f", anomaly_tracker.size, thresh)

    except KeyboardInterrupt:
        logger.info("Processor stopped by user. Total processed: %d", processed)
    finally:
        consumer.close()


def main():
    parser = argparse.ArgumentParser(description="IoT Stream Processor")
    parser.add_argument("--bootstrap-servers", type=str, default=None)
    parser.add_argument("--topic", type=str, default=None)
    parser.add_argument("--model", type=str, default=None)
    args = parser.parse_args()

    servers = args.bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = args.topic or os.getenv("KAFKA_TOPIC", "iot-sensor-events")
    model = args.model or os.getenv(
        "MODEL_PATH",
        os.path.join(PROJECT_ROOT, "models", "anomaly_model.pkl"),
    )

    run_processor(servers, topic, model)


if __name__ == "__main__":
    main()
