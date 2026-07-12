from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "aizen-todo"
TASKS_FILE = CONFIG_DIR / "tasks.json"
BACKUP_DIR = CONFIG_DIR / "backups"

CATEGORIES = [
    "Work", "Personal", "Coding", "Business",
    "Learning", "Health", "Finance", "Ideas", "Urgent"
]

PRIORITIES = {1: "CRITICAL", 2: "HIGH", 3: "MEDIUM", 4: "LOW", 5: "TRIVIAL"}
PRIORITY_COLORS = {1: "red", 2: "yellow", 3: "cyan", 4: "green", 5: "bright_black"}
PRIORITY_BARS = {1: "██████", 2: "████▓", 3: "███▒▒", 4: "██▒▒▒", 5: "█▒▒▒▒"}

CATEGORY_COLORS = {
    "Work": "bright_white", "Personal": "green", "Coding": "cyan",
    "Business": "yellow", "Learning": "magenta", "Health": "red",
    "Finance": "green_yellow", "Ideas": "bright_magenta", "Urgent": "bright_red"
}

STATUSES = ["pending", "in_progress", "done", "cancelled"]

BANNER = """\
┏━┓╻╺━┓┏━╸┏┓╻   ╺┳╸┏━┓╺┳┓┏━┓
┣━┫┃┏━┛┣╸ ┃┗┫    ┃ ┃ ┃ ┃┃┃ ┃
╹ ╹╹┗━╸┗━╸╹ ╹    ╹ ┗━┛╺┻┛┗━┛"""

SHORTCUTS = (
    "[dim]Shortcuts:[/dim] "
    "[bold bright_cyan]a[/bold bright_cyan]dd  "
    "[bold bright_cyan]t[/bold bright_cyan]oggle  "
    "[bold bright_cyan]e[/bold bright_cyan]dit  "
    "[bold bright_cyan]d[/bold bright_cyan]elete  "
    "f[bold bright_cyan]c[/bold bright_cyan]at  "
    "f[bold bright_cyan]p[/bold bright_cyan]ri  "
    "f[bold bright_cyan]s[/bold bright_cyan]tat  "
    "[bold bright_cyan]s[/bold bright_cyan]earch  "
    "[bold bright_cyan]o[/bold bright_cyan]verdue  "
    "[bold bright_cyan]b[/bold bright_cyan]ackup  "
    "[bold red]q[/bold red]uit"
)
