# Quickstart: Break Tracking

**Feature**: 001-break-tracking
**Date**: 2026-02-03

## Prerequisites

- Python 3.8 or higher
- tkinter (included with most Python installations)

## Installation

No installation needed - the program is a single Python file.

```bash
# Clone or download the repository
cd break-reminder

# Run the program
python main.py
```

## Basic Usage

### Starting a Session

1. Run `python main.py`
2. Your break history is shown in the terminal
3. A pop-up dialog appears with interval options
4. Click an interval button (5, 15, 30, or 60 min) to start the timer
5. The default is 30 minutes - click "Continue (30 min)" to use it

### Dialog Layout

```
┌──────────────────────────────────┐
│        Time for a break!         │
├──────────────────────────────────┤
│    [ Continue (30 min) ]         │  ← Click to use current interval
├──────────────────────────────────┤
│  [5 min] [15 min] [30 min] [60 min]  ← Click to change interval
├──────────────────────────────────┤
│          [ Stop ]                │  ← Click to end session
└──────────────────────────────────┘
```

### Taking Breaks

1. When a pop-up appears saying "Time for a break!"
2. Click **Continue (X min)** to record the break and use the same interval
3. Or click a preset button (5/15/30/60) to record the break AND change the next interval
4. Continue working until the next reminder

### Ending a Session

1. When a pop-up appears, click **Stop** (or close the window with X)
2. A summary appears in the terminal showing:
   - Number of breaks taken
   - Session duration
3. The session is saved to your break history

## Viewing History

At program start, you'll see a summary of your previous sessions:

```text
=== Break History ===
Yesterday: 5 breaks
Today: 2 breaks
```

## File Location

Your break history is stored at:
- **Linux/macOS**: `~/.break_reminder/history.json`
- **Windows**: `C:\Users\<username>\.break_reminder\history.json`

The file is human-readable JSON and can be manually edited if needed.

## Troubleshooting

### "History file corrupted" message

The program detected invalid data in the history file. It will:
1. Show a warning message
2. Create a new empty history
3. Continue running normally

Your old history file is not automatically backed up - if you need the data, check the file before running the program again.

### Pop-up not appearing

- Make sure no other window is blocking it
- On some systems, the pop-up may appear behind other windows
- Check your taskbar for the "Break Reminder" window

### Program won't start

- Ensure Python 3.8+ is installed: `python --version`
- Ensure tkinter is available: `python -c "import tkinter"`
- On Linux, you may need to install tkinter: `sudo apt install python3-tk`

## Example Session

```text
$ python main.py

=== Break History ===
No previous sessions found.

[Dialog appears - "Time for a break!"]
> User clicks "15 min" preset button

[Timer starts: 15 minutes]
[Dialog appears after 15 minutes]
> User clicks "Continue (15 min)"

[Break recorded, timer restarts: 15 minutes]
[Dialog appears after 15 minutes]
> User clicks "30 min" preset button

[Break recorded, timer restarts: 30 minutes]
[Dialog appears after 30 minutes]
> User clicks "Stop"

=== Session Summary ===
Session duration: 1 hour
Breaks taken: 3
Session saved to history.
```

## Interval Presets

| Button | Interval |
|--------|----------|
| 5 min | 5 minutes (quick check-in) |
| 15 min | 15 minutes (short focus) |
| 30 min | 30 minutes (standard, default) |
| 60 min | 60 minutes (deep work) |

The "Continue" button always shows the current interval and is the quickest way to continue with the same setting.
