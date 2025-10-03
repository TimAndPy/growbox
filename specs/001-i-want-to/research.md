# Research: GrowBox IoT Control System

**Date**: 2025-10-03
**Phase**: 0 - Outline & Research
**Purpose**: Resolve technical unknowns and establish best practices for implementation

---

## Research Questions

### 1. NVIDIA Jetson Nano GPIO Library Selection

**Decision**: Use Jetson.GPIO library (official NVIDIA library)

**Rationale**:
- Official support from NVIDIA for Jetson Nano
- RPi.GPIO-compatible API (familiar to developers)
- Direct hardware access without additional abstraction layers
- Active maintenance and community support
- Compatible with Python 3.6+ (our target: Python 3.9+)

**Alternatives Considered**:
- **Adafruit_Blinka**: Cross-platform but adds abstraction overhead
- **gpiozero**: Higher-level but less direct control for real-time requirements
- **sysfs GPIO**: Deprecated in newer kernels, not recommended

**Best Practices**:
- Use BCM pin numbering for consistency
- Implement proper GPIO cleanup on shutdown
- Use pull-up/pull-down resistors for reliable sensor readings
- Debounce water level sensor (float switch)

---

### 2. MQTT Broker Selection and Configuration

**Decision**: Mosquitto MQTT broker (self-hosted or cloud service)

**Rationale**:
- Lightweight and efficient (important for 2GB RAM constraint)
- Supports MQTT 3.1.1 and 5.0 protocols
- QoS levels 0, 1, 2 for reliability options
- Well-supported by Paho MQTT Python library
- Can run on separate server or cloud (AWS IoT Core, HiveMQ Cloud)

**Alternatives Considered**:
- **RabbitMQ**: More features but higher overhead
- **AWS IoT Core**: Cloud-only, adds external dependency
- **HiveMQ**: Enterprise features not needed for single GrowBox

**Best Practices**:
- Use QoS 1 for sensor data (at-least-once delivery)
- Use QoS 2 for control commands (exactly-once delivery)
- Implement retained messages for last known state
- Use topic structure: `growbox/{box_id}/{category}/{action}`
  - Example: `growbox/001/sensors/temperature`
  - Example: `growbox/001/devices/lights/command`
- Implement Last Will and Testament (LWT) for connection loss detection
- Enable TLS for production (development can use unencrypted)

---

### 3. Sensor Hardware and Libraries

**Decision**:
- **Temperature/Humidity**: DHT22 sensor with Adafruit_DHT library
- **Light Level**: BH1750 I2C light sensor or analog photodiode with ADC
- **Water Level**: Ultrasonic sensor (HC-SR04) or capacitive water level sensor

**Rationale**:
- DHT22: Accurate (±0.5°C, ±2-5% RH), affordable, widely supported
- BH1750: I2C interface, returns lux (convertible to PPFD approximation)
- HC-SR04: Non-contact, reliable for water level measurement

**Best Practices**:
- DHT22: 2-second minimum read interval, add 4.7kΩ pull-up resistor
- BH1750: Use I2C bus 1 on Jetson Nano, address 0x23
- HC-SR04: Trigger/echo timing critical, use threading for non-blocking reads
- Implement sensor health checks (detect failed reads, stale data)
- Calibrate sensors on first run (store calibration in config)

---

### 4. Web Framework for Tablet UI

**Decision**: Flask with Flask-SocketIO for real-time updates

**Rationale**:
- Lightweight (fits 2GB RAM constraint)
- Simple for single-page dashboard application
- Flask-SocketIO enables WebSocket communication for 5-second updates
- Jinja2 templating matches mockup requirements
- Easy to serve static assets (CSS, JS)

**Alternatives Considered**:
- **FastAPI**: Modern async support but overkill for simple UI
- **Django**: Too heavyweight for embedded system
- **Plain HTTP polling**: Less efficient than WebSockets

**Best Practices**:
- Use WebSocket events for real-time sensor updates
- Implement reconnection logic on client side
- Minimize JavaScript framework dependencies (vanilla JS or lightweight lib)
- Serve UI on localhost only (tablet accesses via local network)
- Use CSS Grid for responsive layout matching mockup

