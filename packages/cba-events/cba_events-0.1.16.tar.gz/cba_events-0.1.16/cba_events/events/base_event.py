from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime
import json
import uuid
from dataclasses_json import DataClassJsonMixin


@dataclass
class BaseEvent(DataClassJsonMixin):
    """Base event class with common attributes for all events"""

    event_id: str
    user_id: str
    event_type: str
    timestamp: str
    entity_id: str
    location: str
    site_id: str
    survey_date: str
    survey_id: str
    correlation_id: Optional[str] = None

    def __post_init__(self):
        # Automatically generate a unique event_id
        self.event_id = str(uuid.uuid4())

        # Set timestamp to current time if not provided
        if not self.timestamp:
            self.timestamp = datetime.now()

    def to_json(self) -> str:
        """Serialize the event to JSON"""
        event_dict = {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),  # Convert datetime to string
            "entity_id": self.entity_id,
            "location": self.location,
            "site_id": self.site_id,
            "survey_date": self.survey_date,
            "survey_id": self.survey_id,
            "correlation_id": self.correlation_id,
        }
        return json.dumps(event_dict)
