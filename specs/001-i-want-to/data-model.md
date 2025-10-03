# Data Model: GrowBox IoT Control System

**Date**: 2025-10-03
**Phase**: 1 - Design & Contracts
**Purpose**: Define entities, fields, relationships, and validation rules

---

## Entity Overview

This system manages five primary entities:
1. **SensorReading** - Environmental measurements over time
2. **DeviceControl** - Device state changes and control commands
3. **GrowthCycle** - Plant growth phase tracking
4. **TargetParameters** - Environmental target ranges
5. **SystemStatus** - Overall system health and connectivity

---

## Entity Definitions

### 1. SensorReading

**Purpose**: Represents a single timestamped environmental measurement

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| timestamp | DATETIME | NOT NULL, INDEXED | When the reading was taken (UTC) |
| sensor_type | TEXT | NOT NULL, ENUM('temperature', 'humidity', 'light', 'water') | Sensor category |
| value | REAL | NOT NULL | Measured value (numeric) |
| unit | TEXT | NOT NULL | Unit of measurement (celsius, percent, ppfd, liters) |
| status | TEXT | DEFAULT 'valid', ENUM('valid', 'error', 'stale') | Reading validity |

**Validation Rules**:
- `timestamp` must be <= current time (no future readings)
- `value` must be within physical sensor ranges:
  - temperature: -40 to 80 (°C for DHT22)
  - humidity: 0 to 100 (% RH)
  - light: 0 to 200000 (μmol for PPFD)
  - water: 0 to 100 (liters, configurable max)
- `status = 'error'` when sensor read fails
- `status = 'stale'` when reading is >30 seconds old

**Relationships**:
- None (time-series data, no foreign keys for performance)

**Indexes**:
- `(timestamp)` - for time-range queries
- `(sensor_type, timestamp)` - for per-sensor historical queries

**State Transitions**:
- N/A (immutable once recorded)

**Example**:
```json
{
  "id": 12345,
  "timestamp": "2025-10-03T19:45:23Z",
  "sensor_type": "temperature",
  "value": 23.5,
  "unit": "celsius",
  "status": "valid"
}
```

---

### 2. DeviceControl

**Purpose**: Represents a device state change event

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| timestamp | DATETIME | NOT NULL, INDEXED | When the state changed (UTC) |
| device_type | TEXT | NOT NULL, ENUM('lights', 'ventilation', 'pump', 'heater', 'co2') | Device category |
| state | TEXT | NOT NULL, ENUM('on', 'off', 'auto') | New device state |
| command_source | TEXT | ENUM('local', 'remote', 'auto', 'failsafe') | Where command originated |
| triggered_by | TEXT | NULL | User ID or 'automation' or 'watchdog' |

**Validation Rules**:
- `timestamp` must be <= current time
- `state = 'auto'` only valid when auto mode enabled
- `command_source = 'failsafe'` implies `state = 'off'`
- Cannot transition to same state (must be a change)

**Relationships**:
- None (event log, no foreign keys)

**Indexes**:
- `(timestamp)` - for recent activity queries
- `(device_type, timestamp)` - for per-device history

**State Transitions**:
```
[off] --command--> [on]
[on]  --command--> [off]
[on]  --enable_auto--> [auto]
[off] --enable_auto--> [auto]
[auto] --manual_command--> [on|off]
[any] --failsafe--> [off]
```

**Example**:
```json
{
  "id": 456,
  "timestamp": "2025-10-03T19:45:30Z",
  "device_type": "lights",
  "state": "on",
  "command_source": "remote",
  "triggered_by": "user_mendix_app"
}
```

---

### 3. GrowthCycle

**Purpose**: Represents a plant growth phase configuration

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| start_date | DATE | NOT NULL | When this phase began |
| phase | TEXT | NOT NULL, ENUM('vegetative', 'flowering') | Growth phase name |
| light_schedule | TEXT | NOT NULL | Light on/off schedule (e.g., '18/6', '12/12') |
| target_temp_min | REAL | NULL | Minimum target temperature (°C) for this phase |
| target_temp_max | REAL | NULL | Maximum target temperature (°C) |
| target_humidity_min | REAL | NULL | Minimum target humidity (% RH) |
| target_humidity_max | REAL | NULL | Maximum target humidity (% RH) |
| active | BOOLEAN | DEFAULT 1, UNIQUE WHERE active=1 | Only one active cycle at a time |

**Validation Rules**:
- Only ONE `active = 1` record allowed (enforced by unique constraint)
- `start_date` cannot be in the future
- `phase` determines default `light_schedule`:
  - vegetative → '18/6'
  - flowering → '12/12'
- `target_temp_min` < `target_temp_max`
- `target_humidity_min` < `target_humidity_max`

**Relationships**:
- Influences `TargetParameters` (phase-specific targets)
- Affects automation logic (light schedule)

**Indexes**:
- `(active)` - quick lookup of current phase

**State Transitions**:
```
[vegetative, active=1] --user_switches_phase--> [vegetative, active=0] + [flowering, active=1]
```

**Example**:
```json
{
  "id": 3,
  "start_date": "2025-10-01",
  "phase": "flowering",
  "light_schedule": "12/12",
  "target_temp_min": 22.0,
  "target_temp_max": 25.0,
  "target_humidity_min": 60.0,
  "target_humidity_max": 70.0,
  "active": true
}
```

