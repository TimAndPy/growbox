# GrowBox IoT Control System

An automated indoor plant cultivation system powered by NVIDIA Jetson Nano 2GB, featuring real-time environmental monitoring, automated control, and a tablet-based user interface.

## Features

- **Real-time Monitoring**: Track temperature, humidity, light intensity, and water levels
- **Automated Control**: Intelligent environmental control with hysteresis-based automation
- **Remote Management**: Control via MQTT from mobile app (Mendix)
- **Local Tablet UI**: Touch-friendly web interface for on-site control
- **Growth Phase Management**: Automated light schedules for vegetative (18/6) and flowering (12/12) phases
- **Safety Features**: 30-second watchdog failsafe, max runtime limits, cooldown periods
- **Historical Data**: Full-season SQLite database with indexed time-series data

## Hardware Requirements

### Components

- **Controller**: NVIDIA Jetson Nano 2GB Developer Kit
- **Sensors**:
  - DHT22 (Temperature & Humidity)
  - BH1750 (Light Intensity)
  - HC-SR04 (Ultrasonic Water Level)
- **Actuators**:
  - 5-Channel Relay Board
  - Grow Lights
  - Ventilation Fan
  - Water Pump
  - Heater
  - CO₂ Dispenser
- **Display**: Tablet for local control panel (connected via WiFi)

### GPIO Pin Mappings

| Device/Sensor | GPIO Pin | Type | Notes |
|---------------|----------|------|-------|
| DHT22 | GPIO 4 | Input | Temperature & Humidity |
| BH1750 | I2C Bus 1 (0x23) | I2C | Light sensor |
| HC-SR04 Trigger | GPIO 23 | Output | Water level sensor |
| HC-SR04 Echo | GPIO 24 | Input | Water level sensor |
| Lights Relay | GPIO 17 | Output | Active high |
| Ventilation Relay | GPIO 27 | Output | Active high |
| Pump Relay | GPIO 22 | Output | Active high |
| Heater Relay | GPIO 10 | Output | Active high |
| CO₂ Relay | GPIO 9 | Output | Active high |

## Software Requirements

- **OS**: Ubuntu 18.04 or 20.04 for Jetson Nano
- **Python**: 3.8 or higher
- **MQTT Broker**: Mosquitto or compatible (can be local or remote)

## Installation

### 1. Jetson Nano Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-dev git i2c-tools

# Enable I2C interface
sudo usermod -aG i2c $USER

# Verify I2C devices
i2cdetect -y -r 1
```

### 2. Clone Repository

```bash
cd ~
git clone https://github.com/yourusername/growbox.git
cd growbox
```

### 3. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. MQTT Broker Setup

#### Option A: Local Mosquitto Broker

```bash
# Install Mosquitto on Jetson Nano
sudo apt install -y mosquitto mosquitto-clients

# Enable and start service
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Test connection
mosquitto_sub -t "test" &
mosquitto_pub -t "test" -m "Hello"
```

#### Option B: Remote MQTT Broker

Update `config/mqtt.json` with your broker details:

```json
{
  "broker_url": "your-broker-url.com",
  "broker_port": 1883,
  "box_id": "001"
}
```

### 5. Database Initialization

```bash
# Create data directory
mkdir -p data

# Initialize database schema
python src/storage/init_db.py
```

### 6. Configuration

Update configuration files in `config/`:

**config/sensors.json** - Verify GPIO pins match your wiring
**config/devices.json** - Verify relay GPIO pins
**config/targets.json** - Set your environmental targets

### 7. Hardware Wiring

#### Power Supply

- **Jetson Nano**: 5V 4A barrel jack (recommended)
- **Relay Board**: External 5V supply (do NOT power from Jetson GPIO)
- **Sensors**: 3.3V from Jetson (pins 1 or 17)

#### Wiring Diagram

```
Jetson Nano 2GB
├─ GPIO 4  ──────────> DHT22 Data
├─ GPIO 17 ──────────> Relay CH1 (Lights)
├─ GPIO 27 ──────────> Relay CH2 (Ventilation)
├─ GPIO 22 ──────────> Relay CH3 (Pump)
├─ GPIO 10 ──────────> Relay CH4 (Heater)
├─ GPIO 9  ──────────> Relay CH5 (CO₂)
├─ GPIO 23 ──────────> HC-SR04 Trigger
├─ GPIO 24 ──────────> HC-SR04 Echo
├─ I2C SDA ──────────> BH1750 SDA
└─ I2C SCL ──────────> BH1750 SCL
```

**Safety Notes**:
- Connect relay common (COM) to mains/high voltage supply
- Use proper wire gauge for high current loads (lights, heater)
- Ensure proper grounding of all devices
- Add fuses to protect against overcurrent

## Running the System

### Start GrowBox Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run main application
python src/main.py
```

The application will:
1. Initialize database
2. Configure sensors and devices
3. Connect to MQTT broker
4. Start automation controller
5. Launch web UI on `http://0.0.0.0:5000`

### Access Tablet UI

Navigate to `http://<jetson-ip>:5000` from your tablet browser.

### First-Time Configuration

1. Access tablet UI
2. Verify sensor readings are displaying correctly
3. Manually test each device (ON/OFF buttons)
4. Adjust target parameters if needed
5. Enable automation mode
6. Set growth phase (vegetative or flowering)

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Tablet UI (Flask)                  │
│              http://jetson-ip:5000                  │
└─────────────────────────────────────────────────────┘
                          │
                    WebSocket
                          │
