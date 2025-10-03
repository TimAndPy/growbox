# Tasks: GrowBox IoT Control System

**Input**: Design documents from `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\001-i-want-to\`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- Repository root: `C:\Users\Timve\Desktop\github_spec_growbox\growbox\`
- Source code: `src/`
- Tests: `tests/`
- Config: `config/`
- Specs: `specs/001-i-want-to/`

---

## Phase 3.1: Setup & Infrastructure

- [x] **T001** Create project structure with directories: `src/sensors/`, `src/devices/`, `src/mqtt/`, `src/storage/`, `src/automation/`, `src/ui/`, `tests/contract/`, `tests/integration/`, `tests/unit/`, `config/`

- [x] **T002** Initialize Python project with `setup.py` and `requirements.txt` including dependencies: `paho-mqtt`, `Jetson.GPIO`, `Flask`, `Flask-SocketIO`, `Adafruit-DHT`, `smbus2` (for BH1750), `pytest`, `jsonschema`

- [x] **T003** [P] Create configuration files in `config/`:
  - `mqtt.json` (broker URL, port, QoS settings)
  - `sensors.json` (GPIO pin mappings for DHT22, HC-SR04)
  - `devices.json` (GPIO pin mappings for 5 relay channels)
  - `targets.json` (default target parameter ranges)

- [x] **T004** [P] Configure pytest in `pytest.ini` with test paths, markers for contract/integration/unit tests, and coverage settings

- [x] **T005** [P] Create SQLite database initialization script in `src/storage/init_db.py` with schema from data-model.md (5 tables: sensor_readings, device_states, growth_cycles, target_parameters, system_status)

---

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### Contract Tests (MQTT Message Schemas)

- [x] **T006** [P] Contract test for sensor data messages in `tests/contract/test_mqtt_sensor_data.py` - validate against `specs/001-i-want-to/contracts/mqtt-sensor-data.json` schema for all 4 sensor types (temperature, humidity, light, water)

- [x] **T007** [P] Contract test for device command messages in `tests/contract/test_mqtt_device_command.py` - validate against `specs/001-i-want-to/contracts/mqtt-device-command.json` schema for all 5 devices

- [x] **T008** [P] Contract test for device state messages in `tests/contract/test_mqtt_device_state.py` - validate against `specs/001-i-want-to/contracts/mqtt-device-state.json` schema

- [x] **T009** [P] Contract test for system status messages in `tests/contract/test_mqtt_system_status.py` - validate against `specs/001-i-want-to/contracts/mqtt-system-status.json` schema

### Integration Tests (User Scenarios)

- [x] **T010** [P] Integration test for sensor-to-MQTT flow in `tests/integration/test_sensor_to_mqtt.py` - verify sensors publish data every 5 seconds to MQTT topics `growbox/001/sensors/{sensor}`

- [x] **T011** [P] Integration test for MQTT-to-device control flow in `tests/integration/test_mqtt_to_device.py` - verify device commands received via MQTT activate GPIO pins within 2 seconds

- [x] **T012** [P] Integration test for auto mode in `tests/integration/test_auto_mode.py` - verify automation controller activates devices based on sensor readings and target parameters with hysteresis

- [x] **T013** [P] Integration test for communication loss failsafe in `tests/integration/test_failsafe.py` - verify watchdog turns OFF all devices when MQTT connection lost for >30 seconds

- [x] **T014** [P] Integration test for growth phase switching in `tests/integration/test_growth_phase.py` - verify phase change updates light schedule (18/6 → 12/12) and resets day counter

- [x] **T015** [P] Integration test for historical data storage in `tests/integration/test_data_retention.py` - verify sensor readings and device states persisted to SQLite with correct timestamps and indexing

---

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Data Models & Storage

- [x] **T016** [P] Create `SensorReading` model in `src/storage/models.py` with fields: id, timestamp, sensor_type, value, unit, status (per data-model.md)

- [x] **T017** [P] Create `DeviceControl` model in `src/storage/models.py` with fields: id, timestamp, device_type, state, command_source, triggered_by

- [x] **T018** [P] Create `GrowthCycle` model in `src/storage/models.py` with fields: id, start_date, phase, light_schedule, target ranges, active flag

- [x] **T019** [P] Create `TargetParameters` model in `src/storage/models.py` with fields: id, parameter_name, min/max values, warning_threshold, unit

- [x] **T020** [P] Create `SystemStatus` model in `src/storage/models.py` as singleton with fields: connection_state, last_mqtt_publish/receive, auto_mode_enabled, active_alerts, uptime

- [x] **T021** Create database interface in `src/storage/database.py` with methods: `insert_sensor_reading()`, `insert_device_state()`, `get_latest_sensor_value()`, `get_current_growth_cycle()`, `update_system_status()` (uses SQLite with WAL mode)

### Sensor Modules

- [x] **T022** [P] Create base sensor interface in `src/sensors/base.py` with abstract methods: `read()`, `get_status()`, `calibrate()`

- [x] **T023** [P] Implement DHT22 temperature sensor in `src/sensors/temperature.py` using Adafruit_DHT library, GPIO pin from config, 2-second minimum read interval

- [x] **T024** [P] Implement DHT22 humidity sensor in `src/sensors/humidity.py` using Adafruit_DHT library, GPIO pin from config

- [x] **T025** [P] Implement BH1750 light sensor in `src/sensors/light.py` using smbus2 I2C interface, I2C address 0x23, convert lux to PPFD approximation

- [x] **T026** [P] Implement HC-SR04 ultrasonic water level sensor in `src/sensors/water.py` using GPIO trigger/echo pins from config, non-blocking threading

### Device Control Modules

- [x] **T027** [P] Create base device controller interface in `src/devices/base.py` with abstract methods: `turn_on()`, `turn_off()`, `get_state()`, `cleanup()`

- [x] **T028** [P] Implement grow lights controller in `src/devices/lights.py` using Jetson.GPIO, relay GPIO pin from config

- [x] **T029** [P] Implement ventilation controller in `src/devices/ventilation.py` using Jetson.GPIO, relay GPIO pin from config

- [x] **T030** [P] Implement water pump controller in `src/devices/pump.py` using Jetson.GPIO, relay GPIO pin from config

- [x] **T031** [P] Implement heater controller in `src/devices/heater.py` using Jetson.GPIO, relay GPIO pin from config

- [x] **T032** [P] Implement CO₂ system controller in `src/devices/co2.py` using Jetson.GPIO, relay GPIO pin from config

### MQTT Communication Layer

- [x] **T033** Create MQTT client wrapper in `src/mqtt/client.py` with connection handling, QoS configuration, Last Will and Testament (LWT) for connection loss detection, reconnection logic with exponential backoff

- [x] **T034** Create sensor data publisher in `src/mqtt/publisher.py` that reads all 4 sensors every 5 seconds, formats as JSON per contract schema, publishes to topics `growbox/001/sensors/{sensor}` with QoS 1 and retained flag

- [x] **T035** Create control command subscriber in `src/mqtt/subscriber.py` that subscribes to `growbox/001/devices/+/command` with QoS 2, validates against contract schema, triggers device controller methods

- [x] **T036** Add system status publisher to `src/mqtt/publisher.py` that publishes heartbeat and status to `growbox/001/status` every 10 seconds with current phase, auto-mode state, alerts

### Automation & Safety

- [x] **T037** Create automation controller in `src/automation/controller.py` implementing threshold-based control with hysteresis for temperature (±0.5°C), humidity (±3% RH), water level (±2L) based on target parameters from database

- [x] **T038** Add watchdog thread to `src/automation/watchdog.py` that monitors last MQTT publish timestamp, triggers failsafe (all devices OFF) if >30 seconds elapsed, logs failsafe event

- [x] **T039** Implement growth phase scheduler in `src/automation/scheduler.py` that calculates light on/off times based on current phase (18/6 for vegetative, 12/12 for flowering), respects manual overrides

### Web UI for Tablet

- [x] **T040** Create Flask application in `src/ui/app.py` with Flask-SocketIO for WebSocket support, serves static files and templates

- [x] **T041** [P] Create HTML template in `src/ui/templates/index.html` matching mockup layout: 4-column sensor card grid (top), system controls panel (left), growth cycle panel (right), online indicator (top-right)

- [x] **T042** [P] Create CSS design system in `src/ui/static/css/style.css` with design tokens from mockup: colors (primary green #4CAF50, backgrounds, text), typography (48px sensor values, 18px labels), spacing (8/16/24/32px), card styling (12px radius, shadows)

- [x] **T043** [P] Create JavaScript control panel logic in `src/ui/static/js/main.js` with WebSocket connection for real-time sensor updates (every 5 seconds), device toggle event handlers, phase switch button, target parameter editing

- [x] **T044** Add WebSocket event handlers to `src/ui/app.py`: `emit('sensor_update')` every 5 seconds with current values, `on('device_command')` to handle toggle switches, `on('phase_switch')` to update growth cycle

### Main Application Orchestration

- [x] **T045** Create main entry point in `src/main.py` that initializes database, starts sensor reading threads, starts MQTT client with publisher/subscriber, starts automation controller with watchdog, starts Flask web server, handles graceful shutdown with GPIO cleanup

---

## Phase 3.4: Integration & Configuration

- [x] **T046** Connect automation controller to database in `src/automation/controller.py` - load target parameters on startup, update growth cycle active status, log automation decisions

- [x] **T047** Add MQTT device state publishing to all device controllers in `src/devices/*.py` - publish state change to `growbox/001/devices/{device}/state` with command_source and timestamp

- [x] **T048** Implement data persistence in sensor/device modules - insert readings to database via `src/storage/database.py` methods after each sensor read and device state change

- [x] **T049** Add error handling and logging throughout - sensor read failures set status='error', MQTT connection failures trigger retry, device GPIO errors logged to file and database

- [x] **T050** Configure CORS and security headers in Flask app if needed (tablet on local network, may not need strict CORS)

---

## Phase 3.5: Polish & Constitutional Compliance

- [x] **T051** [P] Unit tests for sensor modules in `tests/unit/test_sensors.py` - mock GPIO, verify read intervals, calibration, error handling

- [x] **T052** [P] Unit tests for device modules in `tests/unit/test_devices.py` - mock GPIO, verify state transitions, cleanup on shutdown

- [x] **T053** [P] Unit tests for database operations in `tests/unit/test_storage.py` - verify CRUD operations, indexes, singleton pattern for SystemStatus

- [x] **T054** [P] Unit tests for automation logic in `tests/unit/test_automation.py` - verify hysteresis calculations, threshold comparisons, cooldown periods

- [ ] **T055** Performance validation - run system for 1 hour, verify 5-second sensor update cycle maintained, <2-second device response time, no memory leaks (within 2GB RAM limit)

- [x] **T056** [P] Update `README.md` with installation instructions for Jetson Nano, hardware wiring diagram (GPIO pins), MQTT broker setup, first-time configuration

- [x] **T057** Remove duplicate code and unused imports - scan all `src/` files, extract common MQTT handling to shared module if duplicated, remove commented-out code blocks

- [x] **T058** UI consistency review - compare tablet UI at `http://localhost:5000` with `Mockup_ControlPanelUI.png`, verify design system tokens applied (colors, spacing, typography), test touch targets (≥44px), capture screenshots for documentation

- [x] **T059** Clean up folder structure - remove any empty `__pycache__` directories, verify all files have purpose (no orphaned test files), ensure config files have examples with .example suffix

- [ ] **T060** Run manual testing from `specs/001-i-want-to/quickstart.md` - execute all 10 test suites, document results, fix any failures before sign-off

---

## Dependencies

**Critical Path**:
1. Setup (T001-T005) must complete before all others
2. Tests (T006-T015) must be written and failing before implementation (T016-T045)
3. Models (T016-T021) must complete before storage integration (T046, T048)
4. Sensor modules (T022-T026) must complete before MQTT publisher (T034)
5. Device modules (T027-T032) must complete before MQTT subscriber (T035) and automation (T037)
6. MQTT layer (T033-T036) must complete before main orchestration (T045)
7. All core implementation (T016-T045) must complete before integration (T046-T050)
8. All integration (T046-T050) must complete before polish (T051-T060)

**Parallel Opportunities**:
- T003-T005: Config files, pytest setup, DB init (all independent)
- T006-T009: Contract tests (all test different schemas)
- T010-T015: Integration tests (all test different flows)
- T016-T020: Data models (all independent classes)
- T022-T026: Sensor modules (all independent, different files)
- T027-T032: Device modules (all independent, different files)
- T041-T043: UI static files (HTML, CSS, JS in different files)
- T051-T054: Unit tests (all test different modules)

---

## Parallel Execution Examples

### Example 1: Contract Tests (T006-T009)
```bash
# Launch all 4 contract tests in parallel
pytest tests/contract/test_mqtt_sensor_data.py &
pytest tests/contract/test_mqtt_device_command.py &
pytest tests/contract/test_mqtt_device_state.py &
pytest tests/contract/test_mqtt_system_status.py &
wait
```

### Example 2: Sensor Modules (T023-T026)
Create all sensor implementations simultaneously:
- T023: `src/sensors/temperature.py`
- T024: `src/sensors/humidity.py`
- T025: `src/sensors/light.py`
- T026: `src/sensors/water.py`

### Example 3: Device Modules (T028-T032)
Create all device controllers simultaneously:
- T028: `src/devices/lights.py`
- T029: `src/devices/ventilation.py`
- T030: `src/devices/pump.py`
- T031: `src/devices/heater.py`
- T032: `src/devices/co2.py`

### Example 4: UI Static Assets (T041-T043)
```
Parallel creation:
- T041: src/ui/templates/index.html
- T042: src/ui/static/css/main.css
- T043: src/ui/static/js/control-panel.js
```

---

## Notes

- **[P] tasks** = different files, no dependencies, can execute in parallel
- **Verify tests fail** before implementing (TDD enforcement)
- **Commit after each task** for granular history
- **Hardware setup required**: Jetson Nano with sensors and relays connected per GPIO pin mappings in config files
- **MQTT broker required**: Mosquitto or compatible broker accessible on network
- **Constitutional compliance**: Tasks T057-T059 enforce Code Minimalism, Zero Redundancy, Clean Architecture principles

---

## Task Generation Rules Applied

1. **From Contracts** (4 files):
   - Each contract file → contract test task [P] (T006-T009)
   - Each message type → validation and schema enforcement

2. **From Data Model** (5 entities):
   - Each entity → model creation task [P] (T016-T020)
   - Database interface task (T021)

3. **From User Stories** (quickstart.md 10 test suites):
   - Each critical flow → integration test [P] (T010-T015)
   - Manual validation task (T060)

4. **From Project Structure** (plan.md):
   - Sensors (4) → base + 4 implementations [P] (T022-T026)
   - Devices (5) → base + 5 implementations [P] (T027-T032)
   - MQTT layer → client + publisher + subscriber (T033-T036)
   - UI components → Flask app + HTML + CSS + JS [P] (T040-T044)

5. **Ordering**:
   - Setup (T001-T005) → Tests (T006-T015) → Models (T016-T021) → Sensors (T022-T026) + Devices (T027-T032) → MQTT (T033-T036) + Automation (T037-T039) + UI (T040-T044) → Main (T045) → Integration (T046-T050) → Polish (T051-T060)

---

## Validation Checklist

- [x] All 4 contracts have corresponding tests (T006-T009)
- [x] All 5 entities have model tasks (T016-T020)
- [x] All tests come before implementation (T006-T015 before T016+)
- [x] Parallel tasks truly independent (same file = sequential, different files = [P])
- [x] Each task specifies exact file path or module
- [x] No task modifies same file as another [P] task
- [x] Constitutional compliance tasks included (T057: duplication removal, T058: UI consistency, T059: cleanup)
- [x] Quality gates addressed in polish phase (T051-T060)

---

**Total Tasks**: 60 numbered, ordered, dependency-tracked tasks
**Estimated Parallel Groups**: 8 groups (config, contract tests, integration tests, models, sensors, devices, UI assets, unit tests)
**Critical TDD Gate**: T006-T015 MUST fail before T016-T045 begin

Ready for implementation execution following constitutional principles.
