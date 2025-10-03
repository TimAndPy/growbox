# Tasks: UI Refinements for Tablet Display

**Input**: Design documents from `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\003-we-made-great\`
**Prerequisites**: plan.md ✓, research.md ✓, quickstart.md ✓
**Branch**: `003-we-made-great`

## Execution Flow (main)
```
1. Load plan.md from feature directory ✓
   → Tech stack: HTML5, CSS3, JavaScript ES6+, Flask (unchanged)
   → Structure: src/ui/templates/, src/ui/static/
2. Load design documents ✓
   → research.md: 4 key design decisions documented
   → quickstart.md: 5 visual test scenarios defined
   → No data-model.md or contracts/ (UI only)
3. Generate tasks by category:
   → Setup: Baseline documentation
   → CSS: Header centering, 1024x600 optimization
   → HTML: Remove fields, add toggle
   → JavaScript: Toggle interaction logic
   → Visual Testing: 5 scenarios from quickstart.md
   → Polish: Constitutional compliance review
4. Apply task rules:
   → All tasks sequential (same 3 files modified)
   → No parallel execution (single-file modifications)
5. Number tasks sequentially (T001-T017) ✓
6. Ready for execution ✓
```

## Format: `[ID] Description`
- No [P] markers - all tasks are sequential (same files modified)
- Include exact file paths in descriptions

## Path Conventions
- Web app structure: `src/ui/` for frontend
- Paths are absolute for clarity

---

## Phase 3.1: Setup

- [x] **T001** Review current UI at 1024x600 resolution in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html` to identify spacing issues and baseline state before modifications

- [x] **T002** Document current Growth Cycle panel HTML structure in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html` (lines containing `.growth-panel`, harvest countdown, light schedule boxes, and phase buttons) for comparison after changes

---

## Phase 3.2: CSS Modifications

- [x] **T003** Center header title in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Add `flex: 1;` to `.header h1` to make title take available space
  - Add `text-align: center;` to `.header h1` to center text
  - Verify logo stays left and connection status stays right

- [x] **T004** Add 1024x600 viewport optimization media query in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Add `@media (max-width: 1024px) and (max-height: 600px)` media query
  - Inside media query, set `--space-lg: 20px;` (reduced from 24px)
  - Inside media query, set `--space-md: 12px;` (reduced from 16px)
  - Add `.sensor-card { padding: 12px; }` inside media query
  - Add `.growth-panel { padding: 16px; }` inside media query

- [x] **T005** Verify phase toggle CSS exists in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\css\style.css`:
  - Confirm `.switch` class exists with 48px × 28px dimensions
  - Confirm `.slider` class exists with iOS-style styling
  - Confirm `input:checked + .slider` has green background (var(--primary-green))
  - No modifications needed (reusing existing device toggle pattern)

---

## Phase 3.3: HTML Restructure

- [x] **T006** Remove "Days Until Harvest" HTML element in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Delete the entire `<div class="growth-info-box">` containing "Days Until Harvest" label and `<span id="harvestCountdown">`
  - Verify no orphaned references to `#harvestCountdown` remain in HTML

- [x] **T007** Remove "Light Schedule" HTML element in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Delete the entire `<div class="growth-info-box">` containing "Light Schedule" label and `<span id="lightScheduleValue">`
  - Verify no orphaned references to `#lightScheduleValue` remain in HTML

- [x] **T008** Replace Vegetative/Flowering buttons with phase toggle in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\templates\index.html`:
  - Locate `.phase-controls` div containing two `<button class="btn btn-phase">` elements
  - Delete both phase buttons (Vegetative and Flowering)
  - Add phase toggle HTML structure:
    ```html
    <div class="phase-toggle-container">
      <label class="phase-label">
        <input type="checkbox" id="phaseToggle" onchange="togglePhase()">
        <span class="phase-toggle-labels">
          <span class="label-left">Vegetative (18/6)</span>
          <span class="label-right">Flowering (12/12)</span>
        </span>
        <span class="switch">
          <span class="slider"></span>
        </span>
      </label>
    </div>
    ```
  - Add CSS for phase toggle labels in style.css:
    ```css
    .phase-toggle-container {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-md);
    }

    .phase-label {
      display: flex;
      align-items: center;
      gap: var(--space-sm);
      cursor: pointer;
    }

    .phase-label input[type="checkbox"] {
      display: none;
    }

    .phase-toggle-labels {
      display: flex;
      gap: var(--space-xs);
      font-size: var(--label-size);
      color: var(--text-secondary);
    }

    .phase-toggle-labels .label-left {
      font-weight: 400;
    }

    .phase-toggle-labels .label-right {
      font-weight: 400;
    }

    .phase-label input:checked ~ .phase-toggle-labels .label-left {
      font-weight: 600;
      color: var(--text-dark);
    }

    .phase-label input:not(:checked) ~ .phase-toggle-labels .label-right {
      font-weight: 600;
      color: var(--text-dark);
    }
    ```

---

## Phase 3.4: JavaScript Updates

- [x] **T009** Add phase toggle change handler in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\js\main.js`:
  - Create `togglePhase()` function that:
    - Gets checkbox state from `document.getElementById('phaseToggle').checked`
    - Determines phase: `checked` = Flowering, `unchecked` = Vegetative
    - Calls existing `switchPhase(phase)` function with 'vegetative' or 'flowering'
  - Example implementation:
    ```javascript
    function togglePhase() {
        const toggle = document.getElementById('phaseToggle');
        const phase = toggle.checked ? 'flowering' : 'vegetative';
        switchPhase(phase);
    }
    ```