┌─────────────────────────────────────────────────────┐
│              Main Application (main.py)              │
│  ┌─────────────┐  ┌────────────┐  ┌─────────────┐  │
│  │  Sensors    │  │   MQTT     │  │ Automation  │  │
│  │  - DHT22    │  │  Publisher │  │ Controller  │  │
│  │  - BH1750   │  │ Subscriber │  │  Watchdog   │  │
│  │  - HC-SR04  │  └────────────┘  │  Scheduler  │  │
│  └─────────────┘         │         └─────────────┘  │
│  ┌─────────────┐         │         ┌─────────────┐  │
│  │  Devices    │         │         │  Database   │  │
│  │  - Lights   │  ┌──────▼──────┐  │  (SQLite)   │  │
│  │  - Fan      │  │ MQTT Broker │  │  WAL Mode   │  │
│  │  - Pump     │  └─────────────┘  └─────────────┘  │
│  │  - Heater   │                                     │
│  │  - CO₂      │                                     │
│  └─────────────┘                                     │
└─────────────────────────────────────────────────────┘
                          │
                         MQTT
                          │
                  ┌───────▼────────┐
                  │  Mendix Mobile │
                  │      App       │
                  └────────────────┘
```

## Automation Features

### Temperature Control

- **Heating**: Activates heater when temperature < 22°C
- **Cooling**: Activates ventilation when temperature > 25°C
- **Hysteresis**: ±0.5°C to prevent rapid cycling

### Humidity Control

- **Dehumidification**: Activates ventilation when humidity > 70%
- **Hysteresis**: ±3% to prevent rapid cycling

### Water Level Control

- **Auto-fill**: Activates pump when level < 30L
- **Safety**: Max runtime 5 minutes, 60-second cooldown

### Safety Features

- **Watchdog Failsafe**: All devices turn OFF if MQTT connection lost >30 seconds
- **Max Runtime Limits**: Pump (5 min), CO₂ (3 min)
- **Cooldown Periods**: Heater (60s), Pump (60s), CO₂ (5 min)

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run contract tests
pytest tests/contract/ -v -m contract

# Run integration tests
pytest tests/integration/ -v -m integration

# Run unit tests
pytest tests/unit/ -v -m unit

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code (if using black)
black src/

# Lint code (if using flake8)
flake8 src/

# Type checking (if using mypy)
mypy src/
```

## Troubleshooting

### Sensors Not Reading

1. Verify GPIO pin connections
2. Check I2C bus: `i2cdetect -y -r 1`
3. Ensure DHT22 has 10kΩ pull-up resistor on data line
4. Check power supply voltage (3.3V for sensors)

### Devices Not Responding

1. Verify relay board has external power supply
2. Check GPIO pin configuration in `config/devices.json`
3. Test GPIO manually: `sudo gpioinfo`
4. Verify relay board logic level (3.3V or 5V)

### MQTT Connection Issues

1. Verify broker is running: `sudo systemctl status mosquitto`
2. Test connectivity: `mosquitto_pub -t "test" -m "hello"`
3. Check firewall rules: `sudo ufw status`
4. Verify `config/mqtt.json` settings

### Web UI Not Accessible

1. Check Flask is running: `ps aux | grep python`
2. Verify port 5000 is not blocked: `sudo netstat -tulpn | grep 5000`
3. Try localhost first: `http://localhost:5000`
4. Check Jetson IP address: `hostname -I`

### Database Errors

1. Check database file exists: `ls -lh data/growbox.db`
2. Verify WAL mode: `sqlite3 data/growbox.db "PRAGMA journal_mode;"`
3. Check permissions: `ls -l data/`
4. Reinitialize if corrupted: `python src/storage/init_db.py`

## API Reference

### MQTT Topics

#### Sensor Data (Published)
- `growbox/001/sensors/temperature` (QoS 1, Retained)
- `growbox/001/sensors/humidity` (QoS 1, Retained)
- `growbox/001/sensors/light` (QoS 1, Retained)
- `growbox/001/sensors/water` (QoS 1, Retained)

#### Device Commands (Subscribed)
- `growbox/001/devices/lights/command` (QoS 2)
- `growbox/001/devices/ventilation/command` (QoS 2)
- `growbox/001/devices/pump/command` (QoS 2)
- `growbox/001/devices/heater/command` (QoS 2)
- `growbox/001/devices/co2/command` (QoS 2)

#### Device States (Published)
- `growbox/001/devices/{device}/state` (QoS 2, Retained)

#### System Status (Published)
- `growbox/001/status` (QoS 1, Retained)

### REST API Endpoints

- `GET /api/status` - System status
- `GET /api/sensors` - Latest sensor readings
- `GET /api/devices` - Device states
- `POST /api/device/<type>/<command>` - Control device
- `POST /api/auto_mode/<action>` - Enable/disable automation
- `POST /api/growth_phase/<phase>` - Switch growth phase

## Constitutional Principles

This project follows strict development principles:

1. **Code Minimalism**: No unnecessary abstractions
2. **Zero Redundancy**: DRY principle strictly enforced
3. **UI Consistency**: Unified design system
4. **Quality Over Speed**: Maintainability prioritized
5. **Clean Architecture**: Logical folder structure

## License

[Your License Here]

## Contributors

[Your Name/Team]

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Documentation: `specs/001-i-want-to/`

## Acknowledgments

- NVIDIA Jetson Nano Community
- Adafruit Libraries
- Eclipse Mosquitto MQTT Broker
- Flask & SocketIO Teams
