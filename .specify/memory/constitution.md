<!--
SYNC IMPACT REPORT
Version Change: none → 1.0.0
Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (5 principles: Code Minimalism, Zero Redundancy, UI Consistency, Quality Over Speed, Clean Architecture)
  - Development Standards
  - Quality Gates
  - Governance
Removed Sections: N/A
Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md (Updated Constitution Check section with all 5 principles as checkable gates)
  ✅ .specify/templates/spec-template.md (No changes required - remains implementation-agnostic)
  ✅ .specify/templates/tasks-template.md (Added constitutional compliance tasks to Polish phase; updated validation checklist)
  ✅ .specify/templates/agent-file-template.md (No changes required - generic template)
Follow-up TODOs: None
-->

# GrowBox Constitution

## Core Principles

### I. Code Minimalism
Every line of code must justify its existence. The codebase MUST remain lean and purposeful.

**Rules**:
- Write only what is needed to meet requirements—no speculative features
- Delete unused code, commented-out blocks, and dead imports immediately
- Prefer simple solutions over clever abstractions
- One clear way to do each thing (avoid multiple similar implementations)

**Rationale**: Minimal code reduces cognitive load, bugs, and maintenance burden. Unused code creates confusion and technical debt.

### II. Zero Redundancy
Duplicate code and inconsistent patterns are strictly prohibited.

**Rules**:
- DRY (Don't Repeat Yourself) is non-negotiable—extract shared logic immediately
- Use consistent naming conventions throughout the entire codebase
- Establish and follow uniform code patterns (same pattern for same problem)
- Refactor duplicates found during code review before merging
- No copy-paste programming—always extract reusable components

**Rationale**: Redundancy causes maintenance nightmares, inconsistent behavior, and bug multiplication. Consistency enables faster comprehension and reduces errors.

### III. UI Consistency (NON-NEGOTIABLE)
User interface MUST be visually and behaviorally consistent across all screens and components.

**Rules**:
- All UI implementations MUST be reviewed for consistency before completion
- Establish design system (colors, spacing, typography, components) and enforce strictly
- Same user action must behave identically everywhere
- Visual hierarchy and layout patterns must remain uniform
- No mix of design patterns (e.g., don't combine material + custom styles arbitrarily)

**Rationale**: Inconsistent UI destroys user trust, creates confusion, and signals poor quality. Users judge the entire application by its visual consistency.

### IV. Quality Over Speed
Correctness and maintainability take precedence over development velocity.

**Rules**:
- Take time to understand requirements fully before coding
- Design before implementing—no "code first, think later"
- Write tests that validate correctness, not just coverage
- Refactor immediately when code smells are detected
- Review and improve existing code during feature work
- Never ship knowingly broken or poorly designed code

**Rationale**: Rushing creates technical debt that compounds exponentially. Time spent on quality design saves multiples in debugging and refactoring.

### V. Clean Architecture
Code organization must be logical, discoverable, and maintainable.

**Rules**:
- Clear folder structure that matches domain concepts (no "misc" or "utils" dumping grounds)
- Each file has single, well-defined responsibility
- Remove empty folders and unused resources immediately
- Logical grouping by feature/domain, not by technical layer alone
- Dependencies flow in one direction (no circular dependencies)
- No orphaned files—every file must be reachable from entry points

**Rationale**: Messy structure makes code undiscoverable and unmaintainable. Clean architecture enables rapid navigation and prevents structural decay.

## Development Standards

**Code Review Requirements**:
- Every PR must verify: no duplicate code, no unused resources, UI consistency, clean structure
- Reviewers MUST reject PRs that violate constitutional principles
- Changes that touch UI require visual consistency verification (screenshots/video)

**Refactoring Policy**:
- Continuous improvement is mandatory—refactor during feature work when issues found
- Create dedicated refactoring tasks when major restructuring needed
- Never accumulate "we'll fix it later" technical debt

**Testing Standards**:
- Tests must validate behavior correctness, not implementation details
- UI tests must verify visual consistency (snapshot/visual regression)
- Quality of tests matters more than quantity of tests

## Quality Gates

**Before Any Commit**:
- [ ] No unused imports, variables, or files
- [ ] No commented-out code blocks
- [ ] No duplicate logic or redundant patterns
- [ ] Folder structure is clean and logical

**Before Marking UI Tasks Complete**:
- [ ] Visual consistency verified across all affected screens
- [ ] Design system followed (colors, spacing, typography)
- [ ] Interaction patterns consistent with existing UI
- [ ] Responsive behavior tested (if applicable)

**Before PR Merge**:
- [ ] All quality gates passed
- [ ] Code review confirms constitutional compliance
- [ ] No new technical debt introduced
- [ ] Documentation updated if behavior changed

## Governance

**Amendment Process**:
1. Propose change with rationale and impact analysis
2. Document in constitution with version bump
3. Update all dependent templates and documentation
4. Communicate to all contributors

**Versioning**:
- MAJOR: Principle removal or fundamental redefinition
- MINOR: New principle or significant expansion
- PATCH: Clarifications, wording improvements

**Compliance**:
- All PRs must reference this constitution
- Violations must be justified in Complexity Tracking (plan.md)
- Repeated violations require architecture review
- Constitution supersedes convenience

**Constitutional Authority**:
- These principles are binding on all development work
- Exceptions require explicit documentation and justification
- When in doubt, favor quality and consistency over speed

**Version**: 1.0.0 | **Ratified**: 2025-10-03 | **Last Amended**: 2025-10-03
