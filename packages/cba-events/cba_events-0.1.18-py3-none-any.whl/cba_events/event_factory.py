from typing import Dict, Type, Optional
from confluent_kafka import Producer, Consumer
from .events.types import BaseEvent
from .events.types import StockpileEvent, PitEvent
from .publishers.kafka import KafkaEventPublisher
from .consumers.kafka_consumer import KafkaEventConsumer
from .handlers.stockpile_handler import StockpileEventHandler


class EventFactory:
    def __init__(
        self, producer: Optional[Producer] = None, consumer: Optional[Consumer] = None
    ):
        self.producer = producer
        self._publishers: Dict[str, KafkaEventPublisher] = {}
        self._consumers: Dict[str, KafkaEventConsumer] = {}
        self._topics: Dict[str, str] = {
            "stockpile_event": "stockpile_events",
            "pit_event": "pit_events",
            "waste_dump_event": "waste_dump_events",
        }
        self._event_types: Dict[str, Type[BaseEvent]] = {
            "stockpile_event": StockpileEvent,
            "pit_event": PitEvent,
            #'waste_dump_event': WasteDumpEvent
        }

        self._event_handlers = {
            "stockpile_event": StockpileEventHandler()
            #'pit_event': PitEventHandler(),
            #'waste_dump_event': WastedumpEventHandler()
        }

    def get_publisher(self, event_type: str) -> KafkaEventPublisher:

        if event_type not in self._publishers:
            if not self.producer:
                raise ValueError("Producer not initialized")
            topic = self._topics.get(event_type)
            if not topic:
                raise ValueError(f"Unknown event type: {event_type}")
            self._publishers[event_type] = KafkaEventPublisher(
                producer=self.producer, default_topic=topic
            )
        return self._publishers[event_type]

    def get_consumer(self, event_type: str) -> KafkaEventConsumer:
        if event_type not in self._consumers:
            if not self.consumer:
                raise ValueError("Consumer not initialized")
            topic = self._topics.get(event_type)
            event_class = self._event_types.get(event_type)
            if not topic or not event_class:
                raise ValueError(f"Unknown event type: {event_type}")
            self._consumers[event_type] = KafkaEventConsumer(
                consumer=self.consumer, topic=topic, event_class=event_class
            )
        return self._consumers[event_type]

    def create_event(self, event_type: str, **kwargs) -> BaseEvent:
        """Create an event of the specified type"""
        event_class = self._event_types.get(event_type)
        if not event_class:
            raise ValueError(f"Unknown event type: {event_type}")
        return event_class(**kwargs)

    def publish_event(self, event: BaseEvent, topic: Optional[str] = None) -> None:
        """Publish an event using the appropriate publisher"""
        publisher = self.get_publisher(event.event_type)
        publisher.publish(event, topic)

    def get_handler(self, event_type: str):
        return self._event_handlers.get(event_type)