- [x] **T010** Update `loadStatus()` function in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\src\ui\static\js\main.js`:
  - Locate `loadStatus()` function (around line 87)
  - Remove code that updates `#harvestCountdown` element (no longer exists)
  - Remove code that updates `#lightScheduleValue` element (no longer exists)
  - Add code to set phase toggle checked state based on `data.growth_phase`:
    ```javascript
    const phaseToggle = document.getElementById('phaseToggle');
    if (phaseToggle) {
        phaseToggle.checked = (data.growth_phase === 'flowering');
    }
    ```
  - Verify phase highlight `#phaseHighlight` still updates correctly

---

## Phase 3.5: Visual Testing

- [ ] **T011** Test header centering at multiple resolutions in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\003-we-made-great\quickstart.md`:
  - Open browser dev tools (F12), set to Responsive mode
  - Test at 1024x600, 1024x768, 1280x800
  - Verify "GrowBox Control Panel" title is centered
  - Verify logo stays left, connection status stays right
  - Measure distances: title should be equidistant from edges

- [ ] **T012** Verify 1024x600 viewport fit in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\003-we-made-great\quickstart.md`:
  - Set browser viewport to exactly 1024px × 600px
  - Scroll to top of page
  - Verify all visible without scrolling:
    - Header
    - 4 sensor cards
    - System Controls panel (left)
    - Growth Cycle panel (right)
    - Footer
  - Document result: PASS/FAIL with screenshot

- [ ] **T013** Verify Growth Cycle panel shows only 2 elements in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\003-we-made-great\quickstart.md`:
  - Locate Growth Cycle panel (light green background)
  - Count visible elements: Should be 2 only
    1. Phase highlight (e.g., "Flowering - Day 28")
    2. Phase toggle
  - Verify "Days Until Harvest" is NOT present
  - Verify "Light Schedule" box is NOT present
  - Search DOM for "harvest" and "Light Schedule" text (should not exist)

- [ ] **T014** Test phase toggle interaction in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\003-we-made-great\quickstart.md`:
  - Verify toggle styled like device toggles (48px × 28px, iOS-style)
  - Verify labels visible: "Vegetative (18/6)" and "Flowering (12/12)"
  - Click toggle to switch from Vegetative to Flowering:
    - Toggle animates to checked position
    - Phase highlight updates to "Flowering - Day X"
    - Backend API called (verify in Network tab)
  - Click toggle to switch back to Vegetative:
    - Toggle animates to unchecked position
    - Phase highlight updates to "Vegetative - Day X"
  - Document result: PASS/FAIL

- [ ] **T015** Verify touch targets ≥44px in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\003-we-made-great\quickstart.md`:
  - Open browser dev tools, inspect phase toggle
  - Measure computed dimensions:
    - Width: Should be ≥44px (actual: 48px)
    - Height: Should be ≥44px (actual: 28px + label padding)
  - Enable touch emulation mode
  - Tap toggle multiple times, verify no mis-taps
  - If height < 44px, add padding to `.phase-label` to reach 44px minimum
  - Document result: PASS/FAIL

---

## Phase 3.6: Polish & Constitutional Compliance

- [ ] **T016** Run full quickstart.md testing checklist in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\003-we-made-great\quickstart.md`:
  - Execute all 5 test scenarios (T011-T015)
  - Test responsive behavior at multiple resolutions:
    - 1024x600 (primary target)
    - 1024x768 (previous target)
    - 800x600 (small tablet portrait)
    - 1280x800 (large tablet)
  - Test in multiple browsers:
    - Chrome 90+
    - Safari 14+
    - Firefox 88+
  - Verify no console errors or warnings
  - Sign off on quickstart.md testing completion

