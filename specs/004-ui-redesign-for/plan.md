
# Implementation Plan: UI Redesign for 1024x600 Tablet Display

**Branch**: `004-ui-redesign-for` | **Date**: 2025-10-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/004-ui-redesign-for/spec.md`

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
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 8. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
This is a pure UI/visual redesign to optimize the GrowBox Control Panel for 1024x600 tablet displays. The redesign focuses on layout restructuring: placing all sensor cards in a single horizontal row, consolidating the System Controls into a single card with an integrated Vegetative/Flowering mode toggle in the header, and removing the Growth Cycle panel. All existing functionality (sensor readings, device control toggles, light schedule modes) remains unchanged - only HTML structure and CSS styling will be modified.

## Technical Context
**Language/Version**: Python 3.x with Flask web framework
**Primary Dependencies**: Flask, Flask-SocketIO (existing web UI stack)
**Storage**: N/A (no data model changes)
**Testing**: Manual visual verification against goal mockup
**Target Platform**: 1024x600 tablet browser (fixed viewport, no scrolling)
**Project Type**: Single web application (Flask backend + HTML/CSS/JS frontend)
**Performance Goals**: No performance changes (UI-only redesign)
**Constraints**: Must fit within 1024x600 pixel viewport without scrolling
**Scale/Scope**: 3 files modified (index.html, style.css, possibly main.js for any selector updates)

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Code Minimalism**:
- [x] Feature scope is minimal and necessary (pure visual redesign, no new features)
- [x] Solution approach avoids unnecessary abstractions (CSS/HTML changes only)
- [x] Plan identifies code/resources to remove during implementation (Growth Cycle panel removal, legacy CSS cleanup)

**II. Zero Redundancy**:
- [x] No duplicate implementations planned (reusing existing components, just restructured)
- [x] Consistent naming and patterns with existing codebase (maintain current class naming conventions)
- [x] Shared logic extraction identified where applicable (consolidate duplicate CSS if found)

**III. UI Consistency**:
- [x] UI patterns consistent with existing design system (preserving current color palette, typography, spacing system)
- [x] Visual review checkpoint included in tasks (visual comparison against goal mockup required)
- [x] Interaction patterns align with current app behavior (all toggles and controls function identically)

**IV. Quality Over Speed**:
- [x] Design phase completed before implementation tasks (Phase 1 produces layout spec and visual requirements)
- [x] Test strategy validates correctness, not just coverage (visual validation at 1024x600 resolution)
- [x] Refactoring tasks identified for existing code issues (remove unused Growth Cycle CSS, clean up old layout styles)

**V. Clean Architecture**:
- [x] Folder structure is logical and matches domain (no folder changes, existing ui/ structure remains)
- [x] Each component has single, clear responsibility (HTML for structure, CSS for styling, JS for behavior unchanged)
- [x] No orphaned or unused resources will be created (explicitly removing Growth Cycle panel code)
- [x] Dependencies are unidirectional (CSS depends on HTML structure, no circular dependencies)

## Project Structure

### Documentation (this feature)
```
specs/004-ui-redesign-for/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
src/ui/
├── templates/
│   └── index.html           # Modified: restructure sensor grid, controls panel, remove growth cycle
├── static/
│   ├── css/
│   │   └── style.css        # Modified: update layout, spacing, remove growth cycle styles
│   └── js/
│       └── main.js          # Potentially modified: update selectors if IDs/classes change
└── app.py                   # Unchanged: backend API remains identical
```

**Structure Decision**: Single web application (Flask). UI redesign touches only the frontend presentation layer (HTML/CSS) within `src/ui/`. Backend Python code in `src/ui/app.py` remains completely unchanged as all existing API endpoints and data flow are preserved.

## Phase 0: Outline & Research

**Research Tasks**:
1. **Analyze Current UI Implementation**
   - Map existing HTML structure: sensor cards grid, controls panel, growth cycle panel
   - Identify all CSS classes and IDs used for current layout
   - Document current viewport media queries and responsive behavior
   - Catalog JavaScript selectors that reference UI elements

2. **CSS Grid/Flexbox Best Practices for Fixed Viewports**
   - Research optimal CSS techniques for 1024x600 fixed-size layouts
   - Review Flexbox vs CSS Grid for horizontal sensor card rows
   - Best practices for preventing content overflow in constrained viewports

3. **Visual Design System Preservation**
   - Document existing color variables (--primary-green, --light-gray, etc.)
   - Catalog current spacing system (--space-xs through --space-xl)
   - Identify typography scales currently in use
   - Ensure redesign preserves all current design tokens

**Output**: `research.md` containing:
- Complete inventory of current HTML/CSS structure
- Decision on layout technique (CSS Grid recommended for sensor cards)
- Visual design system documentation
- List of CSS classes/IDs to remove (growth cycle related)
- Selector mapping if ID/class changes required for main.js

## Phase 1: Design & Contracts

**Design Artifacts**:

1. **HTML Layout Specification** (documented in quickstart.md):
   - New sensor grid structure (4 cards, single row, equal widths)
   - System Controls card with header row layout
   - Positioning of Vegetative/Flowering toggle in controls header
   - Removal of Growth Cycle panel HTML

2. **CSS Styling Specification** (documented in quickstart.md):
   - Sensor grid: `display: grid; grid-template-columns: repeat(4, 1fr);`
   - System Controls card header: Flexbox with space-between for title/toggle
   - Updated spacing values to fit 1024x600 viewport without scrolling
   - Media query adjustments specific to 1024x600 resolution
   - Removal of `.growth-panel` and related styles

3. **Visual Validation Checklist** (documented in quickstart.md):
   - [ ] All 4 sensor cards visible in single horizontal row at 1024x600
   - [ ] System Controls displays with header containing "System Controls" + mode toggle
   - [ ] Growth Cycle panel completely removed
   - [ ] Footer "Powered by Squad Apps" retained
   - [ ] No horizontal or vertical scrolling required
   - [ ] Current icons preserved (no icon changes)
   - [ ] Color scheme unchanged (white cards, gray background)

4. **Update agent file** (CLAUDE.md):
   - Run: `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
   - Add: UI redesign context (HTML/CSS modification scope)
   - Update recent changes

