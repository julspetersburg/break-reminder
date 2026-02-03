# Implementation Plan: In-Popup Interval Selection (User Story 4)

**Branch**: `001-break-tracking` | **Date**: 2026-02-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-break-tracking/spec.md`

**Note**: This plan covers User Story 4 only. User Stories 1-3 are already implemented.

## Summary

Replace the terminal-based interval input with an in-popup interval selector. The custom tkinter dialog will show preset interval buttons (5, 15, 30, 60 min), a "Continue" button showing the current interval, and a "Stop" button. This eliminates the need for terminal interaction after starting the program.

## Technical Context

**Language/Version**: Python 3.8+ (type hints, pathlib)
**Primary Dependencies**: tkinter (built-in) - requires custom Toplevel dialog instead of messagebox
**Storage**: Local JSON file (`~/.break_reminder/history.json`) - unchanged
**Testing**: Manual testing (per constitution)
**Target Platform**: Cross-platform desktop (Windows, macOS, Linux)
**Project Type**: Single project (single main.py file)
**Performance Goals**: Instant response (<100ms for all operations)
**Constraints**: No external dependencies; built-in tkinter only
**Scale/Scope**: Single user, local storage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Simplicity First | Use built-in libraries | ✅ PASS | tkinter Toplevel is built-in |
| I. Simplicity First | Single-purpose functions | ✅ PASS | New dialog function has one job |
| I. Simplicity First | Clear variable names | ✅ PASS | `show_interval_dialog()`, `selected_interval` |
| II. Working Code | Handle errors gracefully | ✅ PASS | Window close (X) treated as Stop |
| II. Working Code | No silent crashes | ✅ PASS | All user actions have defined behavior |
| II. Working Code | Testable by running | ✅ PASS | Can verify by clicking buttons |
| III. Clear Intent | Comments explain "why" | ✅ PASS | Will document dialog structure |
| III. Clear Intent | No magic numbers | ✅ PASS | PRESET_INTERVALS constant |

**Gate Result**: ✅ PASS - All constitution principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-break-tracking/
├── plan.md              # This file (updated for US4)
├── research.md          # Phase 0 output (updated for US4)
├── data-model.md        # Phase 1 output (updated for US4)
├── quickstart.md        # Phase 1 output (updated for US4)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
main.py                  # Existing file - will be modified
```

**Structure Decision**: Keep single-file structure (Constitution Principle I). Add custom dialog function to existing main.py.

## Key Changes from Current Implementation

| Current | New (US4) |
|---------|-----------|
| `messagebox.askokcancel()` | Custom `Toplevel` dialog with buttons |
| Terminal input for interval | Preset buttons in dialog |
| `get_minutes_with_default()` | `show_interval_dialog()` |
| OK/Cancel buttons | Continue (X min) / 5 / 15 / 30 / 60 / Stop buttons |

## Complexity Tracking

> No violations - design passes all constitution checks without justification needed.
