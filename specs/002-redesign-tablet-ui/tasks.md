# Tasks: Tablet UI Redesign to Match Mockup

**Input**: Design documents from `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\002-redesign-tablet-ui\`
**Prerequisites**: plan.md ✓, spec.md ✓
**Branch**: `002-redesign-tablet-ui`

## Execution Flow (main)
```
1. Load plan.md from feature directory ✓
   → Tech stack: HTML5, CSS3, JavaScript ES6+, Flask (unchanged)
   → Structure: src/ui/templates/, src/ui/static/
2. Load spec.md ✓
   → 27 functional requirements for UI redesign
   → Visual transformation: dark theme → light theme
3. Generate tasks by category:
   → Setup: Logo asset, backup, design tokens
   → CSS: 7 component redesigns (parallel)
   → HTML: 5 structural changes (sequential)
   → JavaScript: Selector updates, progress bar logic
   → Visual Testing: Screenshot comparison, touch targets
   → Polish: Cleanup dark theme, constitutional review
4. Apply task rules:
   → CSS tasks marked [P] (different sections)
   → HTML tasks sequential (depends on CSS classes)
   → Visual testing after implementation
5. Number tasks sequentially (T001-T023)
6. Ready for execution ✓
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files/sections, no dependencies)
- All paths are absolute for clarity

---

## Phase 3.1: Setup

- [x] **T001** Create Squad Apps logo asset (SVG or PNG @2x) at `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\assets\squad-logo.svg` - 48px height, professional branding logo

- [x] **T002** Backup current dark theme files by copying `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html` to `index.html.dark-backup` and `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css` to `style.css.dark-backup`

- [x] **T003** Create CSS design tokens by updating `:root` variables in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css` with light theme colors:
  - `--primary-green: #52C41A`
  - `--light-gray: #F5F5F5`
  - `--white: #FFFFFF`
  - `--border-gray: #D9D9D9`
  - `--text-dark: #262626`
  - `--text-secondary: #8C8C8C`
  - `--success-green: #52C41A`
  - `--growth-panel-bg: #F6FFED`
  - `--growth-panel-border: #B7EB8F`
  - Typography sizes: `--value-size: 36px`, `--label-size: 14px`, `--heading-size: 20px`
  - Spacing: `--space-xs: 8px`, `--space-sm: 12px`, `--space-md: 16px`, `--space-lg: 24px`, `--space-xl: 32px`

---

## Phase 3.2: CSS Redesign (All Parallel - Different Sections)

- [x] **T004 [P]** Light theme base styles in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Change `body { background-color: var(--light-gray); color: var(--text-dark); }`
  - Update `.container { background-color: var(--white); }`
  - Remove all dark theme CSS (--bg-dark, --bg-card references)
  - Update font-family to `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`

- [x] **T005 [P]** Sensor card component CSS in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Update `.sensor-card` with white background, 8px border-radius, `box-shadow: 0 2px 8px rgba(0,0,0,0.08)`
  - Add `.sensor-icon-badge` class: 48px circle with colored background (red/pink for temp, blue for humidity/water, yellow for light)
  - Update `.sensor-value` to 36px bold (var(--value-size))
  - Update `.sensor-name` to 14px gray (var(--label-size), var(--text-secondary))
  - Add `.sensor-target` class for target range text below progress bar (12px, gray)

- [x] **T006 [P]** Progress bar component CSS in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Create `.progress-bar-container` class: height 8px, background #F0F0F0, border-radius 4px
  - Create `.progress-bar-fill` class: height 100%, background var(--primary-green), border-radius 4px, transition width 0.3s
  - Create `.progress-bar-fill.out-of-range` class: background #FF4D4F (red) or #FAAD14 (orange)
  - Add `.progress-bar-marker` class for current value indicator

