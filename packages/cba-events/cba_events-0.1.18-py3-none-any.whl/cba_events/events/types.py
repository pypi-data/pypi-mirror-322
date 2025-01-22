from dataclasses import dataclass, field
import json
from typing import Optional, Dict, Any
from .base_event import BaseEvent


@dataclass
class StockpileEvent(BaseEvent):
    """Stockpile-related event class"""

    action: str = "calculate"
    data_source: str = "dem"
    method: str = "linear_plane"
    event_type: str = "stockpile_event"
    details: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Initialize any fields specific to StockpileEvent after BaseEvent's __post_init__ is called
        super().__post_init__()

        # Ensure that 'details' is properly initialized if it's an empty dictionary
        if self.details is None:
            self.details = {}

    def to_json(self) -> str:
        """Override to ensure all fields, including details, are JSON serializable"""
        # First, serialize the base event part (timestamp, event_id, etc.)
        event_dict = json.loads(
            super().to_json()
        )  # Get base event JSON as a dictionary

        # Serialize details field (it could be a complex structure, so handle with default=str)
        event_dict["details"] = json.dumps(
            self.details, default=str
        )  # Handle non-serializables

        return json.dumps(event_dict)


# @dataclass
class PitEvent(BaseEvent):
    """Stockpile-related event class"""

    action: str = "calculate"
    details: Dict[str, Any] = field(default_factory=dict)

    def __init__(
        self,
        site_id: str,
        location: str,
        entity_id: str,
        survey_date: str,
        user_id: str,
        survey_id: str,
        action: str,
        **kwargs,
    ):
        super().__init__(
            event_type="pit_event",
            entity_id=entity_id,
            location=location,
            site_id=site_id,
            survey_date=survey_date,
            user_id=user_id,
            survey_id=survey_id,
        )
        self.action = action
        self.details = kwargs.get("details", {})


# @dataclass
class VolumetricEvent(BaseEvent):
    """Stockpile-related event class"""

    action: str = "calculate"
    details: Dict[str, Any] = field(default_factory=dict)

    def __init__(
        self,
        site_id: str,
        location: str,
        entity_id: str,
        survey_date: str,
        user_id: str,
        survey_id: str,
        action: str,
        **kwargs,
    ):
        super().__init__(
            event_type="volumetric_event",
            entity_id=entity_id,
            location=location,
            site_id=site_id,
            survey_date=survey_date,
            user_id=user_id,
            survey_id=survey_id,
        )
        self.action = action
        self.details = kwargs.get("details", {})
