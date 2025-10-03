# Tasks: UI Redesign for 1024x600 Tablet Display

**Input**: Design documents from `specs/004-ui-redesign-for/`
**Prerequisites**: plan.md, research.md, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Extract: Flask web app, HTML/CSS/JS modification scope
   → Structure: src/ui/ contains templates/, static/css/, static/js/
2. Load design documents:
   → research.md: Current UI structure, classes to remove
   → quickstart.md: Detailed layout specs, validation checklist
3. Generate tasks by category:
   → Preparation: Backups, baseline screenshots
   → HTML restructuring: Remove Growth Cycle panel, consolidate controls
   → CSS updates: Remove growth styles, add controls header styles
   → Validation: Visual testing, functionality verification
   → Polish: Cleanup unused code, constitutional compliance
4. Apply task rules:
   → HTML before CSS before JS validation (sequential dependencies)
   → Backup first for easy rollback
   → Visual validation after each major change
5. Number tasks sequentially (T001, T002...)
6. Validate completeness:
   → All HTML changes specified?
   → All CSS removals identified?
   → Visual validation comprehensive?
   → Constitutional compliance included?
7. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **UI Files**: `src/ui/templates/index.html`, `src/ui/static/css/style.css`, `src/ui/static/js/main.js`
- **Backups**: Same directory with `.backup` extension
- **Screenshots**: Documented in task descriptions

---

## Phase 3.1: Preparation

- [x] **T001** Create backup of current HTML file
  - **File**: `src/ui/templates/index.html` → `src/ui/templates/index.html.backup`
  - **Action**: Copy current file to backup before any modifications
  - **Verification**: Backup file exists and is identical to original

- [x] **T002** Create backup of current CSS file
  - **File**: `src/ui/static/css/style.css` → `src/ui/static/css/style.css.backup`
  - **Action**: Copy current file to backup before any modifications
  - **Verification**: Backup file exists and is identical to original

- [ ] **T003** Document baseline screenshots at 1024x600
  - **Action**: Start Flask app, open browser at 1024x600 resolution, screenshot current UI
  - **Save**: Document current layout appearance for comparison
  - **Purpose**: Establish "before" state for visual validation (Manual - user must perform)

---

## Phase 3.2: HTML Restructuring (Sequential - Same File)

**CRITICAL: These tasks modify index.html sequentially. Complete in order.**

- [x] **T004** Remove `.panels-container` wrapper div
  - **File**: `src/ui/templates/index.html`
  - **Location**: Around line 68
  - **Action**: Delete `<div class="panels-container">` opening tag and corresponding closing `</div>` (after Growth Cycle panel)
  - **Rationale**: No longer need 2-column grid layout
  - **Verification**: `.system-controls-panel` and `.growth-panel` are now siblings under `.container`, not wrapped

- [x] **T005** Remove Growth Cycle panel entirely
  - **File**: `src/ui/templates/index.html`
  - **Location**: Lines approximately 118-134
  - **Action**: Delete entire `<section class="section growth-panel">...</section>` block
  - **Includes**: Remove h2, `.growth-phase-highlight`, `.phase-toggle-container` (will be moved to controls)
  - **Verification**: No `<section class="section growth-panel">` exists in HTML

- [x] **T006** Add `.controls-header` div to System Controls panel
  - **File**: `src/ui/templates/index.html`
  - **Location**: Inside `.system-controls-panel`, before `.device-list`
  - **Action**: Insert new `<div class="controls-header">` containing h2 and phase toggle
  - **Structure**:
    ```html
    <div class="controls-header">
        <h2>System Controls</h2>
        <div class="phase-toggle-container">
            <!-- Phase toggle here -->
        </div>
    </div>
    ```
  - **Verification**: h2 "System Controls" and phase toggle are inside `.controls-header`

