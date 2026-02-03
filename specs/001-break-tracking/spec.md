# Feature Specification: Break Tracking

**Feature Branch**: `001-break-tracking`
**Created**: 2026-02-03
**Status**: Draft
**Input**: User description: "Add break tracking to record when breaks are taken"

## Clarifications

### Session 2026-02-03

- Q: What preset interval options should be shown in the pop-up? → A: 5, 15, 30, 60 minutes (balanced range)
- Q: Should users be able to type a custom interval value? → A: No, presets only (simpler implementation for now)
- Q: Should the terminal prompt for interval be kept or removed? → A: Remove entirely, show interval picker in first pop-up
- Q: How should interval selection be presented in the pop-up? → A: "Continue (X min)" primary button + preset buttons (5/15/30/60) + Stop button
- Q: What should be the default interval at startup? → A: Always default to 30 minutes

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record Break Taken (Priority: P1)

As a user, when I click Continue on the break reminder pop-up, the system records that I took a break at that moment. This helps me understand my break habits over time.

**Why this priority**: This is the core functionality - without recording breaks, no tracking is possible. It delivers immediate value by capturing break data.

**Independent Test**: Can be fully tested by running the program, waiting for a reminder, clicking Continue, and verifying a break was recorded.

**Acceptance Scenarios**:

1. **Given** the break reminder pop-up is displayed, **When** the user clicks Continue or a preset interval button, **Then** the system records the current date and time as a completed break.
2. **Given** the user clicks Continue or preset buttons multiple times across a session, **When** each break is acknowledged, **Then** each break is recorded separately with its own timestamp.
3. **Given** the user clicks Cancel/Stop to exit, **When** they close the program, **Then** no break is recorded for that dismissal.

---

### User Story 2 - View Session Summary (Priority: P2)

As a user, I want to see a summary of my breaks when I stop the program so I can understand how many breaks I took during this session.

**Why this priority**: Viewing the data is the natural next step after recording it. Provides feedback that makes the tracking useful.

**Independent Test**: Can be tested by taking multiple breaks, stopping the program, and verifying a summary is displayed.

**Acceptance Scenarios**:

1. **Given** the user has taken 3 breaks during the session, **When** they click Cancel/Stop, **Then** they see a summary showing they took 3 breaks.
2. **Given** the user has taken no breaks (stopped immediately), **When** they click Cancel/Stop, **Then** they see a summary showing 0 breaks.
3. **Given** the user has taken breaks, **When** the summary is displayed, **Then** it includes the total count and the time span of the session.

---

### User Story 3 - Persist Break History (Priority: P3)

As a user, I want my break history to be saved between sessions so I can track my break habits over multiple days.

**Why this priority**: Persistence adds long-term value but requires more infrastructure. The core tracking works without it.

**Independent Test**: Can be tested by running the program, taking breaks, stopping, restarting the program, and verifying previous session data is accessible.

**Acceptance Scenarios**:

1. **Given** the user took 5 breaks yesterday, **When** they start the program today, **Then** they can access their historical break data.
2. **Given** break history exists from multiple sessions, **When** the user views history, **Then** breaks are organized by date.
3. **Given** the user runs the program for the first time, **When** no history file exists, **Then** the program creates a new history and continues normally.

---

### User Story 4 - In-Popup Interval Selection (Priority: P4)

As a user, I want to set the reminder interval directly in the pop-up dialog so I don't have to interact with the terminal.

**Why this priority**: Enhances UX by consolidating all interaction into the GUI. Builds on existing functionality.

**Independent Test**: Can be tested by starting the program, selecting an interval in the pop-up, and verifying the next reminder uses that interval.

**Acceptance Scenarios**:

1. **Given** the program starts, **When** the initial pop-up appears, **Then** I see preset interval buttons (5, 15, 30, 60 min) with 30 min as default.
2. **Given** the break reminder pop-up is displayed, **When** I click "Continue (30 min)", **Then** the break is recorded and the next reminder is set for 30 minutes.
3. **Given** the break reminder pop-up is displayed, **When** I click a different preset (e.g., 15 min), **Then** the break is recorded and the next reminder is set for 15 minutes.
4. **Given** the break reminder pop-up is displayed, **When** I click "Stop", **Then** the program shows the session summary and exits.
5. **Given** I selected 15 minutes on my last break, **When** the next pop-up appears, **Then** the "Continue" button shows "Continue (15 min)" reflecting my last choice.

---

### Edge Cases

- What happens when the history file is corrupted or unreadable? The program displays an error message and starts fresh without losing the ability to record new breaks.
- What happens when the system clock is changed during a session? Breaks are recorded with whatever the current system time shows; no validation is performed.
- What happens when disk space is full and history cannot be saved? The program displays an error message but continues running the reminder function.
- What happens if the user closes the pop-up window (X button)? Treated the same as clicking "Stop" - shows summary and exits.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST record the date and time when a user acknowledges a break by clicking a continue/interval button.
- **FR-002**: System MUST NOT record a break when the user clicks Stop.
- **FR-003**: System MUST display a session summary showing the break count when the user stops the program.
- **FR-004**: System MUST persist break history to a file so it survives program restarts.
- **FR-005**: System MUST handle missing or corrupted history files gracefully by starting fresh.
- **FR-006**: System MUST display the session duration (start time to end time) in the summary.
- **FR-007**: System MUST show interval selection in the pop-up dialog with presets: 5, 15, 30, 60 minutes.
- **FR-008**: System MUST default to 30 minutes on first start.
- **FR-009**: System MUST remember the last selected interval within the current session.
- **FR-010**: System MUST NOT require terminal input for interval selection.

### Key Entities

- **Break Record**: Represents a single break taken. Contains: timestamp (when the break was acknowledged).
- **Session**: Represents a single run of the program. Contains: start time, end time, list of break records, current interval.
- **Break History**: Collection of all sessions across multiple program runs.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can see how many breaks they took in a session within 2 seconds of stopping the program.
- **SC-002**: Break history is preserved across 100% of normal program restarts.
- **SC-003**: Users can identify their break count for any previous day in under 10 seconds.
- **SC-004**: The program continues functioning normally even when history file operations fail.
- **SC-005**: Users can select an interval and start a reminder in under 3 seconds using only the pop-up.

## Assumptions

- Break history is stored locally on the user's machine (no cloud sync).
- The history file format is human-readable for debugging purposes.
- Session summary is displayed in the terminal (output only, no input required).
- All interval selection happens via the pop-up GUI (no terminal input).
- Custom interval input may be added in a future iteration.