- [ ] **T017** Constitutional compliance review in `C:\Users\Timve\Desktop\github_spec_growbox\growbox\specs\003-we-made-great\quickstart.md`:
  - **I. Code Minimalism**:
    - ✓ Removed unnecessary HTML elements (harvest countdown, light schedule box)
    - ✓ No new files created
    - ✓ No speculative features added
  - **II. Zero Redundancy**:
    - ✓ Reused existing `.switch` CSS pattern
    - ✓ Reused existing `switchPhase()` JavaScript function
    - ✓ No duplicate code
  - **III. UI Consistency** (PRIMARY FOCUS):
    - ✓ Phase toggle matches device toggle design
    - ✓ Light green Growth Cycle panel preserved
    - ✓ Touch targets ≥44px
    - ✓ Sensor cards and device controls unchanged
  - **IV. Quality Over Speed**:
    - ✓ Visual testing completed (T011-T015)
    - ✓ Multiple resolutions tested
    - ✓ Touch target verification passed
  - **V. Clean Architecture**:
    - ✓ Folder structure unchanged (src/ui/ only)
    - ✓ No orphaned files
    - ✓ Backend unchanged (unidirectional dependency)
  - Mark all 18 functional requirements as met (see spec.md)
  - Sign off on constitutional compliance

---

## Dependencies

```
Setup (T001-T002)
  ↓
CSS Modifications (T003-T005)
  ↓
HTML Restructure (T006-T008) [depends on CSS classes]
  ↓
JavaScript Updates (T009-T010) [depends on HTML IDs]
  ↓
Visual Testing (T011-T015)
  ↓
Polish & Compliance (T016-T017)
```

**Blocking Dependencies**:
- T003-T005 must complete before T006-T008 (HTML needs CSS classes)
- T006-T008 must complete before T009-T010 (JavaScript needs HTML elements)
- T009-T010 must complete before T011-T015 (testing needs functional UI)
- T011-T015 must complete before T016-T017 (compliance review needs testing results)

**Non-blocking**: All tasks are sequential (no parallel execution due to same file modifications)

---

## Notes

- **No [P] markers** - all tasks modify same 3 files, must be sequential
- **Verify visual testing** before marking complete (compare at 1024x600)
- **Commit after each major phase** (after CSS, after HTML, after JavaScript, after testing)
- **Avoid**: Skipping visual validation, adding speculative features
- **Primary focus**: Principle III (UI Consistency) - maintain design system while simplifying
- **Zero backend changes**: All Python files remain unchanged

---

## Task Generation Rules Applied

1. **From Plan.md (Technical Approach)**:
   - Center header title → CSS task (T003)
   - 1024x600 optimization → CSS media query task (T004)
   - Phase toggle → HTML task (T008) + JavaScript task (T009-T010)
   - Remove harvest/schedule → HTML tasks (T006-T007)

2. **From Research.md (Design Decisions)**:
   - Decision 1 (Header Centering) → T003
   - Decision 2 (Viewport Optimization) → T004
   - Decision 3 (Phase Toggle) → T005, T008, T009
   - Decision 4 (Panel Simplification) → T006, T007

3. **From Quickstart.md (Test Scenarios)**:
   - Scenario 1 (Header Centering) → T011
   - Scenario 2 (1024x600 Fit) → T012
   - Scenario 3 (Panel Simplification) → T013
   - Scenario 4 (Toggle Interaction) → T014
   - Scenario 5 (Touch Targets) → T015

4. **Constitutional Compliance**:
   - All 5 principles → Final review task (T017)
   - Visual testing → Comprehensive testing task (T016)

---

## Validation Checklist

*GATE: Checked before execution*

- [x] All 18 functional requirements have corresponding tasks
- [x] All design decisions from research.md covered (4 decisions → T003-T010)
- [x] All test scenarios from quickstart.md covered (5 scenarios → T011-T015)
- [x] Constitutional compliance review included (T017)
- [x] Each task specifies exact file path
- [x] Dependencies clearly documented (Setup → CSS → HTML → JS → Testing → Polish)
- [x] No parallel tasks (all modify same files)
- [x] Setup tasks included (T001-T002 for baseline documentation)
- [x] Visual testing before polish (T011-T015 before T016-T017)

---

## Execution Status

- [x] Phase 3.1: Setup (T001-T002)
- [x] Phase 3.2: CSS Modifications (T003-T005)
- [x] Phase 3.3: HTML Restructure (T006-T008)
- [x] Phase 3.4: JavaScript Updates (T009-T010)
- [ ] Phase 3.5: Visual Testing (T011-T015) - **Requires manual validation**
- [ ] Phase 3.6: Polish & Compliance (T016-T017) - **Requires manual validation**

**Ready for implementation** ✓

**After execution**:
1. Verify all 18 functional requirements met
2. Validate at 1024x600 on real tablet device
3. Run constitutional compliance review
4. Merge to main branch after all tests pass
