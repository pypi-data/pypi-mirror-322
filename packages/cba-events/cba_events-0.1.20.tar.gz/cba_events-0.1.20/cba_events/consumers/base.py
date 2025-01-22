from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Callable, Any
from ..events.base_event import BaseEvent

T = TypeVar("T", bound=BaseEvent)


class EventConsumer(ABC, Generic[T]):
    def __init__(self, topic: str):
        self.topic = topic

    @abstractmethod
    def consume(self, callback: Optional[Callable[[T], Any]] = None) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
