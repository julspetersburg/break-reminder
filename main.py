"""Break reminder: shows a pop-up every N minutes until you click Stop."""

import tkinter as tk
from tkinter import messagebox


def get_minutes_with_default(default_minutes: int) -> int:
    """Ask for minutes in the terminal, defaulting when empty."""
    raw = input(
        f"Minutes between breaks (press Enter for {default_minutes}): "
    ).strip()
    if raw == "":
        return default_minutes
    try:
        minutes = int(raw)
    except ValueError:
        print("Please type a whole number like 5, 15, or 30.")
        return get_minutes_with_default(default_minutes)
    if minutes <= 0:
        print("Please type a number greater than 0.")
        return get_minutes_with_default(default_minutes)
    return minutes


def main() -> None:
    minutes = get_minutes_with_default(30)
    seconds = minutes * 60

    # Create a hidden Tkinter root window for pop-ups.
    root = tk.Tk()
    root.withdraw()

    while True:
        # Wait for the chosen time.
        root.after(seconds * 1000, root.quit)
        root.mainloop()

        # Show the reminder pop-up.
        result = messagebox.askokcancel(
            "Break Reminder",
            "Time for a break!",
            icon=messagebox.INFO,
        )

        # OK = keep running, Cancel (Stop) = exit.
        if not result:
            break
        # Let the user change the time for the next reminder.
        minutes = get_minutes_with_default(minutes)
        seconds = minutes * 60

    root.destroy()


if __name__ == "__main__":
    main()
