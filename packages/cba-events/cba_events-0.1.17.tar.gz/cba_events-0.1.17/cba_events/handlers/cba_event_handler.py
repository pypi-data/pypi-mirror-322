import json
from typing import Optional, Type
from confluent_kafka import Producer, Consumer
from ..events.base_event import BaseEvent
from ..events.types import VolumetricEvent


class CBAEventHandler:
    def __init__(
        self, producer: Optional[Producer] = None, consumer: Optional[Consumer] = None
    ):
        self.producer = producer
        self.consumer = consumer

    def publish_event(self, event: BaseEvent, topic: str) -> None:
        """Publish event to Kafka topic"""
        if not self.producer:
            raise ValueError("Producer not initialized")

        try:
            self.producer.produce(
                topic=topic,
                key=event.event_id,
                value=event.to_json().encode("utf-8"),
                callback=self._delivery_callback,
            )
            self.producer.flush()
        except Exception as e:
            raise Exception(f"Error publishing event: {str(e)}")

    def _delivery_callback(self, err, msg):
        """Callback for producer delivery reports"""
        if err:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def process_events(self, topic: str, event_type: Type[BaseEvent]) -> None:
        """Process events from Kafka topic"""
        if not self.consumer:
            raise ValueError("Consumer not initialized")

        try:
            self.consumer.subscribe([topic])
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                try:
                    event_data = json.loads(msg.value().decode("utf-8"))
                    event = event_type.from_dict(event_data)
                    self._handle_event(event)
                except Exception as e:
                    print(f"Error processing message: {str(e)}")

        except Exception as e:
            print(f"Error consuming messages: {str(e)}")
        finally:
            self.consumer.close()

    def _handle_event(self, event: BaseEvent) -> None:
        """Handle different event types"""
        if isinstance(event, VolumetricEvent):
            print(f"Processing user event: {event.user_id}, Action: {event.action}")
