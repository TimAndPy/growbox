# Feature Specification: UI Refinements for Tablet Display

**Feature Branch**: `003-we-made-great`
**Created**: 2025-10-03
**Status**: Draft
**Input**: User description: "We made great improvements to the UI. This is the current state of the UI ( @CurrentUI.png ). I want the "GrowBox Control Panel" to be centered in the header. Also I want the UI to fit my tablet screen (1024x600 px). Remove the "days until harvest". Remove the "light schedule" input box. Make light schema selection (vegatitive / Flowering) a toggle instead of two buttons."

## Execution Flow (main)
```
1. Parse user description from Input ✓
   → Feature: UI refinements for better tablet display (1024x600)
2. Extract key concepts from description ✓
   → Center header title
   → Optimize for 1024x600 screen size
   → Remove "days until harvest" field
   → Remove "light schedule" input box
   → Replace phase buttons with toggle switch
3. Compare current UI (@CurrentUI.png) vs requested changes
   → Current: Left-aligned title, two phase buttons, harvest countdown, light schedule box
   → Desired: Centered title, single toggle, removed fields, optimized layout
4. Fill User Scenarios & Testing section ✓
5. Generate Functional Requirements ✓
6. Run Review Checklist ✓
7. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users see and interact with
- ❌ Avoid HOW to implement CSS/HTML structure
- 👥 Written for UI/UX perspective

---

## User Scenarios & Testing

### Primary User Story
As a grower using a tablet with 1024x600 screen resolution, I want a cleaner, more focused control panel interface with centered header, simplified growth cycle controls, and optimized layout so that all key information fits on screen without scrolling and controls are easier to use.

### Acceptance Scenarios

1. **Given** I open the tablet UI at 1024x600 resolution, **When** I view the header, **Then** I see "GrowBox Control Panel" title centered in the header

2. **Given** I view the Growth Cycle panel, **When** I look at the controls, **Then** I see:
   - A single toggle switch for Vegetative/Flowering phase selection
   - NO "Days Until Harvest" field
   - NO "Light Schedule" input box
   - Current phase displayed (e.g., "Flowering - Day 28")

3. **Given** I want to switch growth phases, **When** I use the phase toggle, **Then** the toggle switches between Vegetative (18/6) and Flowering (12/12) modes with a single click/tap

4. **Given** the UI is displayed at 1024x600 resolution, **When** I view the entire interface, **Then**:
   - All content fits on screen without horizontal scrolling
   - Vertical scrolling is minimal or eliminated
   - All controls remain accessible and properly sized

5. **Given** I interact with the phase toggle, **When** I tap it, **Then** it provides clear visual feedback showing which mode is active (Vegetative or Flowering)

### Edge Cases
- What happens when screen is rotated (600x1024)? [Current UI should adapt using existing responsive breakpoints]
- How does the toggle indicate current phase at first load? [Toggle position reflects current active phase from backend data]
- What if phase data is unavailable? [Display "Unknown" phase with toggle defaulting to Vegetative]

## Requirements

### Functional Requirements

**Header Layout**
- **FR-001**: System MUST display "GrowBox Control Panel" title centered in the header
- **FR-002**: Header MUST maintain Squad Apps logo on the left side
- **FR-003**: Header MUST display connection status indicator on the right side

**Screen Size Optimization**
- **FR-004**: Interface MUST be optimized for 1024x600 pixel tablet screen resolution
- **FR-005**: All sensor cards MUST remain visible without horizontal scrolling at 1024x600
- **FR-006**: System Controls and Growth Cycle panels MUST fit within viewport at 1024x600
- **FR-007**: Primary interface elements MUST be accessible without scrolling at 1024x600

**Growth Cycle Panel Simplification**
- **FR-008**: System MUST remove "Days Until Harvest" field from Growth Cycle panel
- **FR-009**: System MUST remove "Light Schedule" input box from Growth Cycle panel
- **FR-010**: Growth Cycle panel MUST display current phase and day count (e.g., "Flowering - Day 28")

**Phase Selection Toggle**
- **FR-011**: System MUST replace Vegetative/Flowering buttons with a single toggle switch
- **FR-012**: Toggle switch MUST show clear labels for Vegetative (18/6) and Flowering (12/12) options
- **FR-013**: Toggle switch MUST visually indicate active phase (e.g., toggle position left for Vegetative, right for Flowering)
- **FR-014**: Toggle switch MUST allow switching between Vegetative and Flowering phases with single click/tap
- **FR-015**: Toggle switch MUST maintain ≥44px touch target for tablet usability

**Visual Consistency**
- **FR-016**: Phase toggle MUST follow same iOS-style design as existing device toggle switches
- **FR-017**: Growth Cycle panel MUST maintain light green background (#F6FFED) and border (#B7EB8F)
- **FR-018**: All existing sensor cards, progress bars, and device controls MUST remain unchanged

### Key UI Components

- **Header**: Squad Apps logo (left), "GrowBox Control Panel" title (center), connection status (right)
- **Sensor Cards**: 4-column grid unchanged (Temperature, Humidity, Light Level, Water Level with progress bars)
- **System Controls Panel**: Device toggle list unchanged
- **Growth Cycle Panel**:
  - Phase highlight: "Flowering - Day 28" (current phase display)
  - Phase toggle: Single switch for Vegetative ↔ Flowering selection
  - REMOVED: "Days Until Harvest" box
  - REMOVED: "Light Schedule" input box
- **Layout**: Optimized for 1024x600 viewport (2-column panels may stack if needed)

---

## Review & Acceptance Checklist

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and visual requirements
- [x] Written for UI/UX stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable (visual comparison, screen size validation)
- [x] Scope is clearly bounded (UI refinements only, no backend changes)
- [x] Dependencies: Uses existing toggle switch design pattern, maintains current data flow

---

## Execution Status

- [x] User description parsed
- [x] Key concepts extracted (centered title, 1024x600 optimization, remove fields, phase toggle)
- [x] Ambiguities marked (none - requirements are clear)
- [x] User scenarios defined
- [x] Requirements generated (18 functional requirements)
- [x] UI components identified
- [x] Review checklist passed

---

## Visual Comparison Summary

### Current UI → Desired UI Changes

| Element | Current | Desired |
|---------|---------|---------|
| Header Title | Left-aligned (with logo) | Centered |
| Growth Phase Selection | Two buttons (Vegetative/Flowering) | Single toggle switch |
| Days Until Harvest | Displayed in info box | REMOVED |
| Light Schedule | Displayed in info box | REMOVED |
| Viewport Optimization | General responsiveness | Specifically optimized for 1024x600 |
| Growth Cycle Panel | 4 elements (highlight + 2 boxes + 2 buttons) | 2 elements (highlight + toggle) |

This refinement focuses on simplifying the Growth Cycle interface, improving header balance, and ensuring optimal display on the specific 1024x600 tablet screen size.
