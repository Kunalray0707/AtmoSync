"""
AtmoSync Kafka Topic Provisioning Tool
Creates topics with optimal partitions and replication factors.
"""

import os
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AtmoSyncKafkaTopics")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

TOPICS_CONFIG = {
    "atmosync.container.telemetry": {"partitions": 6, "replication_factor": 1},
    "atmosync.container.alerts": {"partitions": 3, "replication_factor": 1},
    "atmosync.container.dlq": {"partitions": 2, "replication_factor": 1},
    "atmosync.analytics.spoilage": {"partitions": 3, "replication_factor": 1},
    "atmosync.analytics.arbitrage": {"partitions": 3, "replication_factor": 1}
}


def create_kafka_topics(bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS) -> bool:
    """Creates Kafka topics if confluent_kafka or kafka-python admin client is available."""
    try:
        from kafka.admin import KafkaAdminClient, NewTopic
        admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers,
            client_id='atmosync_admin'
        )
        
        existing_topics = admin_client.list_topics()
        new_topics: List[NewTopic] = []
        
        for topic_name, cfg in TOPICS_CONFIG.items():
            if topic_name not in existing_topics:
                new_topics.append(
                    NewTopic(
                        name=topic_name,
                        num_partitions=cfg["partitions"],
                        replication_factor=cfg["replication_factor"]
                    )
                )
                
        if new_topics:
            admin_client.create_topics(new_topics=new_topics, validate_only=False)
            logger.info(f"Successfully created {len(new_topics)} Kafka topics.")
        else:
            logger.info("All Kafka topics already exist.")
        admin_client.close()
        return True
    except Exception as e:
        logger.warning(f"Could not connect to live Kafka broker at {bootstrap_servers}: {e}. Operating in graceful simulation mode.")
        return False


if __name__ == "__main__":
    create_kafka_topics()
