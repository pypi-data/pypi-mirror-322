# cba-events
A Python package for handling Kafka events with strong typing and serialization support.

## Installation

```bash
pip install cba-events
```

## Usage

```python
from cba_events.events.types import VolumetricEvent
from cba_events.handlers.kafka import VolumetricEventHandler
from confluent_kafka import Producer

# Configure Kafka producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Create event handler
handler = VolumetricEventHandler(producer)

# Create and publish event
event = VolumetricEvent(
    event_id="123",
    action="calculate",
    payload={"tin": "tin file name"}
)
handler.publish_event(event, "volumetric_events")
```

## Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests: `pytest`

# Example usage:
"""
# Volumentric Producer example
from confluent_kafka import Producer
from cba_events.events.types import VolumetricEvent
from cba_events.handlers.vol_metric_handler import VolumetricEventHandler

producer_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(producer_config)
vol_handler = VolumetricEventHandler(producer=producer)

# Create and publish a volumetric event
calculate_event = VolumetricEvent(
    user_id="user123",
    action="calculate",
    payload={"dem": "demfilename", "shapes": "shapes"}
)

vol_handler.publish_volumetric_event(calculate_event)

# Consumer example
from confluent_kafka import Consumer

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'volumetric_events_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
vol_handler = VolumetricEventHandler(consumer=consumer)

# Custom callback
def handle_vol_event(event):    
    print(f"Custom handling for user {event.user_id}")
    print(f"Action: {event.action}")
    print(f"Payload: {event.payload}")

# Start consuming with custom callback
user_handler.consume_volumetric_events(callback=handle_vol_event)
"""