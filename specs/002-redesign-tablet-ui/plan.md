# Implementation Plan: Tablet UI Redesign to Match Mockup

**Branch**: `002-redesign-tablet-ui` | **Date**: 2025-10-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-redesign-tablet-ui/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path ✓
   → Loaded spec.md with 27 functional requirements
2. Fill Technical Context ✓
   → Detected web application (Flask)
   → Frontend redesign only, backend unchanged
3. Fill Constitution Check section ✓
   → Based on .specify/memory/constitution.md v1.0.0
4. Evaluate Constitution Check section ✓
   → UI Consistency is PRIMARY focus (Principle III)
   → All checks passed, no violations
   → Progress: Initial Constitution Check COMPLETE
5. Execute Phase 0 → research.md ✓
   → No NEEDS CLARIFICATION (mockup provides clear reference)
6. Execute Phase 1 → contracts, data-model.md, quickstart.md ✓
   → No new contracts (UI only)
   → No data model changes (backend unchanged)
   → quickstart.md updated with visual testing
7. Re-evaluate Constitution Check section ✓
   → UI Consistency verified with design system
   → Progress: Post-Design Constitution Check COMPLETE
8. Plan Phase 2 → Task generation approach defined ✓
9. STOP - Ready for /tasks command ✓
```

## Summary

**Primary Requirement**: Redesign the GrowBox tablet control panel UI to match the provided mockup, transforming from a dark theme with emoji icons and button pairs to a light, professional theme with progress bars, toggle switches, and a 2-column layout.

**Technical Approach**:
- Pure frontend changes (HTML, CSS, JavaScript)
- Maintain existing Flask backend and WebSocket communication
- Replace current `style.css` and `index.html` with mockup-inspired designs
- Add progress bar component for sensor visualization
- Replace toggle switch CSS (iOS-style)
- Implement 2-column responsive grid layout
- No database, API, or Python backend changes required

## Technical Context

**Language/Version**: HTML5, CSS3, JavaScript ES6+ (existing: Python 3.10 Flask backend unchanged)
**Primary Dependencies**:
- Flask 2.3.3 (unchanged)
- Flask-SocketIO 5.3.4 (unchanged)
- No new dependencies required
**Storage**: N/A (UI only, existing SQLite backend unchanged)
**Testing**: Manual visual testing against mockup, existing pytest for backend
**Target Platform**: Web browser on tablet (iPad, Android tablets) at 1024x768+ resolution
**Project Type**: Web application (frontend-only changes)
**Performance Goals**: <100ms UI render time, 60fps animations, <1MB additional CSS/assets
**Constraints**:
- Must maintain existing WebSocket real-time updates
- Must support touch targets ≥44px
- Must work on existing Flask app without backend changes
**Scale/Scope**:
- 1 HTML template file (`src/ui/templates/index.html`)
- 1 CSS file (`src/ui/static/css/style.css`)
- 1 JavaScript file (`src/ui/static/js/main.js` - minimal changes)
- Squad Apps logo asset (SVG or PNG)

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Code Minimalism**:
- [x] Feature scope is minimal and necessary (UI redesign only, no backend)
- [x] Solution approach avoids unnecessary abstractions (pure CSS/HTML, no framework changes)
- [x] Plan identifies code/resources to remove during implementation (emoji icons, dark theme CSS)

**II. Zero Redundancy**:
- [x] No duplicate implementations planned (single HTML template, single CSS file)
- [x] Consistent naming and patterns with existing codebase (maintains Flask structure)
- [x] Shared logic extraction identified where applicable (CSS custom properties for design system)

**III. UI Consistency** (PRIMARY FOCUS - NON-NEGOTIABLE):
- [x] UI patterns consistent with mockup design system (light theme, card layout, progress bars)
- [x] Visual review checkpoint included in tasks (compare against Mockup_ControlPanelUI.png)
- [x] Interaction patterns align with mockup behavior (toggle switches, touch-friendly)
- [x] Design system defined: Colors (#52C41A green, white/light gray), spacing (8/16/24px), typography (large values)

**IV. Quality Over Speed**:
- [x] Design phase completed before implementation tasks (this plan + research.md)
- [x] Test strategy validates correctness (visual comparison, touch target testing)
- [x] Refactoring tasks identified (remove dark theme CSS, consolidate button styles)

**V. Clean Architecture**:
- [x] Folder structure is logical and matches domain (src/ui/ for frontend)
- [x] Each component has single, clear responsibility (HTML=structure, CSS=design, JS=behavior)
- [x] No orphaned or unused resources will be created (remove old dark theme assets)
- [x] Dependencies are unidirectional (UI → Backend API, no circular refs)

**Compliance Notes**:
- This feature exemplifies Principle III (UI Consistency) - entire purpose is to achieve visual consistency with mockup
- Zero backend changes ensures Code Minimalism (Principle I)
- Single source of truth for styles (one CSS file) ensures Zero Redundancy (Principle II)

## Project Structure

### Documentation (this feature)
```
specs/002-redesign-tablet-ui/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (design system decisions)
├── quickstart.md        # Phase 1 output (visual testing guide)
└── tasks.md             # Phase 2 output (/tasks command - NOT YET CREATED)
```

**Note**: No `data-model.md` or `contracts/` created - UI redesign has no data model changes or API contracts.

### Source Code (repository root)
```
src/ui/
├── templates/
│   └── index.html           # PRIMARY CHANGE: Complete redesign matching mockup
├── static/
│   ├── css/
│   │   └── style.css        # PRIMARY CHANGE: Light theme, progress bars, toggles
│   ├── js/
│   │   └── main.js          # MINOR CHANGE: Update class names, no logic changes
│   └── assets/
│       └── squad-logo.svg   # NEW: Squad Apps branding logo
└── app.py                   # UNCHANGED: Backend API stays the same
```

**Files Modified**:
1. `src/ui/templates/index.html` - Complete HTML restructure (4-column sensor grid, 2-column layout)
2. `src/ui/static/css/style.css` - Complete CSS rewrite (light theme, new components)
3. `src/ui/static/js/main.js` - Minor updates (class name changes for new CSS selectors)

**Files Added**:
1. `src/ui/static/assets/squad-logo.svg` - Squad Apps logo

**Files Unchanged**:
- All Python backend files (`src/main.py`, `src/automation/*`, `src/devices/*`, `src/sensors/*`, etc.)
- Database (`src/storage/*`)
- MQTT layer (`src/mqtt/*`)
- Configuration (`config/*.json`)

---

## Phase 0: Research & Technical Decisions

### Design System Definition

**Color Palette** (from mockup analysis):
```css
--primary-green: #52C41A;      /* Active states, progress bars in-range */
--light-gray: #F5F5F5;         /* Background */
--white: #FFFFFF;              /* Card backgrounds */
--border-gray: #D9D9D9;        /* Card borders */
--text-dark: #262626;          /* Primary text */
--text-secondary: #8C8C8C;     /* Secondary text, labels */
--success-green: #52C41A;      /* Online status, ON toggles */
--growth-panel-bg: #F6FFED;    /* Light green for Growth Cycle panel */
--growth-panel-border: #B7EB8F;/* Growth panel border */
```

**Typography** (from mockup):
```css
--font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--value-size: 36px;            /* Sensor values (23.5°C, 68%, etc.) */
--label-size: 14px;            /* Sensor names, targets */
--heading-size: 20px;          /* Section headings */
--body-size: 14px;             /* Body text, device names */
```

**Spacing System** (8px base):
```css
--space-xs: 8px;
--space-sm: 12px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
```

**Card Design**:
- Border radius: 8px
- Box shadow: 0 2px 8px rgba(0,0,0,0.08)
- Padding: 16px (sensors), 24px (panels)
- Border: 1px solid #D9D9D9

### Component Specifications

**1. Progress Bar** (NEW):
```
Visual: Horizontal bar, height 8px, rounded ends
States:
  - In-range: Green (#52C41A)
  - Out-of-range: Red (#FF4D4F) or Orange (#FAAD14)
  - Background: Light gray (#F0F0F0)
Display: Current value position marker on bar
Below: "Target: X-Y°C" or "Reservoir: 70%"
```

**2. Toggle Switch** (REPLACE buttons):
```
Visual: iOS-style toggle, 48px × 28px
States:
  - ON: Green (#52C41A) background, white circle right
  - OFF: Gray (#D9D9D9) background, white circle left
Interaction: Click/tap to toggle, smooth 200ms transition
```

**3. Sensor Card** (REDESIGN):
```
Layout:
  ┌─────────────────┐
  │   Icon Badge    │  (Colored circular badge with icon)
  │   Sensor Name   │  (14px gray text)
  │   23.5°C        │  (36px bold value)
  │ ■■■■■■□□□□□□□  │  (Progress bar)
  │ Target: 22-25°C │  (12px gray)
  └─────────────────┘
```

**4. Icon Badges** (REPLACE emojis):
```
Temperature: Thermometer icon, red/pink background
Humidity: Water droplet icon, blue background
Light: Light bulb icon, yellow background
Water: Water tank icon, blue background

Size: 48px circle
Icon: SVG or icon font, 24px, white color
```

### Layout Grid

**Top: Sensor Grid (4 columns)**
```
┌────────┬────────┬────────┬────────┐
│  Temp  │  Humid │  Light │  Water │
└────────┴────────┴────────┴────────┘
```

**Bottom: 2-Column Layout**
```
┌───────────────────┬──────────────────┐
│ System Controls   │  Growth Cycle    │
│                   │                  │
│ □ Grow Lights     │ Flowering Day 28 │
│ □ Ventilation     │ 12h ON / 12h OFF │
│ □ Water Pump      │ 32 days left     │
│ □ Auto Mode       │                  │
│ □ CO₂ System      │                  │
│ □ Heater          │                  │
└───────────────────┴──────────────────┘
```

### Responsive Breakpoints

- **Desktop/Tablet (≥1024px)**: Full 4-column + 2-column layout
- **Small Tablet (768-1023px)**: 2-column sensors, stacked panels
- **Mobile (<768px)**: Single column (out of scope, tablet primary)

### Technical Decisions

**CSS Architecture**:
- Use CSS custom properties (`:root` variables) for design system
- BEM-like naming for component classes (`.sensor-card`, `.toggle-switch`)
- No CSS preprocessor (Sass/LESS) - pure CSS3
- Flexbox for layout (Grid optional for sensor cards)

**Icon Strategy**:
- **Option A**: Inline SVG icons in HTML (best performance)
- **Option B**: Icon font (Feather Icons, Heroicons)
- **Decision**: Use SVG sprites for crisp rendering and color flexibility

**Logo Asset**:
- Squad Apps logo: SVG format preferred (scalable)
- Fallback: PNG @2x for retina displays
- Placement: Top-left header, ~40px height

**Browser Compatibility**:
- Target: Modern browsers (Chrome 90+, Safari 14+, Firefox 88+)
- No IE11 support needed (tablets use modern browsers)
- CSS Grid and Flexbox safe to use

---

## Phase 1: Contracts, Data Model, Quickstart

### Contracts
**N/A** - No API changes. Existing WebSocket/REST endpoints unchanged:
- `GET /api/sensors` - Still returns same sensor data
- `POST /api/device/<type>/<command>` - Still accepts same commands
- WebSocket events - Still emit same `sensor_update`, `device_update`

### Data Model
**N/A** - No database schema changes. UI consumes existing data structures:
- `SensorReading` model unchanged
- `DeviceControl` model unchanged
- `GrowthCycle` model unchanged
- All backend logic remains identical

### Quickstart: Visual Testing Guide

See [quickstart.md](./quickstart.md) for:
1. Side-by-side visual comparison checklist (mockup vs. implementation)
2. Touch target testing procedure (44px minimum verification)
3. Progress bar accuracy testing (verify calculations match target ranges)
4. Responsive layout testing (tablet orientations)
5. Interactive state testing (toggle switches, hover states)

---

## Phase 2: Task Generation Approach (for /tasks command)

### Task Organization

**Setup Tasks** (T001-T003):
- T001: Create Squad Apps logo asset (SVG)
- T002: Backup current dark theme files (index.html, style.css)
- T003: Create design tokens CSS file with custom properties

**CSS Redesign Tasks** (T004-T010):
- T004: [P] Light theme base styles (background, typography, colors)
- T005: [P] Sensor card component CSS (card layout, spacing)
- T006: [P] Progress bar component CSS (bar, fill, marker)
- T007: [P] Toggle switch component CSS (iOS-style, animations)
- T008: [P] System Controls panel CSS (list, spacing)
- T009: [P] Growth Cycle panel CSS (light green background, bordered boxes)
- T010: [P] Header and footer CSS (logo, connection status, branding)

**HTML Restructure Tasks** (T011-T015):
- T011: Header HTML (logo, title, connection status)
- T012: Sensor card grid HTML (4-column, icon badges, progress bars, targets)
- T013: System Controls HTML (device list with toggles)
- T014: Growth Cycle panel HTML (phase, schedule, countdown)
- T015: Footer HTML (Squad Apps branding, last sync)

**JavaScript Updates** (T016-T017):
- T016: Update JavaScript selectors for new CSS classes
- T017: Add progress bar update logic (calculate percentage from min/max)

**Visual Testing Tasks** (T018-T020):
- T018: Visual comparison against mockup (screenshot comparison)
- T019: Touch target verification (measure button/toggle sizes)
- T020: Responsive layout testing (tablet portrait/landscape)

**Polish & Cleanup** (T021-T023):
- T021: Remove old dark theme CSS rules
- T022: Remove emoji icon references
- T023: Constitutional UI Consistency review (final check)

### Parallel Execution Opportunities

Tasks marked `[P]` can run in parallel:
- T004-T010: All CSS component tasks (different CSS sections)
- Different HTML sections can be worked on simultaneously

### Dependency Chain

```
T001-T003 (Setup)
  ↓
T004-T010 (CSS) [Parallel]
  ↓
T011-T015 (HTML) [Sequential - depends on CSS classes]
  ↓
T016-T017 (JavaScript)
  ↓
T018-T020 (Visual Testing)
  ↓
T021-T023 (Cleanup)
```

### Testing Strategy

**Visual Regression Testing**:
1. Capture screenshot of mockup (Mockup_ControlPanelUI.png)
2. Capture screenshot of implementation
3. Overlay images at 50% opacity to compare
4. Verify: colors, spacing, typography, component sizes
5. Document any intentional deviations

**Touch Target Testing**:
1. Inspect element for toggle switches
2. Verify computed dimensions ≥44px × 44px
3. Test with actual touch on tablet device
4. Ensure no mis-taps on adjacent controls

**Progress Bar Accuracy Testing**:
```javascript
// Test case: Temperature 23.5°C, target 22-25°C
// Expected: Progress bar ~50% filled (1.5 / 3.0 range)
// Verify: Visual progress bar matches calculated percentage
```

---

## Complexity Tracking

### Constitutional Compliance
- **Primary Principle**: III. UI Consistency (NON-NEGOTIABLE) ✅
- **Justification**: Entire feature is designed to achieve UI consistency with mockup
- **Impact**: Zero backend complexity, purely visual enhancement

### Trade-offs
- **Decision**: Pure CSS/HTML redesign (no new frameworks)
  - **Rationale**: Maintains Code Minimalism (Principle I), avoids dependency bloat
  - **Trade-off**: Manual CSS vs. component library (e.g., Ant Design)
  - **Chosen**: Manual CSS for full control and zero dependencies

- **Decision**: SVG icons vs. Icon font
  - **Rationale**: SVGs offer better color control and crispness
  - **Trade-off**: Inline SVG increases HTML size vs. icon font caching
  - **Chosen**: SVG sprites for flexibility and modern browser support

### Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| CSS breaks existing functionality | High | Incremental changes, test after each component |
| Progress bar math incorrect | Medium | Unit tests for percentage calculation, visual verification |
| Touch targets too small | High | Measure with dev tools, test on real tablet |
| New design doesn't match mockup | High | Side-by-side screenshot comparison, iterate until pixel-perfect |

---

## Progress Tracking

- [x] **Step 1**: Feature spec loaded
- [x] **Step 2**: Technical context filled
- [x] **Step 3**: Constitution check filled
- [x] **Step 4**: Initial constitution check passed
- [x] **Step 5**: Phase 0 research complete (research.md)
- [x] **Step 6**: Phase 1 artifacts complete (quickstart.md - no contracts/data-model needed)
- [x] **Step 7**: Post-design constitution check passed
- [x] **Step 8**: Task generation approach planned
- [x] **Step 9**: STOPPED - Ready for /tasks command

---

## Next Steps

**Ready for `/tasks` command** to generate detailed task breakdown with:
- File paths for each change
- Specific CSS class names and HTML structure
- JavaScript selector updates
- Visual testing checkpoints
- Constitutional compliance verification tasks

**After `/tasks`**:
- Execute implementation tasks (T001-T023)
- Perform visual comparison against mockup
- Validate touch targets on real tablet
- Verify progress bar calculations
- Final UI Consistency review before merge
