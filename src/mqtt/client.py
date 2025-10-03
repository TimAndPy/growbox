"""
MQTT client for GrowBox communication.
Handles connection, reconnection, and message publishing/subscribing.
"""

import json
import logging
from datetime import datetime
from typing import Callable, Optional
from pathlib import Path

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class MQTTClient:
    """MQTT client wrapper with automatic reconnection and Last Will."""

    def __init__(self, config_path: str = 'config/mqtt.json'):
        """
        Initialize MQTT client from configuration.

        Args:
            config_path: Path to MQTT configuration file
        """
        self.config = self._load_config(config_path)

        self.broker_url = self.config['broker_url']
        self.broker_port = self.config['broker_port']
        self.box_id = self.config['box_id']

        self.client = mqtt.Client(client_id=f"growbox_{self.box_id}")
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        self._is_connected = False
        self._message_callbacks = {}
        self._last_publish_time: Optional[datetime] = None

        self._setup_last_will()

    def _load_config(self, config_path: str) -> dict:
        """Load MQTT configuration from JSON file."""
        path = Path(config_path)
        if not path.exists():
            logger.error(f"MQTT config not found: {config_path}")
            raise FileNotFoundError(f"MQTT config not found: {config_path}")

        with open(path, 'r') as f:
            return json.load(f)

    def _setup_last_will(self):
        """Set up Last Will and Testament for connection loss."""
        status_topic = self.config['topics']['system_status'].format(box_id=self.box_id)
        lwt_payload = json.dumps({
            'connection_state': 'offline',
            'last_mqtt_publish': datetime.utcnow().isoformat(),
            'auto_mode_enabled': False,
            'active_alerts': ['mqtt_connection_lost']
        })

        self.client.will_set(
            topic=status_topic,
            payload=lwt_payload,
            qos=1,
            retain=True
        )

    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connection is established."""
        if rc == 0:
            self._is_connected = True
            logger.info(f"Connected to MQTT broker at {self.broker_url}:{self.broker_port}")

            # Resubscribe to topics
            for topic in self._message_callbacks.keys():
                client.subscribe(topic, qos=self.config['qos_device_commands'])
                logger.debug(f"Subscribed to topic: {topic}")
        else:
            self._is_connected = False
            logger.error(f"Failed to connect to MQTT broker: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from broker."""
        self._is_connected = False
        if rc != 0:
            logger.warning(f"Unexpected disconnect from MQTT broker: {rc}")
        else:
            logger.info("Disconnected from MQTT broker")

    def _on_message(self, client, userdata, msg):
        """Callback when message is received."""
        topic = msg.topic
        logger.debug(f"Received message on topic: {topic}")

        if topic in self._message_callbacks:
            try:
                payload = json.loads(msg.payload.decode('utf-8'))
                self._message_callbacks[topic](topic, payload)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from {topic}: {e}")
            except Exception as e:
                logger.error(f"Error processing message from {topic}: {e}")

    def connect(self) -> bool:
        """
        Connect to MQTT broker.

        Returns:
            True if connection successful
        """
        try:
            self.client.connect(self.broker_url, self.broker_port, keepalive=60)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()
        self._is_connected = False

    def is_connected(self) -> bool:
        """Check if connected to broker."""
        return self._is_connected

    def publish(self, topic: str, payload: dict, qos: int = 1, retain: bool = False) -> bool:
        """
        Publish message to MQTT topic.

        Args:
            topic: MQTT topic
            payload: Message payload as dictionary
            qos: Quality of Service level (0, 1, 2)
            retain: Retain message flag

        Returns:
            True if publish successful
        """
        if not self._is_connected:
            logger.error("Cannot publish: not connected to MQTT broker")
            return False

        try:
            message = json.dumps(payload)
            result = self.client.publish(topic, message, qos=qos, retain=retain)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self._last_publish_time = datetime.utcnow()
                logger.debug(f"Published to {topic}: {message[:100]}")
                return True
            else:
                logger.error(f"Failed to publish to {topic}: {result.rc}")
                return False

        except Exception as e:
            logger.error(f"Error publishing to {topic}: {e}")
            return False

    def subscribe(self, topic: str, callback: Callable[[str, dict], None], qos: int = 1):
        """
        Subscribe to MQTT topic with callback.

        Args:
            topic: MQTT topic to subscribe to
            callback: Function to call when message received (topic, payload)
            qos: Quality of Service level
        """
        self._message_callbacks[topic] = callback

        if self._is_connected:
            self.client.subscribe(topic, qos=qos)
            logger.info(f"Subscribed to topic: {topic}")

    def unsubscribe(self, topic: str):
        """Unsubscribe from MQTT topic."""
        if topic in self._message_callbacks:
            del self._message_callbacks[topic]

        if self._is_connected:
            self.client.unsubscribe(topic)
            logger.info(f"Unsubscribed from topic: {topic}")

    def get_last_publish_time(self) -> Optional[datetime]:
        """Get timestamp of last successful publish."""
        return self._last_publish_time

    def get_topic(self, topic_type: str, **kwargs) -> str:
        """
        Get formatted topic from configuration.

        Args:
            topic_type: Topic type (sensors, device_command, device_state, system_status)
            **kwargs: Additional format parameters (sensor, device, etc.)

        Returns:
            Formatted MQTT topic
        """
        template = self.config['topics'][topic_type]
        return template.format(box_id=self.box_id, **kwargs)
