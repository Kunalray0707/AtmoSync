"""
AtmoSync Enterprise Kafka Producer Engine
Features schema validation, JSON serialization, retries, and fallback buffer mode.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from kafka.schemas import TelemetryEventSchema, AlertEventSchema, DLQEventSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AtmoSyncKafkaProducer")


class AtmoSyncProducer:
    """Production-grade Kafka Producer with schema validation & fallback buffer."""

    def __init__(self, bootstrap_servers: Optional[str] = None):
        self.bootstrap_servers = bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = None
        self.fallback_buffer = []
        self._init_producer()

    def _init_producer(self):
        try:
            from kafka import KafkaProducer
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                retries=5,
                acks='all',
                max_in_flight_requests_per_connection=1
            )
            logger.info(f"Kafka Producer initialized for broker: {self.bootstrap_servers}")
        except Exception as e:
            logger.warning(f"Kafka broker unavailable at {self.bootstrap_servers}: {e}. Fallback memory buffer active.")
            self.producer = None

    def send_telemetry(self, telemetry_dict: Dict[str, Any], topic: str = "atmosync.container.telemetry") -> bool:
        """Validate and send container telemetry event to Kafka."""
        try:
            # Pydantic Schema Validation
            validated_event = TelemetryEventSchema(**telemetry_dict).model_dump()
            container_id = validated_event["container_id"]

            if self.producer:
                self.producer.send(topic, key=container_id, value=validated_event)
                logger.debug(f"Published telemetry for {container_id} to topic {topic}")
            else:
                self.fallback_buffer.append({"topic": topic, "key": container_id, "payload": validated_event})
                if len(self.fallback_buffer) > 1000:
                    self.fallback_buffer.pop(0)  # Circular buffer cap
            return True
        except Exception as err:
            logger.error(f"Schema validation or send error for telemetry: {err}")
            self.send_to_dlq(topic, telemetry_dict, str(err))
            return False

    def send_alert(self, alert_dict: Dict[str, Any], topic: str = "atmosync.container.alerts") -> bool:
        """Send alert event to Kafka alert topic."""
        try:
            validated = AlertEventSchema(**alert_dict).model_dump()
            if self.producer:
                self.producer.send(topic, key=validated["container_id"], value=validated)
            else:
                self.fallback_buffer.append({"topic": topic, "key": validated["container_id"], "payload": validated})
            return True
        except Exception as e:
            logger.error(f"Alert schema validation error: {e}")
            return False

    def send_to_dlq(self, failed_topic: str, failed_event: Dict[str, Any], error_msg: str):
        """Send corrupted or failed payload to Dead Letter Queue (DLQ)."""
        dlq_payload = DLQEventSchema(
            original_topic=failed_topic,
            failed_event=failed_event,
            error_message=error_msg,
            failed_at=datetime.now(timezone.utc).isoformat(),
            retry_count=1
        ).model_dump()

        if self.producer:
            self.producer.send("atmosync.container.dlq", value=dlq_payload)
        else:
            logger.info(f"[DLQ Buffer] Recorded failed event for topic {failed_topic}: {error_msg}")

    def flush(self):
        if self.producer:
            self.producer.flush()


# Global Singleton Instance
kafka_producer = AtmoSyncProducer()
