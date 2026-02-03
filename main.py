"""Break reminder: shows a pop-up every N minutes until you click Stop."""

import json
from datetime import datetime, timedelta
from pathlib import Path

import tkinter as tk

# Path to break history storage
HISTORY_DIR = Path.home() / ".break_reminder"
HISTORY_FILE = HISTORY_DIR / "history.json"

# Interval presets for break reminders (in minutes)
PRESET_INTERVALS = [5, 15, 30, 60]
DEFAULT_INTERVAL = 30


def get_history_path() -> Path:
    """Return the cross-platform path to the history file."""
    return HISTORY_FILE


def load_history() -> dict:
    """Load break history from JSON file.

    Returns an empty history if file is missing or corrupted.
    """
    history_path = get_history_path()
    if not history_path.exists():
        return {"sessions": []}
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Basic validation: ensure sessions key exists
            if "sessions" not in data:
                print("Warning: History file missing 'sessions' key. Starting fresh.")
                return {"sessions": []}
            return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Could not read history file ({e}). Starting fresh.")
        return {"sessions": []}


def save_history(history: dict) -> bool:
    """Save break history to JSON file.

    Creates the directory if it doesn't exist.
    Returns True on success, False on failure.
    """
    history_path = get_history_path()
    try:
        # Create directory if needed
        history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
        return True
    except OSError as e:
        print(f"Warning: Could not save history ({e}). Data may be lost.")
        return False


def create_session() -> dict:
    """Create a new session with the current start time."""
    return {
        "start": datetime.now().isoformat(timespec="seconds"),
        "end": None,
        "breaks": []
    }


def record_break(session: dict) -> None:
    """Record the current time as a break in the session."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    session["breaks"].append(timestamp)


def format_duration(seconds: int) -> str:
    """Convert seconds to a human-readable duration string."""
    if seconds < 60:
        return f"{seconds} seconds"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes == 0:
        return f"{hours} hour{'s' if hours != 1 else ''}"
    return f"{hours} hour{'s' if hours != 1 else ''} {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"


def show_session_summary(session: dict) -> None:
    """Display a summary of the session to the terminal."""
    break_count = len(session["breaks"])
    start_time = datetime.fromisoformat(session["start"])
    end_time = datetime.fromisoformat(session["end"])
    duration_seconds = int((end_time - start_time).total_seconds())

    print("\n=== Session Summary ===")
    print(f"Session duration: {format_duration(duration_seconds)}")
    print(f"Breaks taken: {break_count}")


def show_history_summary(history: dict) -> None:
    """Display break counts organized by date."""
    sessions = history.get("sessions", [])
    if not sessions:
        print("\n=== Break History ===")
        print("No previous sessions found.")
        return

    # Group breaks by date
    breaks_by_date: dict[str, int] = {}
    for session in sessions:
        for break_time in session.get("breaks", []):
            date_str = break_time[:10]  # Extract YYYY-MM-DD from ISO format
            breaks_by_date[date_str] = breaks_by_date.get(date_str, 0) + 1

    print("\n=== Break History ===")
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    for date_str in sorted(breaks_by_date.keys(), reverse=True)[:7]:  # Show last 7 days
        count = breaks_by_date[date_str]
        if date_str == today:
            label = "Today"
        elif date_str == yesterday:
            label = "Yesterday"
        else:
            label = date_str
        print(f"{label}: {count} break{'s' if count != 1 else ''}")


def add_session_to_history(history: dict, session: dict) -> None:
    """Add a completed session to the history."""
    history["sessions"].append(session)


def show_interval_dialog(root: tk.Tk, current_interval: int) -> tuple[str, int]:
    """Show a custom dialog for interval selection.

    Displays a dialog with:
    - "Time for a break!" message
    - Continue button showing current interval
    - Preset interval buttons (5, 15, 30, 60 min)
    - Stop button

    Args:
        root: The parent Tk window (hidden)
        current_interval: The currently selected interval in minutes

    Returns:
        Tuple of (action, interval) where:
        - action is "continue" or "stop"
        - interval is the selected minutes (int)
    """
    result = {"action": "stop", "interval": current_interval}

    dialog = tk.Toplevel(root)
    dialog.title("Break Reminder")
    dialog.resizable(False, False)

    # Handle window close (X button) as "stop"
    def on_close():
        result["action"] = "stop"
        dialog.destroy()

    dialog.protocol("WM_DELETE_WINDOW", on_close)

    # Title label
    title_label = tk.Label(dialog, text="Time for a break!", font=("Arial", 14, "bold"))
    title_label.pack(pady=(15, 10))

    # Continue button with current interval
    def on_continue():
        result["action"] = "continue"
        dialog.destroy()

    continue_btn = tk.Button(
        dialog,
        text=f"Continue ({current_interval} min)",
        command=on_continue,
        width=20,
        height=2
    )
    continue_btn.pack(pady=10)

    # Preset buttons frame
    preset_frame = tk.Frame(dialog)
    preset_frame.pack(pady=10)

    def make_preset_handler(minutes: int):
        def handler():
            result["action"] = "continue"
            result["interval"] = minutes
            dialog.destroy()
        return handler

    for minutes in PRESET_INTERVALS:
        btn = tk.Button(
            preset_frame,
            text=f"{minutes} min",
            command=make_preset_handler(minutes),
            width=8
        )
        btn.pack(side=tk.LEFT, padx=3)

    # Stop button
    def on_stop():
        result["action"] = "stop"
        dialog.destroy()

    stop_btn = tk.Button(dialog, text="Stop", command=on_stop, width=20)
    stop_btn.pack(pady=(10, 15))

    # Center the dialog on screen
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"+{x}+{y}")

    # Make dialog modal and wait for it to close
    dialog.grab_set()
    dialog.focus_set()
    root.wait_window(dialog)

    return (result["action"], result["interval"])


def main() -> None:
    # Load and display history at startup
    history = load_history()
    show_history_summary(history)

    # Create a hidden Tkinter root window for pop-ups
    root = tk.Tk()
    root.withdraw()

    # Show initial interval selection dialog
    current_interval = DEFAULT_INTERVAL
    action, current_interval = show_interval_dialog(root, current_interval)

    # If user clicks Stop on initial dialog, exit without starting session
    if action == "stop":
        print("\nSession cancelled.")
        root.destroy()
        return

    # Initialize session to track breaks
    current_session = create_session()

    while True:
        # Wait for the chosen time
        seconds = current_interval * 60
        root.after(seconds * 1000, root.quit)
        root.mainloop()

        # Show the interval selection dialog
        action, current_interval = show_interval_dialog(root, current_interval)

        # Stop = exit the loop
        if action == "stop":
            current_session["end"] = datetime.now().isoformat(timespec="seconds")
            break

        # Continue = record the break and continue with selected interval
        record_break(current_session)

    # Show session summary before exiting
    show_session_summary(current_session)

    # Save session to history
    add_session_to_history(history, current_session)
    if save_history(history):
        print("Session saved to history.")

    root.destroy()


if __name__ == "__main__":
    main()