---

### 5. SQLite Schema Design for Historical Data

**Decision**: Time-series optimized schema with indexed timestamps

**Schema**:
```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sensor_type TEXT NOT NULL,  -- 'temperature', 'humidity', 'light', 'water'
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    status TEXT DEFAULT 'valid'  -- 'valid', 'error', 'stale'
);
CREATE INDEX idx_timestamp ON sensor_readings(timestamp);
CREATE INDEX idx_sensor_type ON sensor_readings(sensor_type, timestamp);

CREATE TABLE device_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    device_type TEXT NOT NULL,  -- 'lights', 'ventilation', 'pump', 'heater', 'co2'
    state TEXT NOT NULL,  -- 'on', 'off', 'auto'
    command_source TEXT,  -- 'local', 'remote', 'auto'
    triggered_by TEXT  -- User ID or 'automation'
);
CREATE INDEX idx_device_timestamp ON device_states(timestamp);

CREATE TABLE growth_cycles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_date DATE NOT NULL,
    phase TEXT NOT NULL,  -- 'vegetative', 'flowering'
    light_schedule TEXT NOT NULL,  -- '18/6', '12/12'
    target_temp_min REAL,
    target_temp_max REAL,
    target_humidity_min REAL,
    target_humidity_max REAL,
    active BOOLEAN DEFAULT 1
);

CREATE TABLE target_parameters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parameter_name TEXT UNIQUE NOT NULL,
    min_value REAL,
    max_value REAL,
    warning_threshold REAL,
    unit TEXT NOT NULL
);
```

**Rationale**:
- Separate tables for different data types (normalization)
- Indexed timestamps for fast time-range queries
- Growth cycle tracking enables phase-based parameter changes
- Status field for sensor health monitoring

**Best Practices**:
- Use WAL mode for concurrent reads during writes
- Implement periodic vacuum to reclaim space
- Add retention policy (archive/delete old data after season completion)
- Batch inserts for sensor readings (every 5 seconds = 1 transaction)

---

### 6. Auto Mode Control Algorithm

**Decision**: Simple threshold-based control with hysteresis

**Algorithm**:
```
For each sensor reading:
  IF sensor_value < (target_min - hysteresis):
    Activate compensating device (heater, lights, etc.)
  ELSE IF sensor_value > (target_max + hysteresis):
    Activate counteracting device (ventilation, etc.)
  ELSE IF device_is_active AND sensor_value in [target_min, target_max]:
    Deactivate device (target reached)
```

**Hysteresis Values**:
- Temperature: ±0.5°C (prevent rapid cycling)
- Humidity: ±3% RH
- Water level: ±2 liters

**Rationale**:
- Simple, predictable, debuggable
- Prevents device wear from rapid on/off cycling
- No complex PID tuning required for plant growth (slow-changing system)

**Best Practices**:
- Log all auto-mode decisions for troubleshooting
- Manual override disables auto mode for that device until re-enabled
- Implement cooldown periods (e.g., heater: minimum 60s off between cycles)
- Publish auto-mode state changes to MQTT for mobile app visibility

---

### 7. Communication Loss Safety Implementation

**Decision**: Watchdog timer with failsafe GPIO shutdown

**Implementation**:
- MQTT client publishes heartbeat every 10 seconds
- Watchdog thread checks last successful MQTT publish timestamp
- If >30 seconds since last publish: trigger failsafe
- Failsafe action: Set all GPIO device pins to LOW (OFF state)
- Log failsafe event to local storage

**Rationale**:
- Clarification specified all devices turn OFF on communication loss
- 30-second timeout balances responsiveness vs false positives
- GPIO LOW = safe state for all relay-controlled devices

**Best Practices**:
- Use threading.Event for graceful shutdown
- Implement connection retry logic (exponential backoff, max 5 retries)
- Display connection status on tablet UI
- Persist last known good state to SQLite before shutdown

---

