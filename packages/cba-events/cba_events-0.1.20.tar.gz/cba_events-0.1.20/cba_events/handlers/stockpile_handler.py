from typing import Dict, Any
from ..events.types import StockpileEvent
import logging

logger = logging.getLogger(__name__)


class StockpileEventHandler:
    def handle_event(self, event: StockpileEvent) -> None:
        logger.info(f"Processing stockpile event: {event.event_id}")
        logger.info(f"User ID: {event.user_id}")
        logger.info(f"Action: {event.action}")
        logger.info(f"Survey ID: {event.survey_id}")

        # Handle different stockpile actions
        if event.action == "calculate":
            self._handle_calculate(event)

    def _handle_calculate(self, event: StockpileEvent) -> None:
        # begining Calculation
        logger.info(f"User {event.user_id} logged in")
        print(f" Stockpile Event successfully processed {event.event_id}")
