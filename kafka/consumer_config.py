"""
Kafka Consumer Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_CONFIG = {
    "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    "topic": os.getenv("KAFKA_TOPIC", "iot-sensor-events"),
    "group_id": "iot-stream-processor",
    "auto_offset_reset": "latest",
    "enable_auto_commit": True,
    "value_deserializer": "json",  # handled in processor
}