### 8. Mendix Mobile App Integration

**Decision**: MQTT-only integration (no direct API)

**Rationale**:
- Specification explicitly states MQTT for communication
- Mendix supports MQTT via connectors/widgets
- Simplifies architecture (no REST API needed)
- Real-time updates inherent to MQTT pub/sub

**Topic Structure for Mendix**:
- **Subscribe** (app receives):
  - `growbox/001/sensors/#` - All sensor data
  - `growbox/001/devices/#` - Device states
  - `growbox/001/status` - System status (online/offline)
- **Publish** (app sends):
  - `growbox/001/devices/{device}/command` - Control commands
  - `growbox/001/config/targets` - Update target parameters

**Message Format** (JSON):
```json
{
  "timestamp": "2025-10-03T19:45:00Z",
  "type": "sensor_reading",
  "sensor": "temperature",
  "value": 23.5,
  "unit": "celsius"
}
```

**Best Practices**:
- Use JSON Schema for message validation
- Implement message versioning (`"schema_version": "1.0"`)
- Mendix app caches last known values for offline display
- Include message ID for deduplication

---

### 9. Growth Phase Light Schedules

**Decision**: Predefined schedules with phase-based switching

**Schedules**:
- **Vegetative**: 18 hours ON, 6 hours OFF (18/6)
- **Flowering**: 12 hours ON, 12 hours OFF (12/12)

**Implementation**:
- Store current phase in `growth_cycles` table
- Cron-like scheduler triggers light on/off based on phase
- User manual phase switch: immediately recalculates schedule
- Respect manual overrides during auto-mode operation

**Rationale**:
- Industry-standard schedules for most plants
- Phase change by user observation (per clarification)
- No need for complex schedule customization in v1

**Best Practices**:
- Use timezone-aware datetime (user's local time)
- Handle DST transitions gracefully
- Log phase changes with timestamp for historical tracking
- Publish schedule changes to MQTT for mobile app sync

---

### 10. UI Design System (Based on Mockup)

**Decision**: Custom design tokens matching mockup

**Design Tokens**:
```css
:root {
  /* Colors */
  --color-primary: #4CAF50;      /* Green accent (status bars, buttons) */
  --color-background: #F5F5F5;    /* Light gray background */
  --color-card: #FFFFFF;          /* White card backgrounds */
  --color-text-primary: #333333;  /* Dark gray text */
  --color-text-secondary: #666666; /* Medium gray labels */
  --color-online: #4CAF50;        /* Green online indicator */

  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-size-large: 48px;        /* Sensor values */
  --font-size-medium: 18px;       /* Labels */
  --font-size-small: 14px;        /* Secondary info */

  /* Spacing */
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 32px;

  /* Card Layout */
  --card-border-radius: 12px;
  --card-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

**Component Structure**:
- Sensor cards (4x grid top)
- System controls (left panel)
- Growth cycle info (right panel)
- Online status indicator (top right)

**Rationale**:
- Mockup provides clear visual reference
- Tablet-optimized (touch-friendly buttons)
- Clean, minimal design aligns with constitution

**Best Practices**:
- Use CSS Grid for responsive layout
- Minimum 44px touch targets (buttons, switches)
- Visual feedback on button press (active states)
- Consistent spacing using design tokens
- Accessibility: ARIA labels, keyboard navigation

---

## Summary

All technical unknowns resolved. Implementation ready to proceed to Phase 1 (Design & Contracts).

**Key Technologies**:
- Python 3.9+ with Jetson.GPIO
- Paho MQTT with Mosquitto broker
- Flask + Flask-SocketIO for tablet UI
- SQLite with time-series optimized schema
- DHT22, BH1750, HC-SR04 sensors

**Architecture Pattern**:
- Event-driven (MQTT pub/sub)
- Domain-driven structure (sensors, devices, mqtt, storage, ui, automation)
- Watchdog-based failsafe for communication loss
- Simple threshold-based automation with hysteresis

**No remaining NEEDS CLARIFICATION** from Technical Context - all decisions documented above.
