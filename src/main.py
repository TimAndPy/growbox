"""
Main application entry point for GrowBox.
Orchestrates all components: sensors, devices, MQTT, automation, and UI.
"""

import logging
import sys
import time
import threading
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.logging_config import setup_logging

from storage.database import DatabaseInterface
from storage.init_db import initialize_database

from sensors.temperature import TemperatureSensor
from sensors.humidity import HumiditySensor
from sensors.light import LightSensor
from sensors.water import WaterLevelSensor

from devices.lights import LightsController
from devices.ventilation import VentilationController
from devices.pump import PumpController
from devices.heater import HeaterController
from devices.co2 import CO2Controller

from mqtt.client import MQTTClient
from mqtt.publisher import MQTTPublisher
from mqtt.subscriber import MQTTSubscriber

from automation.controller import AutomationController
from automation.watchdog import CommunicationWatchdog
from automation.scheduler import GrowthPhaseScheduler

from ui.app import init_app, run_app, broadcast_sensor_update, broadcast_device_update

logger = logging.getLogger(__name__)


class GrowBoxApplication:
    """Main GrowBox application orchestrator."""

    def __init__(self, config_dir='config', data_dir='data'):
        """
        Initialize GrowBox application.

        Args:
            config_dir: Configuration directory path
            data_dir: Data directory path
        """
        self.config_dir = Path(config_dir)
        self.data_dir = Path(data_dir)

        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        Path('logs').mkdir(exist_ok=True)

        # Component initialization
        self.database = None
        self.sensors = {}
        self.devices = {}
        self.mqtt_client = None
        self.mqtt_publisher = None
        self.mqtt_subscriber = None
        self.automation = None
        self.watchdog = None
        self.scheduler = None

        self._running = False
        self._sensor_thread = None

    def initialize_database(self):
        """Initialize database schema and connection."""
        logger.info("Initializing database...")

        db_path = self.data_dir / 'growbox.db'

        # Initialize schema if needed
        if not db_path.exists():
            initialize_database(db_path)

        # Create database interface
        self.database = DatabaseInterface(str(db_path))
        self.database.connect()

        logger.info("Database initialized")

    def initialize_sensors(self):
        """Initialize all sensor modules from configuration."""
        logger.info("Initializing sensors...")

        import json
        config_path = self.config_dir / 'sensors.json'

        with open(config_path, 'r') as f:
            sensor_config = json.load(f)

        # Initialize temperature sensor
        temp_config = sensor_config['temperature']
        self.sensors['temperature'] = TemperatureSensor(
            gpio_pin=temp_config['gpio_pin']
        )

        # Initialize humidity sensor (shares DHT22 with temperature)
        humidity_config = sensor_config['humidity']
        self.sensors['humidity'] = HumiditySensor(
            gpio_pin=humidity_config['gpio_pin']
        )

        # Initialize light sensor
        light_config = sensor_config['light']
        self.sensors['light'] = LightSensor(
            i2c_bus=light_config['i2c_bus'],
            i2c_address=int(light_config['i2c_address'], 16)
        )

        # Initialize water level sensor
        water_config = sensor_config['water']
        self.sensors['water'] = WaterLevelSensor(
            gpio_trigger_pin=water_config['gpio_trigger_pin'],
            gpio_echo_pin=water_config['gpio_echo_pin']
        )

        logger.info(f"Initialized {len(self.sensors)} sensors")

    def initialize_devices(self):
        """Initialize all device controllers from configuration."""
        logger.info("Initializing devices...")

        import json
        config_path = self.config_dir / 'devices.json'

        with open(config_path, 'r') as f:
            device_config = json.load(f)

        # Initialize lights
        lights_config = device_config['lights']
        self.devices['lights'] = LightsController(
            gpio_pin=lights_config['gpio_pin'],
            active_high=lights_config['active_high']
        )

        # Initialize ventilation
        vent_config = device_config['ventilation']
        self.devices['ventilation'] = VentilationController(
            gpio_pin=vent_config['gpio_pin'],
            active_high=vent_config['active_high']
        )

        # Initialize pump
        pump_config = device_config['pump']
        self.devices['pump'] = PumpController(
            gpio_pin=pump_config['gpio_pin'],
            active_high=pump_config.get('active_high', True),
            max_runtime_seconds=pump_config.get('max_runtime_seconds', 300),
            cooldown_seconds=pump_config.get('cooldown_seconds', 60)
        )

        # Initialize heater
        heater_config = device_config['heater']
        self.devices['heater'] = HeaterController(
            gpio_pin=heater_config['gpio_pin'],
            active_high=heater_config.get('active_high', True),
            cooldown_seconds=heater_config.get('cooldown_seconds', 60)
        )

        # Initialize CO2
        co2_config = device_config['co2']
        self.devices['co2'] = CO2Controller(
            gpio_pin=co2_config['gpio_pin'],
            active_high=co2_config.get('active_high', True),
            max_runtime_seconds=co2_config.get('max_runtime_seconds', 180),
            cooldown_seconds=co2_config.get('cooldown_seconds', 300)
        )

        logger.info(f"Initialized {len(self.devices)} devices")

    def initialize_mqtt(self):
        """Initialize MQTT client and communication layer."""
        logger.info("Initializing MQTT...")

        config_path = self.config_dir / 'mqtt.json'
        self.mqtt_client = MQTTClient(str(config_path))

        # Connect to broker
        if self.mqtt_client.connect():
            logger.info("Connected to MQTT broker")
        else:
            logger.error("Failed to connect to MQTT broker")

        # Initialize publisher and subscriber
        self.mqtt_publisher = MQTTPublisher(self.mqtt_client)
        self.mqtt_subscriber = MQTTSubscriber(self.mqtt_client)

        # Register device command handlers
        for device_type in self.devices.keys():
            self.mqtt_subscriber.register_device_handler(
                device_type,
                self._handle_device_command
            )

        logger.info("MQTT communication layer initialized")

    def initialize_automation(self):
        """Initialize automation, watchdog, and scheduler."""
        logger.info("Initializing automation...")

        # Automation controller
        self.automation = AutomationController(self.database, self.devices)

        # Communication watchdog
        self.watchdog = CommunicationWatchdog(
            devices=self.devices,
            timeout_seconds=30
        )
        self.watchdog.set_failsafe_callback(self._on_failsafe)

        # Growth phase scheduler
        self.scheduler = GrowthPhaseScheduler(
            database=self.database,
            lights=self.devices['lights']
        )
        self.scheduler.load_current_phase()

        logger.info("Automation layer initialized")

    def initialize_ui(self):
        """Initialize Flask web UI."""
        logger.info("Initializing web UI...")

        init_app(
            database=self.database,
            devices=self.devices,
            automation=self.automation,
            scheduler=self.scheduler
        )

        logger.info("Web UI initialized")

    def start(self):
        """Start all GrowBox services."""
        logger.info("Starting GrowBox application...")

        self._running = True

        # Start watchdog
        self.watchdog.start()

        # Start sensor reading thread
        self._sensor_thread = threading.Thread(target=self._sensor_loop, daemon=True)
        self._sensor_thread.start()

        # Start Flask app (blocking)
        logger.info("GrowBox application started")
        run_app(host='0.0.0.0', port=5000)

    def stop(self):
        """Stop all GrowBox services and clean up resources."""
        logger.info("Stopping GrowBox application...")

        self._running = False

        # Stop watchdog
        if self.watchdog:
            self.watchdog.stop()

        # Disconnect MQTT
        if self.mqtt_client:
            self.mqtt_client.disconnect()

        # Clean up sensors
        for sensor in self.sensors.values():
            sensor.cleanup()

        # Clean up devices (turn off and release GPIO)
        for device in self.devices.values():
            device.turn_off()
            device.cleanup()

        # Close database
        if self.database:
            self.database.close()

        logger.info("GrowBox application stopped")

    def _sensor_loop(self):
        """Main sensor reading loop (runs in separate thread)."""
        logger.info("Sensor reading loop started")

        while self._running:
            try:
                # Read all sensors
                for sensor_type, sensor in self.sensors.items():
                    reading = sensor.read()

                    # Store in database
                    self.database.insert_sensor_reading(reading)

                    # Publish to MQTT
                    self.mqtt_publisher.publish_sensor_reading(reading)

                    # Broadcast to UI
                    broadcast_sensor_update(sensor_type, reading)

                    # Process for automation
                    if self.automation.is_enabled():
                        self.automation.process_sensor_reading(reading)

                # Update system status
                self.database.update_system_status(
                    last_sensor_read=reading.timestamp
                )

                # Check device max runtime
                self.automation.check_device_max_runtime()

                # Check light schedule
                self.scheduler.check_light_schedule()

                # Reset watchdog
                self.watchdog.reset()

                # Publish heartbeat
                self.mqtt_publisher.publish_heartbeat()

                # Wait before next reading (5 seconds)
                time.sleep(5)

            except Exception as e:
                logger.error(f"Error in sensor loop: {e}")
                time.sleep(5)

    def _handle_device_command(self, device_type: str, command: str):
        """
        Handle device command from MQTT.

        Args:
            device_type: Device type
            command: Command (on/off/auto)
        """
        logger.info(f"Received MQTT command: {device_type} -> {command}")

        if device_type not in self.devices:
            logger.error(f"Unknown device: {device_type}")
            return

        device = self.devices[device_type]

        if command == 'on':
            success = device.turn_on()
        elif command == 'off':
            success = device.turn_off()
        elif command == 'auto':
            self.automation.enable()
            return
        else:
            logger.error(f"Unknown command: {command}")
            return

        if success:
            # Log to database
            from storage.models import DeviceControl
            from datetime import datetime

            control = DeviceControl(
                device_type=device_type,
                state=command,
                command_source='remote',
                triggered_by='mqtt_command',
                timestamp=datetime.utcnow()
            )
            self.database.insert_device_state(control)

            # Publish state update
            self.mqtt_publisher.publish_device_state(control)

            # Broadcast to UI
            broadcast_device_update(device_type, command)

    def _on_failsafe(self):
        """Callback when watchdog triggers failsafe."""
        logger.critical("Failsafe callback executed")

        # Disable automation
        self.automation.disable()

        # Update system status
        self.database.update_system_status(
            connection_state='offline',
            auto_mode_enabled=False
        )

        # Log failsafe event for all devices
        from storage.models import DeviceControl
        from datetime import datetime

        for device_type in self.devices.keys():
            control = DeviceControl(
                device_type=device_type,
                state='off',
                command_source='failsafe',
                triggered_by='communication_timeout',
                timestamp=datetime.utcnow()
            )
            self.database.insert_device_state(control)


def main():
    """Main entry point."""
    # Initialize logging first
    setup_logging()

    logger.info("=" * 60)
    logger.info("GrowBox IoT Control System")
    logger.info("=" * 60)

    app = GrowBoxApplication()

    try:
        app.initialize_database()
        app.initialize_sensors()
        app.initialize_devices()
        app.initialize_mqtt()
        app.initialize_automation()
        app.initialize_ui()
        app.start()

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        app.stop()


if __name__ == '__main__':
    main()
