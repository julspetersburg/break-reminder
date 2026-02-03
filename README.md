# Break Reminder

A simple Python program that shows a pop-up reminder every so often to help you take regular breaks.

## Features

- **In-popup interval selection**: Choose your reminder interval directly in the pop-up (5, 15, 30, or 60 minutes)
- **Break tracking**: Records when you take breaks
- **Session summary**: Shows how many breaks you took when you stop
- **History persistence**: Your break history is saved between sessions

## Requirements

- Python 3.8 or higher
- tkinter (included with most Python installations)

## Usage

```bash
python main.py
```

### How it works

1. **Startup**: The program shows your break history, then displays an interval selection dialog
   - Click **Continue (30 min)** to start with the default interval
   - Click a preset button (5, 15, 30, or 60 min) to use a different interval
   - Click **Stop** to exit without starting a session

2. **During session**: A pop-up appears when it's time for a break
   - Click **Continue (X min)** to record the break and continue with the same interval
   - Click a preset button to record the break AND change the interval for the next reminder
   - Click **Stop** (or close the window) to end the session

3. **On exit**: A summary shows your session duration and breaks taken

### Example session

```text
$ python main.py

=== Break History ===
Yesterday: 5 breaks
Today: 2 breaks

[Dialog: "Time for a break!" with Continue/presets/Stop buttons]
> Click "15 min" button

[Timer starts: 15 minutes]

[Dialog appears after 15 minutes]
> Click "Continue (15 min)"

[Break recorded, timer restarts: 15 minutes]

[Dialog appears after 15 minutes]
> Click "Stop"

=== Session Summary ===
Session duration: 30 minutes
Breaks taken: 1
Session saved to history.
```

## Data Storage

Your break history is stored at:
- **Linux/macOS**: `~/.break_reminder/history.json`
- **Windows**: `C:\Users\<username>\.break_reminder\history.json`

The file is human-readable JSON and can be manually edited if needed.

## Troubleshooting

### Pop-up not appearing
- Check if another window is blocking it
- Look for the window in your taskbar

### Program won't start
- Verify Python 3.8+ is installed: `python --version`
- Check tkinter is available: `python -c "import tkinter"`
- On Linux, install tkinter if needed: `sudo apt install python3-tk`