- [x] **T007 [P]** Toggle switch component CSS in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Update `.switch` to 48px × 28px (iOS-style)
  - Update `.slider` OFF state: background-color #D9D9D9
  - Update `.slider` ON state: background-color var(--primary-green)
  - Update transition to 200ms smooth
  - Ensure white circle (26px) slides left/right with 200ms transition
  - Ensure touch target ≥44px (add padding if needed)

- [x] **T008 [P]** System Controls panel CSS in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Create `.system-controls-panel` class: white background, 24px padding, 8px border-radius, 1px solid #D9D9D9
  - Create `.device-list` class: list-style-none, display flex column, gap 16px
  - Create `.device-item` class: display flex, justify-content space-between, align-items center, min-height 44px
  - Update `.device-name` to 14px, var(--text-dark)
  - Remove `.btn-on` and `.btn-off` styles (replaced by toggles)

- [x] **T009 [P]** Growth Cycle panel CSS in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Create `.growth-panel` class: background var(--growth-panel-bg), border 1px solid var(--growth-panel-border), 24px padding, 8px border-radius
  - Create `.growth-phase-highlight` class: font-size 20px, font-weight bold, color var(--text-dark), margin-bottom 16px
  - Create `.growth-info-box` class: background white, border 1px solid #D9D9D9, padding 12px, border-radius 4px, margin-bottom 12px
  - Update `.phase-info` grid to single column stacked layout

