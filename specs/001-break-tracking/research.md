# Research: Break Tracking

**Feature**: 001-break-tracking
**Date**: 2026-02-03

## Overview

This document captures technical decisions for the break tracking feature. All choices prioritize Constitution Principle I (Simplicity First) by using built-in Python libraries.

## Decision 1: Storage Format

**Decision**: JSON file format

**Rationale**:
- Human-readable (spec assumption)
- Python's `json` module is built-in (no external dependencies)
- Easy to debug and manually inspect
- Sufficient for expected scale (~1000 records)

**Alternatives Considered**:
- SQLite: More complex, overkill for this scale
- CSV: Less structured, harder to represent nested data (sessions containing breaks)
- Plain text: Harder to parse reliably

## Decision 2: File Location

**Decision**: User's home directory (`~/.break_reminder/history.json`)

**Rationale**:
- Cross-platform compatible (pathlib handles path differences)
- Doesn't require write permissions in program directory
- Standard location for user data
- Hidden directory (dot prefix) keeps it out of the way

**Alternatives Considered**:
- Same directory as script: May not have write permissions
- Temp directory: Data would be lost on reboot
- AppData/Library paths: Platform-specific, more complex

## Decision 3: Date/Time Handling

**Decision**: ISO 8601 format strings (`2026-02-03T14:30:00`)

**Rationale**:
- Human-readable in JSON file
- Sortable as strings
- Standard format, widely understood
- Python's `datetime.fromisoformat()` parses it directly

**Alternatives Considered**:
- Unix timestamps: Less readable, requires conversion
- Custom format: Non-standard, error-prone

## Decision 4: Error Handling Strategy

**Decision**: Fail gracefully and continue

**Rationale**:
- Core reminder functionality must not break due to tracking issues
- User should see error messages but program continues
- Missing/corrupted history starts fresh (per spec FR-005)

**Approach**:
1. Wrap file operations in try/except
2. Print clear error message to terminal
3. Initialize empty history and continue
4. Never crash the reminder loop due to tracking errors

## Decision 5: Session Boundary

**Decision**: One session = one program run

**Rationale**:
- Simple to implement (session starts at program start, ends at program stop)
- Matches user mental model
- Clear boundary for summary display

**Data captured per session**:
- Start timestamp (when program starts)
- End timestamp (when user stops)
- List of break timestamps

---

## User Story 4: In-Popup Interval Selection

### Decision 6: Custom Dialog Implementation

**Decision**: Use `tkinter.Toplevel` with `tk.Button` widgets

**Rationale**:
- `messagebox` functions (askokcancel, etc.) don't support custom buttons
- `Toplevel` creates a new window that can contain any widgets
- `tk.Button` allows labeled buttons with custom callbacks
- All built-in to tkinter - no external dependencies

**Alternatives Considered**:
- `simpledialog.askinteger()`: Only returns a number, no preset buttons
- Third-party dialog libraries (PySimpleGUI, etc.): Violates Constitution Principle I
- Custom Tk class: Overcomplicated for this use case

### Decision 7: Dialog Layout

**Decision**: Vertical layout with button groups

**Layout**:
```
┌──────────────────────────────────┐
│        Time for a break!         │
├──────────────────────────────────┤
│    [ Continue (30 min) ]         │  ← Primary action, shows current interval
├──────────────────────────────────┤
│  [5 min] [15 min] [30 min] [60 min]  ← Preset buttons in a row
├──────────────────────────────────┤
│          [ Stop ]                │  ← Secondary action
└──────────────────────────────────┘
```

**Rationale**:
- "Continue" is most common action, placed prominently at top
- Preset buttons offer quick access to change interval
- "Stop" separated at bottom to prevent accidental clicks
- Follows standard dialog conventions

### Decision 8: Return Value Pattern

**Decision**: Return tuple `(action, interval)` from dialog function

**Rationale**:
- Clear distinction between user actions
- `action` is one of: "continue", "stop", "preset"
- `interval` is the selected minutes (int)
- Allows main loop to handle each case appropriately

**Pattern**:
```python
action, interval = show_interval_dialog(root, current_interval)
if action == "stop":
    break  # Exit loop
# Otherwise continue with new interval
```

### Decision 9: Window Close Handling (X Button)

**Decision**: Treat window close as "Stop"

**Rationale**:
- Matches spec edge case requirement
- Prevents undefined behavior
- Use `protocol("WM_DELETE_WINDOW", ...)` to intercept close
- Consistent UX - closing window = ending program

### Decision 10: Initial Startup Dialog

**Decision**: Show interval selection dialog immediately at startup

**Rationale**:
- Replaces terminal input completely (per clarification)
- First dialog is identical to break reminder dialog
- Shows preset options with 30 min as default
- User can start timer immediately or change interval

**Flow**:
1. Program starts
2. Show history summary (terminal output)
3. Show interval dialog (user selects interval)
4. Start timer with selected interval
5. Loop: timer → dialog → record break → repeat

## Technical Notes

### JSON Schema (informal)

```json
{
  "sessions": [
    {
      "start": "2026-02-03T09:00:00",
      "end": "2026-02-03T17:00:00",
      "breaks": [
        "2026-02-03T09:30:00",
        "2026-02-03T10:00:00"
      ]
    }
  ]
}
```

### Key Python Modules

- `json`: Read/write history file
- `datetime`: Timestamps and formatting
- `pathlib`: Cross-platform file paths
- `tkinter`: GUI dialogs (Tk, Toplevel, Button, Label, Frame)

All modules are part of Python standard library - no pip installs required.

### Preset Intervals Constant

```python
PRESET_INTERVALS = [5, 15, 30, 60]  # minutes
DEFAULT_INTERVAL = 30  # minutes
```
