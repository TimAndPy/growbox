
# Implementation Plan: GrowBox IoT Control System

**Branch**: `001-i-want-to` | **Date**: 2025-10-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\001-i-want-to\spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Build an IoT-based environmental monitoring and control system for indoor plant cultivation. The system uses NVIDIA Jetson Nano 2GB to interface with sensors (temperature, humidity, light, water level) and control devices (lights, ventilation, pump, heater, CO₂). A local tablet displays a control panel, while remote access is provided via Mendix mobile app through MQTT message broker. System supports manual device control, automated regulation based on target parameters, growth phase tracking (vegetative/flowering), and full-season historical data storage for analysis.

## Technical Context
**Language/Version**: Python 3.9+ (Jetson Nano compatibility)
**Primary Dependencies**: Paho MQTT, GPIO library (Jetson.GPIO), web framework for tablet UI (Flask/FastAPI), sensor libraries (DHT22, etc.)
**Storage**: SQLite for local historical data, file-based configuration
**Testing**: pytest for Python components, integration tests for MQTT messaging, hardware-in-loop tests for GPIO
**Target Platform**: NVIDIA Jetson Nano 2GB (ARM64 Ubuntu 18.04/20.04), tablet browser (Chrome/Firefox), Mendix mobile app
**Project Type**: IoT embedded system + web interface (hybrid: embedded backend + local web UI + mobile client)
**Performance Goals**: 5-second sensor update cycle, <2-second control response time, handle 3 concurrent MQTT clients
**Constraints**: 2GB RAM limit on Jetson Nano, offline-capable (tablet works without internet), real-time GPIO control required, safe-fail on communication loss
**Scale/Scope**: Single GrowBox unit, 4 sensors, 5 controllable devices, ~100,000 sensor readings per growing season (3-6 months)

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Code Minimalism**:
- [x] Feature scope is minimal and necessary (no speculative additions) - implements only specified FR-001 through FR-042
- [x] Solution approach avoids unnecessary abstractions - direct GPIO control, simple MQTT pub/sub, minimal layers
- [x] Plan identifies code/resources to remove during implementation - greenfield project, no cleanup needed

**II. Zero Redundancy**:
- [x] No duplicate implementations planned - single sensor reader, single device controller, shared MQTT client
- [x] Consistent naming and patterns with existing codebase - new project, will establish patterns
- [x] Shared logic extraction identified where applicable - common MQTT handling, sensor reading base class, device control interface

**III. UI Consistency**:
- [x] UI patterns consistent with existing design system (or new system defined) - mockup provided, will establish design tokens
- [x] Visual review checkpoint included in tasks - UI consistency verification required per constitution
- [x] Interaction patterns align with current app behavior - new system, mockup defines canonical interaction

**IV. Quality Over Speed**:
- [x] Design phase completed before implementation tasks - Phase 0 research and Phase 1 design before coding
- [x] Test strategy validates correctness, not just coverage - contract tests for MQTT messages, integration tests for sensor/device flows
- [x] Refactoring tasks identified for existing code issues - N/A for greenfield

**V. Clean Architecture**:
- [x] Folder structure is logical and matches domain - sensors/, devices/, mqtt/, storage/, ui/ by functional domain
- [x] Each component has single, clear responsibility - separate modules for sensors, devices, MQTT, web UI, storage
- [x] No orphaned or unused resources will be created - minimal scope, all code serves defined requirements
- [x] Dependencies are unidirectional - sensors→storage, devices→gpio, mqtt↔services, ui→services

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
growbox/
├── src/
│   ├── sensors/              # Sensor reading modules
│   │   ├── __init__.py
│   │   ├── base.py          # Base sensor interface
│   │   ├── temperature.py   # DHT22 temperature sensor
│   │   ├── humidity.py      # DHT22 humidity sensor
│   │   ├── light.py         # PPFD light sensor
│   │   └── water.py         # Water level sensor
│   ├── devices/             # Device control modules
│   │   ├── __init__.py
│   │   ├── base.py          # Base device controller interface
│   │   ├── lights.py        # Grow lights controller
│   │   ├── ventilation.py   # Ventilation fan controller
│   │   ├── pump.py          # Water pump controller
│   │   ├── heater.py        # Heater controller
│   │   └── co2.py           # CO₂ system controller
│   ├── mqtt/                # MQTT communication
│   │   ├── __init__.py
│   │   ├── client.py        # MQTT client wrapper
│   │   ├── publisher.py     # Sensor data publisher
│   │   └── subscriber.py    # Control command subscriber
│   ├── storage/             # Data persistence
│   │   ├── __init__.py
│   │   ├── database.py      # SQLite database interface
│   │   └── models.py        # Data models (SensorReading, DeviceControl, etc.)
│   ├── automation/          # Auto mode logic
│   │   ├── __init__.py
│   │   └── controller.py    # Automated device control based on targets
│   ├── ui/                  # Web interface for tablet
│   │   ├── __init__.py
│   │   ├── app.py           # Flask/FastAPI application
│   │   ├── static/          # CSS, JS, images
│   │   │   ├── css/
│   │   │   │   └── main.css
│   │   │   └── js/
│   │   │       └── control-panel.js
│   │   └── templates/       # HTML templates
│   │       └── index.html   # Control panel UI
│   └── main.py              # Entry point, orchestrates all components
├── tests/
│   ├── contract/            # MQTT message schema tests
│   │   ├── test_sensor_messages.py
│   │   └── test_control_messages.py
│   ├── integration/         # End-to-end flow tests
│   │   ├── test_sensor_to_mqtt.py
│   │   ├── test_mqtt_to_device.py
│   │   └── test_auto_mode.py
│   └── unit/                # Component unit tests
│       ├── test_sensors.py
│       ├── test_devices.py
│       └── test_storage.py
├── config/
│   ├── mqtt.json            # MQTT broker configuration
│   ├── sensors.json         # Sensor GPIO pin mappings
│   ├── devices.json         # Device GPIO pin mappings
│   └── targets.json         # Target parameter ranges
├── requirements.txt
├── setup.py
└── README.md
```

**Structure Decision**: IoT embedded system structure with clear domain separation. Sensors and devices are GPIO-interfaced modules, MQTT handles remote communication, storage persists data locally, UI serves the tablet interface, and automation implements auto-mode logic. Configuration files separate hardware pinouts from code. Tests follow TDD approach with contracts, integration, and unit layers.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) - research.md created
- [x] Phase 1: Design complete (/plan command) - data-model.md, contracts/, quickstart.md created
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [x] Phase 3: Tasks generated (/tasks command) - tasks.md created with 60 ordered tasks
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS - all principles satisfied
- [x] Post-Design Constitution Check: PASS - no violations introduced
- [x] All NEEDS CLARIFICATION resolved - research.md documents all decisions
- [x] Complexity deviations documented - N/A, no violations

**Artifacts Generated**:
- ✅ research.md - Technical research and best practices
- ✅ data-model.md - 5 entities with validation rules and relationships
- ✅ contracts/mqtt-sensor-data.json - Sensor reading MQTT contract
- ✅ contracts/mqtt-device-command.json - Device command MQTT contract
- ✅ contracts/mqtt-device-state.json - Device state MQTT contract
- ✅ contracts/mqtt-system-status.json - System status MQTT contract
- ✅ quickstart.md - Manual testing procedures for all FR requirements
- ✅ tasks.md - 60 implementation tasks with dependencies and parallel execution guidance

---
*Based on Constitution v1.0.0 - See `.specify/memory/constitution.md`*
