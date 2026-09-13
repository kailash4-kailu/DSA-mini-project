"""
Kafka Producer
===============
Reads sensor data from a CSV file and streams it to a Kafka topic
one record at a time, simulating real-time IoT data arrival.

The delay between messages is configurable via STREAM_DELAY env var
(default 0.5 seconds) so that the dashboard visibly updates during demos.
"""

import os
import sys
import csv
import json
import time
import argparse
import logging
from datetime import datetime

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from dotenv import load_dotenv

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("kafka.producer")


def create_producer(bootstrap_servers: str, retries: int = 10, wait: float = 3.0):
    """Create a KafkaProducer with retry logic for broker availability."""
    for attempt in range(1, retries + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks="all",
            )
            logger.info("Connected to Kafka at %s", bootstrap_servers)
            return producer
        except NoBrokersAvailable:
            logger.warning(
                "Kafka not available (attempt %d/%d). Retrying in %.1fs…",
                attempt, retries, wait,
            )
            time.sleep(wait)
    raise ConnectionError(f"Could not connect to Kafka at {bootstrap_servers} after {retries} attempts")


def stream_csv(csv_path: str, topic: str, bootstrap_servers: str, delay: float, loop: bool = False):
    """Stream CSV rows to Kafka, one at a time."""
    producer = create_producer(bootstrap_servers)

    def _send_file():
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                # Use current timestamp for live feel
                row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                # Cast numeric fields
                for field in ["temperature", "humidity", "pressure", "vibration"]:
                    try:
                        row[field] = float(row[field])
                    except (ValueError, KeyError):
                        pass

                producer.send(topic, value=row)
                producer.flush()

                if i % 50 == 0:
                    logger.info("Sent %d events to topic '%s'", i, topic)
                else:
                    logger.debug("Sent event %d: device=%s temp=%.1f", i, row.get("device_id"), row.get("temperature", 0))

                time.sleep(delay)

        logger.info("Finished streaming file %s", csv_path)

    try:
        if loop:
            cycle = 1
            while True:
                logger.info("Starting streaming cycle %d", cycle)
                _send_file()
                cycle += 1
        else:
            _send_file()
    except KeyboardInterrupt:
        logger.info("Producer stopped by user.")
    finally:
        producer.close()


def main():
    parser = argparse.ArgumentParser(description="Kafka IoT Sensor Producer")
    parser.add_argument(
        "--data",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "..", "data", "sensor_data.csv"),
        help="Path to sensor CSV file",
    )
    parser.add_argument("--topic", type=str, default=None, help="Kafka topic")
    parser.add_argument("--delay", type=float, default=None, help="Delay between messages (seconds)")
    parser.add_argument("--loop", action="store_true", help="Loop the CSV continuously")
    parser.add_argument("--bootstrap-servers", type=str, default=None, help="Kafka bootstrap servers")
    args = parser.parse_args()

    topic = args.topic or os.getenv("KAFKA_TOPIC", "iot-sensor-events")
    delay = args.delay if args.delay is not None else float(os.getenv("STREAM_DELAY", "0.5"))
    servers = args.bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    logger.info("Producer config: topic=%s  delay=%.2fs  loop=%s", topic, delay, args.loop)
    stream_csv(args.data, topic, servers, delay, args.loop)


if __name__ == "__main__":
    main()
