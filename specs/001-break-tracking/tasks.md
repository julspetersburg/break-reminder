# Tasks: Break Tracking

**Input**: Design documents from `/specs/001-break-tracking/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, research.md, quickstart.md

**Tests**: Not requested in feature specification. Manual testing per constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: Single `main.py` file at repository root
- **Storage**: `~/.break_reminder/history.json` created at runtime

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Define constants and imports needed for tracking functionality

- [x] T001 Add required imports (json, datetime, pathlib) to main.py
- [x] T002 Add constant HISTORY_DIR for ~/.break_reminder path in main.py
- [x] T003 Add constant HISTORY_FILE for history.json path in main.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core file I/O and data structure functions that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement `get_history_path()` function to return cross-platform path to history.json in main.py
- [x] T005 Implement `load_history()` function to read JSON file and return dict (empty sessions list if missing/corrupted) in main.py
- [x] T006 Implement `save_history()` function to write dict to JSON file with error handling in main.py
- [x] T007 Implement `create_session()` function to return new session dict with start time in main.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Record Break Taken (Priority: P1) 🎯 MVP

**Goal**: When user clicks OK, record the current timestamp as a break

**Independent Test**: Run program, wait for reminder, click OK, verify break timestamp appears in history.json

### Implementation for User Story 1

- [x] T008 [US1] Add `current_session` variable to track active session in main() in main.py
- [x] T009 [US1] Initialize session with `create_session()` at program start in main.py
- [x] T010 [US1] Implement `record_break()` function to append current timestamp to session breaks list in main.py
- [x] T011 [US1] Call `record_break()` when user clicks OK (result is True) in main loop in main.py

**Checkpoint**: User Story 1 complete - breaks are recorded with timestamps during session

---

## Phase 4: User Story 2 - View Session Summary (Priority: P2)

**Goal**: When user stops the program, display break count and session duration

**Independent Test**: Take 3 breaks, click Cancel, verify summary shows "3 breaks" and session duration

### Implementation for User Story 2

- [x] T012 [US2] Implement `format_duration()` function to convert seconds to human-readable format in main.py
- [x] T013 [US2] Implement `show_session_summary()` function to print break count and duration to terminal in main.py
- [x] T014 [US2] Set session end time when user clicks Cancel in main.py
- [x] T015 [US2] Call `show_session_summary()` before program exits in main.py

**Checkpoint**: User Story 2 complete - session summary displayed on exit

---

## Phase 5: User Story 3 - Persist Break History (Priority: P3)

**Goal**: Save sessions to file and show history summary at startup

**Independent Test**: Take breaks, stop, restart program, verify previous session data is shown

### Implementation for User Story 3

- [x] T016 [US3] Implement `show_history_summary()` function to display break counts by date in main.py
- [x] T017 [US3] Call `load_history()` at program start and display summary in main.py
- [x] T018 [US3] Implement `add_session_to_history()` function to append completed session to history in main.py
- [x] T019 [US3] Call `add_session_to_history()` and `save_history()` when session ends in main.py

**Checkpoint**: User Story 3 complete - history persists across program restarts

---

## Phase 6: User Story 4 - In-Popup Interval Selection (Priority: P4)

**Goal**: Replace terminal-based interval input with preset buttons in the pop-up dialog

**Independent Test**: Start program, select interval via pop-up buttons, verify timer uses selected interval

### Setup for User Story 4

- [x] T024 [US4] Add PRESET_INTERVALS constant [5, 15, 30, 60] to main.py
- [x] T025 [US4] Add DEFAULT_INTERVAL constant (30) to main.py

### Implementation for User Story 4

- [x] T026 [US4] Implement `show_interval_dialog()` function using tkinter.Toplevel with:
  - Title label "Time for a break!"
  - Continue button showing current interval
  - Preset buttons (5, 15, 30, 60 min)
  - Stop button
  - Returns tuple (action, interval) where action is "continue" or "stop"
- [x] T027 [US4] Add window close (X button) handler to treat as "stop" action
- [x] T028 [US4] Replace initial `get_minutes_with_default()` call with `show_interval_dialog()` at startup
- [x] T029 [US4] Replace `messagebox.askokcancel()` in main loop with `show_interval_dialog()`
- [x] T030 [US4] Remove the `get_minutes_with_default()` function (no longer needed)
- [x] T031 [US4] Track current interval across dialog calls (remember last selection)

**Checkpoint**: User Story 4 complete - all interval selection happens in pop-up dialog

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and documentation

- [x] T020 Add docstrings to all new functions in main.py
- [x] T021 Update README.md with break tracking feature description
- [x] T022 Run quickstart.md validation - verify all documented scenarios work
- [x] T023 Handle edge case: corrupted history file (print warning, start fresh) in main.py
- [x] T032 [US4] Add docstring to show_interval_dialog() function
- [x] T033 [US4] Update README.md with in-popup interval selection feature

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - records breaks in memory
- **User Story 2 (Phase 4)**: Depends on US1 - needs session data to summarize
- **User Story 3 (Phase 5)**: Depends on US2 - saves completed sessions to file
- **User Story 4 (Phase 6)**: Depends on US3 - enhances UI for complete workflow
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Depends on US1 (needs session with breaks to summarize)
- **User Story 3 (P3)**: Depends on US2 (needs completed session to persist)
- **User Story 4 (P4)**: Depends on US3 (enhances existing workflow with GUI interval selection)

Note: Unlike typical features, these stories have sequential dependencies because they build on each other (record → summarize → persist → enhance UI).

### Within Each User Story

- Core data structure before display logic
- In-memory operations before file operations
- Story complete before moving to next priority

### Parallel Opportunities

- T001, T002, T003 can run in parallel (all add to top of file)
- T004, T005, T006, T007 are sequential (each builds on prior)
- Within US1: T008, T009 before T010, T011
- Within US2: T012 parallel with T014, then T013, T15
- Within US3: T016 parallel with T18, then T017, T19

---

## Parallel Example: Phase 1 Setup

```bash
# Launch all setup tasks together:
Task: "Add required imports (json, datetime, pathlib) to main.py"
Task: "Add constant HISTORY_DIR for ~/.break_reminder path in main.py"
Task: "Add constant HISTORY_FILE for history.json path in main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T007)
3. Complete Phase 3: User Story 1 (T008-T011)
4. **STOP and VALIDATE**: Run program, take breaks, verify timestamps in session
5. Breaks are tracked in memory (MVP complete)

### Incremental Delivery

1. Setup + Foundational → Core functions ready
2. Add User Story 1 → Breaks recorded in memory (MVP!)
3. Add User Story 2 → User sees summary on exit
4. Add User Story 3 → History persists across runs (Feature complete!)
5. Polish → Documentation and edge cases handled

### Single Developer Strategy

Since this is a beginner project with sequential dependencies:

1. Complete phases in order: Setup → Foundational → US1 → US2 → US3 → Polish
2. Test manually after each user story checkpoint
3. Commit after each phase completion

---

## Notes

- All tasks modify the single `main.py` file
- No separate module files needed (per constitution: Simplicity First)
- Manual testing sufficient (per constitution: Working Code)
- History file created automatically on first save
- All timestamps use ISO 8601 format for consistency
