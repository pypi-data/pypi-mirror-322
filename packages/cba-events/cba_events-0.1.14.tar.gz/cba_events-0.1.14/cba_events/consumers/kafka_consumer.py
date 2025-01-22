from typing import Optional, Callable, Any, Type
from confluent_kafka import Consumer
from .base import EventConsumer, T
import json
import logging

logger = logging.getLogger(__name__)


class KafkaEventConsumer(EventConsumer[T]):
    def __init__(self, consumer: Consumer, topic: str, event_class: Type[T]):
        super().__init__(topic)
        self.consumer = consumer
        self.event_class = event_class
        self._running = False

    def consume(self, callback: Optional[Callable[[T], Any]] = None) -> None:
        try:
            self.consumer.subscribe([self.topic])
            self._running = True
            logger.info(f"Started consuming from topic: {self.topic}")

            while self._running:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue

                try:
                    event_data = json.loads(msg.value().decode("utf-8"))
                    event = self.event_class.from_dict(event_data)

                    if callback:
                        callback(event)
                    else:
                        self._default_handler(event)

                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")

        except Exception as e:
            logger.error(f"Error in consumer: {str(e)}")
        finally:
            self.close()

    def close(self) -> None:
        self._running = False
        self.consumer.close()
        logger.info(f"Closed consumer for topic: {self.topic}")

    def _default_handler(self, event: T) -> None:
        logger.info(f"Received event: {event.event_type} - {event.event_id}")
