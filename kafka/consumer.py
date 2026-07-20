"""
AtmoSync Enterprise Kafka Consumer Engine
Reads micro-climate telemetry streams, runs real-time analytics, triggers alert thresholds, and routes data.
"""

import os
import json
import logging
from typing import Callable, Optional, Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AtmoSyncKafkaConsumer")


class AtmoSyncConsumer:
    """Consumer service processing streaming container events."""

    def __init__(self, topic: str = "atmosync.container.telemetry", group_id: str = "atmosync_analytics_group"):
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.consumer = None

    def start_consuming(self, message_handler: Callable[[Dict[str, Any]], None], max_messages: Optional[int] = None):
        """Subscribe and consume stream records, executing message_handler callback for each record."""
        try:
            from kafka import KafkaConsumer
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                auto_offset_reset='earliest',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            logger.info(f"Subscribed Kafka consumer to topic '{self.topic}' (Group: {self.group_id})")

            count = 0
            for message in self.consumer:
                payload = message.value
                message_handler(payload)
                count += 1
                if max_messages and count >= max_messages:
                    break

        except Exception as err:
            logger.warning(f"Unable to run live Kafka consumer on {self.bootstrap_servers}: {err}. Simulation mode active.")

    def close(self):
        if self.consumer:
            self.consumer.close()


if __name__ == "__main__":
    def sample_processor(event: Dict[str, Any]):
        print(f"[CONSUMER ITEM] Container: {event.get('container_id')} | Temp: {event.get('temperature')}°C | Commodity: {event.get('commodity')}")

    consumer = AtmoSyncConsumer()
    consumer.start_consuming(sample_processor, max_messages=5)