- [x] **T007** Move Vegetative/Flowering toggle to controls header
  - **File**: `src/ui/templates/index.html`
  - **Location**: From deleted Growth Cycle panel to `.controls-header .phase-toggle-container`
  - **Action**: Copy `#phaseToggle` input, switch, and labels into new `.phase-toggle-container`
  - **Simplification**: Replace complex `.phase-label` wrapper with:
    ```html
    <div class="phase-toggle-container">
        <span class="phase-label-text">Vegetative (18/6)</span>
        <label class="switch">
            <input type="checkbox" id="phaseToggle" onchange="togglePhase()">
            <span class="slider"></span>
        </label>
        <span class="phase-label-text">Flowering (12/12)</span>
    </div>
    ```
  - **Verification**: `#phaseToggle` exists inside `.controls-header`, labels show "Vegetative (18/6)" and "Flowering (12/12)"

- [x] **T008** Verify all device toggles preserved
  - **File**: `src/ui/templates/index.html`
  - **Location**: `.device-list` inside `.system-controls-panel`
  - **Action**: Confirm all 6 device items exist unchanged:
    - Grow Lights (#lightsToggle)
    - Ventilation (#ventilationToggle)
    - Water Pump (#pumpToggle)
    - Auto Mode (#autoModeToggle)
    - CO₂ System (#co2Toggle)
    - Heater (#heaterToggle)
  - **Verification**: All 6 toggles present with correct IDs and onchange handlers

---

## Phase 3.3: CSS Updates

**CRITICAL: These tasks modify style.css. Complete in order.**

- [x] **T009** Remove `.panels-container` CSS rule
  - **File**: `src/ui/static/css/style.css`
  - **Location**: Approximately lines 145-150
  - **Action**: Delete entire `.panels-container { display: grid; grid-template-columns: 1fr 1fr; ... }` rule
  - **Rationale**: Container no longer exists in HTML
  - **Verification**: No `.panels-container` selector in CSS

- [x] **T010** Remove all Growth Cycle CSS rules
  - **File**: `src/ui/static/css/style.css`
  - **Location**: Approximately lines 152-219
  - **Action**: Delete all of these rules:
    - `.growth-panel`
    - `.growth-phase-highlight`
    - `.growth-info-box` and child selectors
    - `.phase-info` and child selectors
    - `.phase-controls`
    - `.btn-phase`
  - **Estimated**: ~70 lines removed
  - **Verification**: No growth cycle related selectors remain (except `.phase-toggle-container` which is kept)

- [x] **T011** Add `.controls-header` CSS rule
  - **File**: `src/ui/static/css/style.css`
  - **Location**: After `.system-controls-panel` rule (around line 381)
  - **Action**: Add new rule:
    ```css
    .controls-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--space-md);
        padding-bottom: var(--space-md);
        border-bottom: 1px solid var(--border-gray);
    }

    .controls-header h2 {
        margin: 0;
        font-size: var(--heading-size);
        color: var(--text-dark);
        font-weight: 600;
    }
    ```
  - **Verification**: Header displays with Flexbox layout, border at bottom

- [x] **T012** Update `.system-controls-panel` CSS rule
  - **File**: `src/ui/static/css/style.css`
  - **Location**: Approximately line 375
  - **Action**: Add `margin-top: var(--space-lg);` to existing rule (panel no longer in grid, needs top margin)
  - **Verification**: System Controls panel has appropriate top spacing

- [x] **T013** Update `.phase-toggle-container` CSS for new position
  - **File**: `src/ui/static/css/style.css`
  - **Location**: Around line 222
  - **Action**: Update rule to:
    ```css
    .phase-toggle-container {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }

    .phase-label-text {
        font-size: var(--label-size);
        color: var(--text-secondary);
        white-space: nowrap;
    }
    ```
  - **Note**: Remove old `.phase-label` complex wrapper styles, add simple `.phase-label-text`
  - **Verification**: Toggle displays horizontally with labels on both sides

- [x] **T014** Update 1024x600 media query
  - **File**: `src/ui/static/css/style.css`
  - **Location**: Line 526
  - **Action**:
    - Remove `.growth-panel { padding: 16px; }` rule
    - Add `.system-controls-panel { padding: 16px; }` rule
    - Add `.controls-header { margin-bottom: 12px; padding-bottom: 12px; }` rule
  - **Verification**: Spacing optimized for 1024x600 viewport

- [x] **T015** Update responsive breakpoint at 1023px
  - **File**: `src/ui/static/css/style.css`
  - **Location**: Line 542
  - **Action**: Remove `.panels-container { grid-template-columns: 1fr; }` rule (container no longer exists)
  - **Verification**: No references to `.panels-container` in media queries

---

## Phase 3.4: JavaScript Verification

- [x] **T016** Verify phase toggle event handler still works
  - **File**: `src/ui/static/js/main.js`
  - **Action**: Check if `togglePhase()` function references any DOM elements by ID
  - **Result**: Uses `getElementById('phaseToggle')` which is preserved in restructured HTML
  - **Verification**: No JavaScript changes required - all selectors use IDs which remain unchanged

- [x] **T017** Verify all device toggle handlers unchanged
  - **File**: `src/ui/static/js/main.js`
  - **Action**: Confirm `toggleDevice()` and `toggleAutoMode()` functions work
  - **Result**: Uses `getElementById(deviceType + 'Toggle')` pattern - all IDs preserved
  - **Verification**: No JavaScript changes required

---

## Phase 3.5: Visual Validation (Sequential Testing)

**CRITICAL: Test in order at 1024x600 resolution. These tasks require manual browser testing.**

- [ ] **T018** Visual validation: Sensor cards layout (MANUAL - requires running Flask app)
  - **Browser**: Set to 1024x600 resolution
  - **Check**:
    - [ ] All 4 sensor cards visible in single horizontal row
    - [ ] Equal width distribution (~230px each)
    - [ ] Icons, values, progress bars, targets all visible
    - [ ] No text truncation or overflow
  - **Reference**: quickstart.md Visual Validation Checklist - Sensor Cards section
  - **Screenshot**: Capture for documentation

- [ ] **T019** Visual validation: System Controls panel structure
  - **Browser**: 1024x600 resolution
  - **Check**:
    - [ ] Panel displays full width below sensors
    - [ ] Header row contains "System Controls" on left
    - [ ] Vegetative/Flowering toggle on right side of header
    - [ ] Toggle labels: "Vegetative (18/6)" and "Flowering (12/12)"
    - [ ] Border line separates header from device list
    - [ ] All 6 device rows visible without scrolling
  - **Reference**: quickstart.md Visual Validation Checklist - System Controls Panel section
  - **Screenshot**: Capture for documentation

- [ ] **T020** Visual validation: Growth Cycle removal confirmed
  - **Browser**: 1024x600 resolution
  - **Check**:
    - [ ] Growth Cycle panel completely absent
    - [ ] No empty space or layout gaps where panel was
    - [ ] No console errors about missing elements
  - **Reference**: quickstart.md Visual Validation Checklist - Growth Cycle Panel section
  - **Verification**: Panel successfully removed from UI

- [ ] **T021** Visual validation: Header and footer preserved
  - **Browser**: 1024x600 resolution
  - **Check**:
    - [ ] Header: Squad Apps logo, "GrowBox Control Panel", Online status
    - [ ] Footer: "Powered by Squad Apps • Last sync: [time]"
    - [ ] Both elements appear identical to before
  - **Reference**: quickstart.md Visual Validation Checklist - Header & Footer section
  - **Verification**: Header and footer unchanged

- [ ] **T022** Viewport fit validation: No scrolling required
  - **Browser**: Exactly 1024x600 pixels
  - **Check**:
    - [ ] No horizontal scrollbar
    - [ ] No vertical scrollbar
    - [ ] All content fits within viewport
    - [ ] Adequate spacing (not cramped)
  - **Reference**: quickstart.md Visual Validation Checklist - Viewport Fit section
  - **Critical**: This is primary success criterion

- [ ] **T023** Functionality validation: Device toggles
  - **Browser**: 1024x600 resolution
  - **Test each toggle**:
    - [ ] Grow Lights on/off
    - [ ] Ventilation on/off
    - [ ] Water Pump on/off
    - [ ] Auto Mode on/off
    - [ ] CO₂ System on/off
    - [ ] Heater on/off
  - **Verify**: Toggle visual state updates, backend API calls trigger (check Network tab)
  - **Reference**: quickstart.md Functionality Verification - Device Toggles section

- [ ] **T024** Functionality validation: Phase toggle
  - **Browser**: 1024x600 resolution
  - **Test**:
    - [ ] Click toggle to switch modes
    - [ ] Slider moves visually
    - [ ] Label styling indicates active mode
    - [ ] Backend API call `/api/growth_phase/{phase}` triggers
  - **DevTools**: Check Network tab for POST request
  - **Reference**: quickstart.md Functionality Verification - Phase Toggle section

- [ ] **T025** Functionality validation: Real-time updates
  - **Browser**: 1024x600 resolution
  - **Test**:
    - [ ] Sensor values update via WebSocket
    - [ ] Progress bars animate on changes
    - [ ] Color coding works (green/red)
    - [ ] Connection status indicator updates
    - [ ] No console errors
  - **Reference**: quickstart.md Functionality Verification - Sensor Updates section
  - **Verification**: WebSocket connection intact, real-time updates working

---

## Phase 3.6: Polish & Constitutional Compliance

- [x] **T026** [P] Remove commented-out code from HTML
  - **File**: `src/ui/templates/index.html`
  - **Action**: Search for and delete any commented-out HTML blocks (e.g., old Growth Cycle code if commented instead of deleted)
  - **Constitution**: Code Minimalism - "Delete unused code, commented-out blocks immediately"
  - **Result**: All comments are valid section markers, no dead code found

- [x] **T027** [P] Remove commented-out code from CSS
  - **File**: `src/ui/static/css/style.css`
  - **Action**: Search for and delete any commented CSS rules related to removed growth cycle
  - **Constitution**: Code Minimalism - "Delete unused code, commented-out blocks immediately"
  - **Result**: All comments are valid section headers, no dead code found

- [x] **T028** Verify no orphaned CSS classes
  - **Files**: `src/ui/static/css/style.css`, `src/ui/templates/index.html`
  - **Action**:
    - List all CSS class selectors in style.css
    - Verify each class is used in index.html OR is a state class (e.g., `.online`, `.out-of-range`)
    - Remove any classes defined but never used
  - **Constitution**: Clean Architecture - "No orphaned files—every file must be reachable from entry points"
  - **Result**: Removed orphaned classes: `.device-state`, `.device-controls`, `.devices-grid`, `.device-card`, `.btn`, `.btn:disabled` (~30 lines)

- [ ] **T029** Visual design consistency verification (MANUAL - requires browser testing)
  - **Browser**: 1024x600 resolution
  - **Check**:
    - [ ] Colors match design system (green, gray, white preserved)
    - [ ] Typography sizes consistent (36px values, 20px headings, 14px labels)
    - [ ] Spacing uniform (12-16px at 1024x600)
    - [ ] Icons unchanged (🌡💧☀🚰)
  - **Constitution**: UI Consistency - "Visual hierarchy and layout patterns must remain uniform"
  - **Reference**: quickstart.md Visual Design Consistency section
  - **Verification**: All design tokens preserved from original UI

- [ ] **T030** Compare against goal mockup (UIGoal.png) (MANUAL - requires browser testing)
  - **Browser**: 1024x600 resolution
  - **Action**: Side-by-side comparison of implemented UI with UIGoal.png
  - **Check**:
    - [ ] Sensor cards layout matches (4 horizontal)
    - [ ] System Controls structure matches (single card with header)
    - [ ] Phase toggle position matches (top-right of controls)
    - [ ] Growth Cycle removed as shown in goal
    - [ ] Footer retained as shown in goal
  - **Constitution**: UI Consistency - "UI patterns consistent with existing design system"
  - **Reference**: quickstart.md Comparison Against Goal Mockup section
  - **Acceptable**: Icon styling differences (goal is mockup)

- [ ] **T031** Cross-browser testing (MANUAL - requires multiple browsers)
  - **Browsers**: Chrome/Edge, Firefox, (Safari if available)
  - **Resolution**: 1024x600
  - **Test**:
    - [ ] Layout renders identically
    - [ ] Toggles function correctly
    - [ ] WebSocket updates work
    - [ ] No browser-specific bugs
  - **Reference**: quickstart.md Testing Procedure - Cross-Browser Testing
  - **Verification**: Consistent rendering across browsers

- [ ] **T032** Responsive testing at other resolutions (MANUAL - requires browser testing)
  - **Resolutions**: 1024x600 (target), 1023px (breakpoint), 768px (mobile)
  - **Test**:
    - [ ] 1024x600: Single row sensors, single controls card
    - [ ] 1023px: 2-column sensors, vertical controls stack
    - [ ] 768px: Single column layout
  - **Reference**: quickstart.md Testing Procedure - Responsive Testing
  - **Verification**: No layout breakage at any size

- [x] **T033** Final code cleanup and formatting
  - **Files**: `src/ui/templates/index.html`, `src/ui/static/css/style.css`
  - **Action**:
    - Verify proper indentation in HTML
    - Verify CSS rules are organized logically
    - Remove extra blank lines
    - Ensure consistent formatting
  - **Constitution**: Clean Architecture - "Code organization must be logical, discoverable, and maintainable"
  - **Result**: Files are properly formatted, indentation consistent, no extra blank lines

---

## Dependencies

**Sequential Dependencies**:
- T001, T002 (backups) → T004-T015 (all modifications)
- T003 (baseline) → T018-T025 (visual validation)
- T004-T008 (HTML changes) → T009-T015 (CSS changes)
- T009-T015 (CSS changes) → T016-T017 (JS verification)
- T016-T017 (JS verification) → T018-T025 (visual validation)
- T018-T025 (validation) → T026-T033 (polish)

**Parallel Opportunities**:
- T026, T027 can run in parallel (different concerns, same phase)

**Critical Path**:
1. Backups (T001-T002)
2. HTML restructuring (T004-T008) - MUST be sequential
3. CSS updates (T009-T015) - MUST be sequential
4. JS verification (T016-T017)
5. Visual validation (T018-T025)
6. Polish (T026-T033)

**Blocking Relationships**:
- HTML changes block CSS changes (CSS depends on new HTML structure)
- CSS changes block visual validation (need complete styling)
- Visual validation blocks polish (need working UI to cleanup)

---

## Parallel Example

Only limited parallelism in this UI redesign due to same-file modifications:

```
# T026 and T027 can run in parallel (different files):
Task: "Remove commented-out code from HTML in src/ui/templates/index.html"
Task: "Remove commented-out code from CSS in src/ui/static/css/style.css"
```

**Note**: Most tasks are sequential because they modify the same 2 files (index.html, style.css).

---

## Notes

- **Backup First**: T001-T002 enable easy rollback if issues arise
- **Sequential HTML/CSS**: Same-file modifications prevent parallelization
- **Visual Validation**: T018-T025 must be done at exact 1024x600 resolution
- **Constitutional Compliance**: T026-T033 ensure code quality and consistency
- **Commit Frequency**: Consider committing after each major phase (HTML done, CSS done, validation passed)

---

## Validation Checklist
*GATE: Verified during task generation*

- [x] All HTML changes specified (T004-T008)
- [x] All CSS removals identified (T009-T010, ~70 lines)
- [x] All CSS additions specified (T011-T015)
- [x] Visual validation comprehensive (T018-T025, covers all aspects of quickstart.md)
- [x] Functionality testing included (T023-T025)
- [x] Constitutional compliance tasks included (T026-T033):
  - [x] Code minimalism (T026-T027: remove commented code)
  - [x] Zero redundancy (T028: remove orphaned classes)
  - [x] UI consistency (T029-T030: verify design system)
  - [x] Clean architecture (T028, T033: organized code)
- [x] Each task specifies exact file path
- [x] Tasks ordered by dependencies (HTML → CSS → JS → Validation → Polish)
- [x] Parallel tasks identified where possible (limited due to same-file edits)
- [x] Success criteria referenced (quickstart.md validation checklist)

---

**Estimated Time**: 3-4 hours for complete implementation and validation
**Risk Level**: Low (pure visual changes, no functionality modifications, backups created)
**Rollback**: Use .backup files if issues arise