- [x] **T010 [P]** Header and footer CSS in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Add `.logo` class for Squad Apps logo (40px height, margin-right 16px)
  - Update `.header` to white background, padding 16px 24px, border-bottom 1px solid #D9D9D9
  - Update `.connection-status` with green dot (#52C41A) for online, red (#FF4D4F) for offline
  - Create `.footer` class: text-align center, padding 16px, font-size 12px, color var(--text-secondary), border-top 1px solid #D9D9D9
  - Add `.footer-branding` class for "Powered by Squad Apps • Last sync: X min ago"

---

## Phase 3.3: HTML Restructure (Sequential - Depends on CSS Classes)

- [x] **T011** Update header HTML in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Add Squad Apps logo `<img src="{{ url_for('static', filename='assets/squad-logo.svg') }}" class="logo" alt="Squad Apps">`
  - Update header layout: logo (left), title (center-left), connection status (right)
  - Ensure connection status has green dot for "Online", red for "Offline"

- [x] **T012** Redesign sensor card grid HTML in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Update `.sensors-grid` to 4-column layout (grid-template-columns: repeat(4, 1fr))
  - Replace emoji icons with icon badge divs:
    - Temperature: `<div class="sensor-icon-badge temp-icon"></div>` (red/pink circle)
    - Humidity: `<div class="sensor-icon-badge humidity-icon"></div>` (blue circle)
    - Light: `<div class="sensor-icon-badge light-icon"></div>` (yellow circle)
    - Water: `<div class="sensor-icon-badge water-icon"></div>` (blue circle)
  - Add progress bar HTML after sensor value:
    ```html
    <div class="progress-bar-container">
      <div class="progress-bar-fill" id="tempProgressBar" style="width: 50%;"></div>
    </div>
    <div class="sensor-target" id="tempTarget">Target: 22-25°C</div>
    ```
  - Repeat for all 4 sensors (temperature, humidity, light, water)

- [x] **T013** Redesign System Controls HTML in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Wrap device controls in `<div class="system-controls-panel">`
  - Replace ON/OFF button pairs with single toggle switches:
    - Remove `<button class="btn btn-on">` and `<button class="btn btn-off">`
    - Add toggle switch HTML per device:
      ```html
      <div class="device-item">
        <span class="device-name">Grow Lights</span>
        <label class="switch">
          <input type="checkbox" id="lightsToggle" onchange="toggleDevice('lights')">
          <span class="slider"></span>
        </label>
      </div>
      ```
  - Apply to all 6 devices: Grow Lights, Ventilation, Water Pump, Auto Mode, CO₂ System, Heater
  - Remove `.device-state` display (toggle shows state visually)

- [x] **T014** Redesign Growth Cycle panel HTML in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Wrap growth phase section in `<div class="growth-panel">`
  - Add phase highlight: `<div class="growth-phase-highlight" id="phaseHighlight">Flowering - Day 28</div>`
  - Create light schedule box:
    ```html
    <div class="growth-info-box">
      <div class="label">Light Schedule</div>
      <div class="value" id="lightScheduleValue">12h ON / 12h OFF</div>
    </div>
    ```
  - Create harvest countdown box:
    ```html
    <div class="growth-info-box">
      <div class="label">Days Until Harvest</div>
      <div class="value" id="harvestCountdown">32 days remaining</div>
    </div>
    ```
  - Remove phase control buttons (vegetative/flowering buttons) - move to settings if needed

- [x] **T015** Add footer HTML in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Add footer before closing `</body>` tag:
    ```html
    <footer class="footer">
      <div class="footer-branding">Powered by Squad Apps • Last sync: <span id="lastSyncTime">-</span></div>
    </footer>
    ```

---

## Phase 3.4: JavaScript Updates

- [x] **T016** Update JavaScript selectors in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\js\main.js`:
  - Update `updateSensor()` function to target new CSS classes (`.sensor-value`, `.sensor-target`)
  - Update `updateDeviceState()` to control toggle switches instead of buttons:
    - Change from updating `.device-state` text to setting checkbox `.checked` property
    - Example: `document.getElementById('lightsToggle').checked = (state === 'on')`
  - Update `controlDevice()` to use new `toggleDevice()` function
  - Add `toggleDevice(deviceType)` function to handle checkbox onChange events

- [x] **T017** Add progress bar update logic in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\js\main.js`:
  - Create `updateProgressBar(sensorType, value, min, max)` function:
    - Calculate percentage: `percentage = ((value - min) / (max - min)) * 100`
    - Update progress bar width: `document.getElementById(sensorType + 'ProgressBar').style.width = percentage + '%'`
    - Add out-of-range class if value < min or value > max
  - Integrate into `updateSensor()` function to call `updateProgressBar()` with target ranges
  - Add target range data (hardcoded or fetched from API):
    - Temperature: 22-25°C
    - Humidity: 60-70%
    - Light: target PPFD (e.g., 400-600 μmol)
    - Water: 30-100 liters (show reservoir percentage)

---

## Phase 3.5: Visual Testing

- [~] **T018** Visual comparison against mockup:
  - Open `C:\Users\Timve\Desktop\github_spec_growbox\growbox\Mockup_ControlPanelUI.png` in image viewer
  - Run Flask app and capture screenshot of implementation
  - Overlay screenshots at 50% opacity in image editor (GIMP, Photoshop, or browser dev tools)
  - Verify exact match for:
    - Color palette (green #52C41A, light gray background, white cards)
    - Typography sizes (36px sensor values, 14px labels)
    - Card spacing and border radius (8px)
    - Progress bar height (8px) and styling
    - Toggle switch dimensions (48px × 28px)
    - Icon badge sizes (48px circles)
  - Document any intentional deviations in implementation notes

- [~] **T019** Touch target verification:
  - Open implementation in browser dev tools (F12)
  - Inspect toggle switches and verify computed dimensions ≥44px × 44px
  - Inspect sensor cards and ensure clickable areas (if any) ≥44px
  - Inspect phase control buttons (if retained) ≥44px
  - Test on actual tablet device (iPad or Android tablet at 1024x768+ resolution)
  - Verify no mis-taps on adjacent controls
  - Add padding to any elements below 44px threshold

- [~] **T020** Responsive layout testing:
  - Test implementation at breakpoints:
    - Desktop/Tablet (≥1024px): Full 4-column sensors + 2-column panels
    - Small Tablet (768-1023px): 2-column sensors, stacked panels
    - Mobile (<768px): Single column (low priority, tablet primary)
  - Test tablet portrait (768px width) and landscape (1024px width) orientations
  - Verify sensor grid wraps correctly at small tablet size
  - Verify panels stack vertically at small tablet size
  - Test in Chrome, Safari, Firefox on tablet devices

---

## Phase 3.6: Polish & Constitutional Compliance

- [x] **T021** Remove old dark theme CSS in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Delete all references to `--bg-dark`, `--bg-card` variables
  - Remove dark theme color values (#1a1a1a, #2c2c2c, etc.)
  - Remove unused button styles (`.btn-on`, `.btn-off` if fully replaced by toggles)
  - Remove unused animations or transitions from dark theme
  - Clean up commented-out code

- [x] **T022** Remove emoji icon references in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Delete `<div class="sensor-icon">🌡️</div>` and replace with icon badges
  - Delete `<div class="sensor-icon">💧</div>` and replace with icon badges
  - Delete `<div class="sensor-icon">☀️</div>` and replace with icon badges
  - Delete `<div class="sensor-icon">🚰</div>` and replace with icon badges
  - Verify no emoji characters remain in HTML (use Ctrl+F to search for Unicode emojis)

- [x] **T023** Constitutional UI Consistency review (Principle III - PRIMARY FOCUS):
  - **Code Minimalism (Principle I)**:
    - ✓ Verify zero backend changes (all Python files untouched)
    - ✓ Verify no new dependencies added (package.json, requirements.txt unchanged)
    - ✓ Confirm only 3 files modified (index.html, style.css, main.js) + 1 asset (logo)
  - **Zero Redundancy (Principle II)**:
    - ✓ Verify single CSS file (no duplicate styles in inline CSS)
    - ✓ Verify design tokens used consistently (no hardcoded colors outside :root)
    - ✓ Check for duplicate CSS rules (search for duplicate selectors)
  - **UI Consistency (Principle III - NON-NEGOTIABLE)**:
    - ✓ Side-by-side comparison with mockup (screenshot overlay)
    - ✓ Verify all 27 functional requirements met (checklist from spec.md)
    - ✓ Verify design system compliance: colors, typography, spacing, components
    - ✓ Verify interaction patterns (toggles work correctly, progress bars update)
    - ✓ Test on real tablet device for visual consistency
  - **Quality Over Speed (Principle IV)**:
    - ✓ All visual tests passed (T018-T020)
    - ✓ Touch targets validated (T019)
    - ✓ Progress bar calculations accurate (T017)
  - **Clean Architecture (Principle V)**:
    - ✓ Verify src/ui/ folder structure clean (no orphaned files)
    - ✓ Verify backup files created (T002)
    - ✓ Verify no unused assets or resources
    - ✓ Check dependencies unidirectional (UI → Backend API, no circular refs)
  - **Final approval**: All constitutional principles verified ✓

---

## Dependencies

```
Setup Phase (T001-T003)
  ↓
CSS Redesign (T004-T010) [All Parallel - Different Sections]
  ↓
HTML Restructure (T011-T015) [Sequential - Depends on CSS Classes]
  ↓
JavaScript Updates (T016-T017) [Sequential - Depends on HTML IDs]
  ↓
Visual Testing (T018-T020) [Can be parallel]
  ↓
Polish & Cleanup (T021-T023) [Sequential - T023 depends on all previous]
```

**Blocking Dependencies**:
- T004-T010 block T011 (HTML needs CSS classes defined)
- T011-T015 block T016 (JavaScript needs HTML IDs)
- T016-T017 block T018 (visual testing needs functional UI)
- T018-T020 block T023 (constitutional review needs complete implementation)

**Non-blocking (Parallel Opportunities)**:
- T004-T010 can all run in parallel (different CSS sections)
- T018-T020 can run in parallel (different testing methods)

---

## Parallel Execution Examples

### Example 1: CSS Component Tasks (T004-T010)
```bash
# Launch all CSS tasks together (different sections, no conflicts):
# Task 1: Light theme base styles
# Task 2: Sensor card component CSS
# Task 3: Progress bar component CSS
# Task 4: Toggle switch component CSS
# Task 5: System Controls panel CSS
# Task 6: Growth Cycle panel CSS
# Task 7: Header and footer CSS
```

### Example 2: Visual Testing Tasks (T018-T020)
```bash
# Launch visual testing tasks together:
# Task 1: Visual comparison against mockup (screenshot overlay)
# Task 2: Touch target verification (dev tools + tablet)
# Task 3: Responsive layout testing (multiple breakpoints)
```

---

## Notes

- **[P] tasks** = different files or different CSS sections, no dependencies
- **Verify tests visually** before marking tasks complete (compare against mockup)
- **Commit after each phase** (after Setup, after CSS, after HTML, etc.)
- **Avoid**: Vague tasks, same file conflicts in parallel tasks, skipping visual validation
- **Primary focus**: Principle III (UI Consistency) - must match mockup pixel-perfect
- **Zero backend changes**: All Python files in `src/` remain unchanged

---

## Task Generation Rules Applied

1. **From Spec.md (27 Functional Requirements)**:
   - Visual design (FR-001 to FR-005) → CSS tasks (T004-T010)
   - Sensor display (FR-006 to FR-010) → HTML + CSS tasks (T005, T006, T012)
   - Device controls (FR-011 to FR-014) → HTML + CSS + JS tasks (T008, T013, T016)
   - Growth cycle panel (FR-015 to FR-018) → CSS + HTML tasks (T009, T014)
   - Layout (FR-019 to FR-023) → CSS + HTML tasks (T004, T010, T012, T013)
   - Branding (FR-024 to FR-027) → Asset + HTML + CSS tasks (T001, T010, T015)

2. **From Plan.md (Design System)**:
   - Color palette → Design tokens task (T003)
   - Typography system → Design tokens task (T003)
   - Component specs → Component CSS tasks (T005-T009)
   - Layout grid → HTML restructure tasks (T012-T014)

3. **Constitutional Compliance**:
   - Principle I (Code Minimalism) → Zero backend changes, minimal file changes
   - Principle II (Zero Redundancy) → Single CSS file, design tokens
   - Principle III (UI Consistency - PRIMARY) → Visual testing tasks (T018-T020), final review (T023)
   - Principle IV (Quality Over Speed) → Visual testing before completion
   - Principle V (Clean Architecture) → Cleanup tasks (T021-T022), folder structure validation (T023)

---

## Validation Checklist

*GATE: Checked before execution*

- [x] All 27 functional requirements have corresponding implementation tasks
- [x] All CSS components have dedicated tasks (T004-T010)
- [x] All HTML sections have restructure tasks (T011-T015)
- [x] Visual testing comes after implementation (T018-T020 after T011-T017)
- [x] Parallel tasks truly independent (T004-T010 different CSS sections)
- [x] Each task specifies exact file path (all paths absolute)
- [x] No task modifies same file section as another [P] task
- [x] Constitutional compliance tasks included (T023 comprehensive review)
- [x] Quality gates addressed in polish phase (T018-T023)
- [x] Backup task included before destructive changes (T002)
- [x] Logo asset creation included (T001)
- [x] Design tokens setup included (T003)
- [x] Progress bar logic included (T017)
- [x] Touch target verification included (T019)
- [x] Responsive layout testing included (T020)
- [x] Dark theme cleanup included (T021)
- [x] Emoji removal included (T022)

---

## Execution Status

- [x] Phase 3.1: Setup (T001-T003)
- [x] Phase 3.2: CSS Redesign (T004-T010)
- [x] Phase 3.3: HTML Restructure (T011-T015)
- [x] Phase 3.4: JavaScript Updates (T016-T017)
- [~] Phase 3.5: Visual Testing (T018-T020)
- [x] Phase 3.6: Polish & Constitutional Compliance (T021-T023)

**Ready for implementation** ✓

**After execution**:
1. Perform final visual comparison against mockup (T018)
2. Validate on real tablet device (T019, T020)
3. Run constitutional compliance review (T023)
4. Merge to main branch after all checks pass