**Output**:
- `quickstart.md` with layout specifications and visual validation checklist
- `CLAUDE.md` updated with UI redesign context

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
1. **Preparation Tasks**:
   - Create backup of current index.html and style.css
   - Document current layout screenshots at 1024x600

2. **HTML Restructuring Tasks**:
   - Restructure sensor cards grid (ensure 4-column layout)
   - Consolidate System Controls panel with header row
   - Add Vegetative/Flowering toggle to controls header
   - Remove Growth Cycle panel HTML entirely
   - Verify footer preserved

3. **CSS Styling Tasks**:
   - Update sensor grid CSS for single-row layout
   - Style System Controls header with title + toggle positioning
   - Remove all growth cycle CSS (.growth-panel, .growth-phase-highlight, etc.)
   - Adjust spacing for 1024x600 viewport fit
   - Update/remove media queries as needed

4. **JavaScript Selector Updates** (if needed):
   - Update any JavaScript selectors affected by HTML changes
   - Verify toggle event handlers still function

5. **Visual Validation Tasks**:
   - Test at exact 1024x600 resolution
   - Verify against goal mockup (UIGoal.png)
   - Check all interactive elements (toggles, buttons)
   - Confirm no scrolling required

6. **Cleanup Tasks**:
   - Remove unused CSS classes and IDs
   - Delete commented-out code
   - Verify no orphaned assets

**Ordering Strategy**:
- Sequential execution (HTML before CSS before JS validation)
- Backup task first to enable easy rollback
- Visual validation after each major change
- Cleanup tasks last

**Estimated Output**: 12-15 ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (visual comparison against UIGoal.png at 1024x600 resolution)

## Complexity Tracking
*No constitutional violations - this section intentionally left empty.*

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) - research.md created
- [x] Phase 1: Design complete (/plan command) - quickstart.md created, CLAUDE.md updated
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [x] Phase 3: Tasks generated (/tasks command) - tasks.md created with 33 ordered tasks
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved (via /clarify command)
- [x] Complexity deviations documented (none required)

**Artifacts Generated**:
- [x] specs/004-ui-redesign-for/plan.md (this file)
- [x] specs/004-ui-redesign-for/research.md (current UI analysis, design decisions)
- [x] specs/004-ui-redesign-for/quickstart.md (layout specs, validation checklist)
- [x] specs/004-ui-redesign-for/tasks.md (33 ordered implementation tasks)
- [x] CLAUDE.md (agent context updated)

---
*Based on Constitution v1.0.0 - See `.specify/memory/constitution.md`*