---

### 4. TargetParameters

**Purpose**: Stores user-configurable target ranges for environmental controls

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| parameter_name | TEXT | UNIQUE, NOT NULL | Parameter identifier (e.g., 'temperature', 'humidity') |
| min_value | REAL | NULL | Minimum acceptable value |
| max_value | REAL | NULL | Maximum acceptable value |
| warning_threshold | REAL | NULL | Distance from min/max before warning (loose boundaries) |
| unit | TEXT | NOT NULL | Unit of measurement |

**Validation Rules**:
- `min_value` < `max_value` (when both non-null)
- `warning_threshold` >= 0
- `parameter_name` must match sensor types
- Effective warning range: `[min - threshold, max + threshold]`

**Relationships**:
- Used by `automation.controller` for auto-mode decisions
- Can be overridden per `GrowthCycle`

**Indexes**:
- `(parameter_name)` - unique lookup

**State Transitions**:
- User adjustments update existing records (no history tracking in v1)

**Example**:
```json
{
  "id": 1,
  "parameter_name": "temperature",
  "min_value": 22.0,
  "max_value": 25.0,
  "warning_threshold": 2.0,
  "unit": "celsius"
}
```
*This means warnings shown if temp < 20°C or > 27°C, but auto-control targets 22-25°C*

---

### 5. SystemStatus

**Purpose**: Tracks overall system health and connectivity (in-memory, optionally persisted)

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, SINGLETON | Always id=1 (single row) |
| connection_state | TEXT | ENUM('online', 'offline') | MQTT broker connectivity |
| last_mqtt_publish | DATETIME | NULL | Last successful MQTT message sent |
| last_mqtt_receive | DATETIME | NULL | Last successful MQTT message received |
| auto_mode_enabled | BOOLEAN | DEFAULT 0 | Whether automation is active |
| active_alerts | TEXT | NULL | JSON array of current alerts/warnings |
| uptime_seconds | INTEGER | DEFAULT 0 | System uptime since boot |

**Validation Rules**:
- Only ONE row exists (singleton pattern)
- `connection_state = 'offline'` when `(current_time - last_mqtt_publish) > 30 seconds`
- `active_alerts` is JSON-formatted string

**Relationships**:
- Referenced by UI for status display
- Monitored by watchdog for failsafe trigger

**Indexes**:
- None (single row)

**State Transitions**:
```
[offline] --mqtt_connect--> [online]
[online] --mqtt_disconnect OR timeout--> [offline]
[auto_mode_enabled=0] --user_enables--> [auto_mode_enabled=1]
[auto_mode_enabled=1] --user_disables OR failsafe--> [auto_mode_enabled=0]
```

**Example**:
```json
{
  "id": 1,
  "connection_state": "online",
  "last_mqtt_publish": "2025-10-03T19:45:33Z",
  "last_mqtt_receive": "2025-10-03T19:45:32Z",
  "auto_mode_enabled": true,
  "active_alerts": "[\"water_level_low\"]",
  "uptime_seconds": 86400
}
```

---

## Derived / Calculated Fields

These are NOT stored in database but calculated on demand:

### Days in Current Phase
- **Source**: `GrowthCycle.start_date` (where `active = 1`)
- **Calculation**: `days_between(current_date, start_date)`
- **Used in**: UI display ("Flowering - Day 28")

### Days Until Harvest
- **Source**: User-estimated harvest date (NOT REQUIRED per clarification FR-019)
- **Status**: DEFERRED - observational approach, no harvest date input in v1

### Current Sensor Values
- **Source**: Latest `SensorReading` per `sensor_type`
- **Calculation**: `SELECT * FROM sensor_readings WHERE sensor_type = ? ORDER BY timestamp DESC LIMIT 1`

### Current Device States
- **Source**: Latest `DeviceControl` per `device_type`
- **Calculation**: `SELECT * FROM device_states WHERE device_type = ? ORDER BY timestamp DESC LIMIT 1`

---

## Data Retention Policy

Per clarification: "Long-term archive - keep full growing season history for analysis"

**Retention Rules**:
- **SensorReading**: Retain until user manually archives/deletes season
- **DeviceControl**: Retain until user manually archives/deletes season
- **GrowthCycle**: Archive (set `active = 0`) when new phase starts; retain indefinitely
- **TargetParameters**: No automatic deletion (configuration data)
- **SystemStatus**: Ephemeral (reset on reboot), optionally persist for uptime tracking

**Archive Trigger**: User marks season complete in UI (future feature)

---

## Schema Migration Strategy

**Version 1.0** (this spec):
- Initial schema as defined above
- SQLite with WAL mode
- No migrations needed for greenfield

**Future Considerations**:
- Add `schema_version` table for migration tracking
- Use Alembic or custom migration scripts
- Backward-compatible changes only (add columns, not remove)

---

## Summary

Five core entities model the complete GrowBox system:
- **SensorReading** & **DeviceControl**: Time-series event logs
- **GrowthCycle**: Phase tracking with light schedule automation
- **TargetParameters**: User-adjustable environmental targets
- **SystemStatus**: Real-time system health singleton

All validation rules align with functional requirements (FR-001 through FR-042). Relationships are minimal (event-driven architecture). Indexes optimize time-range queries for historical data access.

Schema ready for contract generation (Phase 1, step 2).
