from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from ..events.base_event import BaseEvent

T = TypeVar("T", bound=BaseEvent)


class EventPublisher(ABC, Generic[T]):

    @abstractmethod
    def publish(self, event: T, topic: str) -> None:
        pass
