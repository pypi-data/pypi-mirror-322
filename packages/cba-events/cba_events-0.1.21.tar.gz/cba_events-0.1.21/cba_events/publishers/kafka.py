from confluent_kafka import Producer
from typing import Optional, Dict, Any
import logging

from .base import EventPublisher, T


logger = logging.getLogger(__name__)


class KafkaEventPublisher(EventPublisher[T]):
    def __init__(self, producer: Producer, default_topic: Optional[str] = None):
        self.producer = producer
        self.default_topic = default_topic

    def publish(self, event: T, topic: Optional[str] = None) -> None:
        publish_topic = topic or self.default_topic
        if not publish_topic:
            raise ValueError(
                "Topic must be specified either during initialization or publish"
            )

        try:
            self.producer.produce(
                topic=publish_topic,
                key=self._get_key(event),
                value=event.to_json().encode("utf-8"),
                callback=self._delivery_callback,
            )
            self.producer.flush()
            logger.info(f"Published {event.event_type} event: {event.event_id}")
        except Exception as e:
            logger.error(f"Error publishing event: {str(e)}")
            raise

    def _get_key(self, event: T) -> str:
        """Extract appropriate key based on event type"""
        if hasattr(event, "survey_id"):
            return str(event.survey_id)

    def _delivery_callback(self, err, msg):
        if err:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")
