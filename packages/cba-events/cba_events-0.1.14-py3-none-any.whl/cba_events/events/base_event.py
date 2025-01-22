from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime
import json
import uuid
from dataclasses_json import DataClassJsonMixin


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

    def __init__(
        self,
        entity_id: str,
        location: str,
        site_id: str,
        survey_date: str,
        event_type: str,
        user_id: str,
        survey_id: str,
        correlation_id: Optional[str] = None,
    ):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.timestamp = datetime.now()
        self.entity_id = entity_id
        self.site_id = site_id
        self.correlation_id = correlation_id
        self.location = location
        self.survey_date = survey_date
        self.user_id = user_id
        self.survey_id = survey_id
