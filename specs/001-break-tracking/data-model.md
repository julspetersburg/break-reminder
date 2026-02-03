# Data Model: Break Tracking

**Feature**: 001-break-tracking
**Date**: 2026-02-03

## Entities

### BreakRecord

Represents a single acknowledged break.

| Field | Type | Description |
|-------|------|-------------|
| timestamp | ISO 8601 string | When the user clicked a continue/interval button |

**Validation Rules**:
- Timestamp must be a valid ISO 8601 datetime string
- Timestamp must be within the parent session's time range

**Example**:
```json
"2026-02-03T14:30:00"
```

Note: In JSON, break records are stored as simple strings (timestamps) for simplicity.

---

### Session

Represents a single program run from start to stop.

| Field | Type | Description |
|-------|------|-------------|
| start | ISO 8601 string | When the program started |
| end | ISO 8601 string | When the user stopped the program |
| breaks | array of strings | List of break timestamps |

**Validation Rules**:
- `start` must be earlier than `end`
- All `breaks` timestamps must be between `start` and `end`
- `breaks` array can be empty (user stopped immediately)

**State Transitions**:
1. **Created**: Session starts when program runs, `start` is set, `end` is null
2. **Active**: User takes breaks, timestamps added to `breaks` array
3. **Completed**: User stops program, `end` is set, session saved to history

**Example**:
```json
{
  "start": "2026-02-03T09:00:00",
  "end": "2026-02-03T17:30:00",
  "breaks": [
    "2026-02-03T09:30:00",
    "2026-02-03T10:00:00",
    "2026-02-03T10:30:00"
  ]
}
```

---

### BreakHistory

The root entity containing all sessions across program runs.

| Field | Type | Description |
|-------|------|-------------|
| sessions | array of Session | All recorded sessions, oldest first |

**Validation Rules**:
- `sessions` array can be empty (first run)
- Sessions should be ordered by start time (ascending)
- No overlapping sessions (one program run at a time)

**Example**:
```json
{
  "sessions": [
    {
      "start": "2026-02-02T09:00:00",
      "end": "2026-02-02T17:00:00",
      "breaks": ["2026-02-02T09:30:00", "2026-02-02T10:00:00"]
    },
    {
      "start": "2026-02-03T09:00:00",
      "end": "2026-02-03T17:30:00",
      "breaks": ["2026-02-03T09:30:00"]
    }
  ]
}
```

---

## Runtime State (In-Memory Only)

### DialogResult

Result from the interval selection dialog (not persisted).

| Field | Type | Description |
|-------|------|-------------|
| action | string | One of: "continue", "stop" |
| interval | int | Selected interval in minutes (5, 15, 30, or 60) |

**Actions**:
- `"continue"`: User wants to continue with the selected interval
- `"stop"`: User clicked Stop or closed the window

**Example**:
```python
("continue", 30)  # User clicked Continue or 30 min preset
("stop", 30)      # User clicked Stop (interval value ignored)
```

---

### IntervalState

Current interval tracking within a session (in-memory only).

| Field | Type | Description |
|-------|------|-------------|
| current_interval | int | Currently selected interval in minutes |

**Default**: 30 minutes

**Behavior**:
- Updated when user selects a different preset
- Persisted only within the current session
- Resets to 30 minutes on next program start

---

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| PRESET_INTERVALS | [5, 15, 30, 60] | Available interval presets in minutes |
| DEFAULT_INTERVAL | 30 | Default interval on first start |

---

## Relationships

```text
BreakHistory (1) ──contains──> (*) Session
Session (1) ──contains──> (*) BreakRecord
```

- One BreakHistory file per user
- One Session per program run
- Zero or more BreakRecords per Session

---

## File Storage

**Location**: `~/.break_reminder/history.json`

**File Structure**:
```text
~/.break_reminder/
└── history.json    # Contains BreakHistory JSON
```

**Initialization**:
- Directory created if missing
- Empty history (`{"sessions": []}`) created if file missing
- Corrupted file replaced with empty history (with warning message)
