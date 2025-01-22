from typing import Optional
from confluent_kafka import Producer, Consumer
from ..events.types import VolumetricEvent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VolumetricEventHandler:
    """Dedicated handler for volumetric-related events"""

    DEFAULT_TOPIC = "volumetric_events"

    def __init__(
        self,
        producer: Optional[Producer] = None,
        consumer: Optional[Consumer] = None,
        topic: str = DEFAULT_TOPIC,
    ):
        self.producer = producer
        self.consumer = consumer
        self.topic = topic

    def publish_volumetric_event(self, event: VolumetricEvent) -> None:
        """Publish a volumetric event to the user events topic"""
        if not self.producer:
            raise ValueError("Producer not initialized")

        if not isinstance(event, VolumetricEvent):
            raise ValueError(f"Expected VolumetricEvent, got {type(event)}")

        try:
            self.producer.produce(
                topic=self.topic,
                key=event.user_id,  # Using user_id as the message key
                value=event.to_json().encode("utf-8"),
                callback=self._delivery_callback,
            )
            self.producer.flush()
            logger.info(
                f"Published user event: {event.event_id} for user: {event.user_id}"
            )
        except Exception as e:
            logger.error(f"Error publishing user event: {str(e)}")
            raise

    def consume_volumetric_events(self, callback=None):
        """Consume user events and process them"""
        if not self.consumer:
            raise ValueError("Consumer not initialized")

        try:
            self.consumer.subscribe([self.topic])
            logger.info(f"Subscribed to topic: {self.topic}")

            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue

                try:
                    event = VolumetricEvent.from_json(msg.value().decode("utf-8"))
                    if callback:
                        callback(event)
                    else:
                        self._default_event_handler(event)
                except Exception as e:
                    logger.error(f"Error processing user event: {str(e)}")

        except Exception as e:
            logger.error(f"Error consuming messages: {str(e)}")
        finally:
            self.consumer.close()

    def _delivery_callback(self, err, msg):
        """Callback for producer delivery reports"""
        if err:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def _default_event_handler(self, event: VolumetricEvent):
        """Default handler for user events"""
        logger.info(f"Processing user event: {event.event_id}")
        logger.info(f"User ID: {event.user_id}")
        logger.info(f"Action: {event.action}")
        logger.info(f"Details: {event.details}")
