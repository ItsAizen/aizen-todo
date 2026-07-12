import shutil
from datetime import datetime, date

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

from aizen_todo.config import (
    CATEGORIES, PRIORITIES, PRIORITY_COLORS, PRIORITY_BARS,
    CATEGORY_COLORS, STATUSES, BANNER, SHORTCUTS
)
from aizen_todo.data import get_stats, load_tasks

console = Console()


# ----- helpers -----
def get_term_width():
    return shutil.get_terminal_size((80, 24)).columns


def centered(text):
    term = get_term_width()
    lines = text.split("\n")
    centered_lines = []
    for line in lines:
        stripped = line.rstrip()
        padding = max(0, (term - len(stripped)) // 2)
        centered_lines.append(" " * padding + stripped)
    return "\n".join(centered_lines)


def section_title(text, style="bold bright_cyan"):
    rule = Rule(style="bright_blue")
    return Group(rule, Align.center(Text(text, style=style)), rule)


def pause(msg="Press Enter to continue"):
    console.print()
    console.print(Align.center(f"[dim]{msg}[/dim]"))
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        import sys
        sys.exit(0)


def clear_screen():
    console.clear()


# ----- banner -----
def show_date():
    now = datetime.now()
    return f"[dim]{now.strftime('%a %b %d  %H:%M')}[/dim]"


def print_banner():
    console.print()
    console.print(Align.center(f"[bold cyan]{BANNER}[/bold cyan]"))
    tagline = "[italic dim]~ organize your code, conquer your day ~[/italic dim]"
    console.print(Align.center(f"{tagline}    {show_date()}"))
    console.print()


def transition():
    clear_screen()
    print_banner()


# ----- stats -----
def show_stats_line(tasks):
    total, done, pending, in_progress, cancelled, active, overdue = get_stats(tasks)
    progress_pct = (done / total * 100) if total else 0

    line = Text()
    line.append("  ", style="dim")
    line.append(f"● {total}", style="bold white")
    line.append(" total  ", style="dim")
    line.append(f"● {active}", style="bold yellow")
    line.append(" active  ", style="dim")
    line.append(f"● {done}", style="bold green")
    line.append(" done", style="dim")
    bar_c = "green" if progress_pct >= 75 else "yellow" if progress_pct >= 40 else "red"
    if total:
        w = 10
        filled = int(w * progress_pct / 100)
        line.append("  ", style="dim")
        line.append("▕", style="dim")
        line.append("━" * filled + "─" * (w - filled), style=bar_c)
        line.append("▏", style="dim")
        line.append(f" {progress_pct:>3.0f}%", style=f"bold {bar_c}")
    if overdue:
        line.append(f"  ⚠ {overdue}", style="bold red")
    line.append("  ", style="dim")
    return line


# ----- badges -----
def status_badge(status):
    badges = {
        "pending": "[bold yellow]◷ PENDING[/bold yellow]",
        "in_progress": "[bold bright_cyan]▶ IN PROGRESS[/bold bright_cyan]",
        "done": "[bold green]✓ DONE[/bold green]",
        "cancelled": "[bold red]✗ CANCELLED[/bold red]",
    }
    return badges.get(status, status)


def priority_badge(priority):
    label = PRIORITIES.get(priority, "N/A")
    color = PRIORITY_COLORS.get(priority, "white")
    bar = PRIORITY_BARS.get(priority, "")
    return f"[bold {color}]{label:<8} {bar}[/bold {color}]"


def cat_color(cat):
    return CATEGORY_COLORS.get(cat, "bright_white")


def cat_badge(cat):
    c = cat_color(cat)
    return f"[bold {c}]{cat}[/bold {c}]"


def date_str(d):
    if not d:
        return "[dim]—[/dim]"
    try:
        dt = datetime.fromisoformat(str(d))
        return dt.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return str(d)


def due_date_style(task):
    due = task.get("due_date", "")
    if not due or task["status"] in ("done", "cancelled"):
        return date_str(due), ""
    try:
        d = str(due)
        today = date.today().isoformat()
        if d < today:
            return f"[bold red]{date_str(due)} ⚠[/bold red]", "overdue"
        elif d == today:
            return f"[bold yellow]{date_str(due)} ← today[/bold yellow]", "today"
        elif d <= date.fromordinal(date.today().toordinal() + 2).isoformat():
            return f"[bold bright_yellow]{date_str(due)}[/bold bright_yellow]", "soon"
        return date_str(due), ""
    except (ValueError, TypeError):
        return date_str(due), ""


# ----- task table -----
def show_tasks(tasks, title="ALL TASKS"):
    if not tasks:
        console.print(Align.center(
            Panel.fit(
                "[bold yellow]✦  No tasks found  ✦[/bold yellow]\n\n"
                "[italic dim]Add one and start making progress![/italic dim]",
                border_style="yellow",
                padding=(2, 6),
            )
        ))
        return

    table = Table(
        box=box.HEAVY_EDGE,
        border_style="bright_blue",
        header_style="bold bright_cyan",
        title=f"[bold bright_white]{title}[/bold bright_white]",
        title_style="bold white",
        title_justify="center",
        show_edge=True,
        padding=(0, 1),
    )
    table.add_column("  #", style="dim", width=4, justify="right")
    table.add_column("TITLE", style="bold white", no_wrap=False, ratio=3)
    table.add_column("CATEGORY", justify="center", ratio=2)
    table.add_column("PRIORITY", justify="center", ratio=2)
    table.add_column("DUE", justify="center", ratio=2)
    table.add_column("STATUS", justify="center", ratio=2)

    for i, task in enumerate(tasks, 1):
        title_text = task["title"]
        if len(title_text) > 40:
            title_text = title_text[:37] + "..."

        due_style, _ = due_date_style(task)

        table.add_row(
            f"[dim]{i:>2}[/dim]",
            title_text,
            cat_badge(task.get("category", "N/A")),
            priority_badge(task.get("priority", 3)),
            due_style,
            status_badge(task["status"]),
        )

    console.print(Align.center(table))


def show_task_detail(task):
    c = cat_color(task.get("category", ""))
    console.print(Align.center(
        Panel.fit(
            Text(task["title"], style="bold white", justify="center"),
            border_style=c,
            padding=(1, 4),
        )
    ))

    detail = Table.grid(padding=(0, 2))
    detail.add_column(style="bold cyan", width=14, justify="right")
    detail.add_column(style="white")
    detail.add_row("ID", f"[dim]{task['id']}[/dim]")
    detail.add_row("Category", cat_badge(task.get("category", "N/A")))
    detail.add_row("Priority", priority_badge(task.get("priority", 3)))
    detail.add_row("Status", status_badge(task["status"]))
    detail.add_row("Due Date", due_date_style(task)[0])
    detail.add_row("Created", date_str(task.get("created_at", "")))
    detail.add_row("Updated", date_str(task.get("updated_at", "")))
    if task.get("description"):
        detail.add_row("", "")
        detail.add_row("Description", f"[italic]{task['description']}[/italic]")

    console.print(Align.center(Panel(detail, border_style="bright_blue", padding=(1, 3))))


# ----- menu -----
def make_menu_panel():
    left = Text()
    left.append("\n")
    left.append("  TASKS\n", style="bold bright_cyan")
    left.append("  [1/a]  ", style="dim")
    left.append("➕ Add\n", style="white")
    left.append("  [2/t]  ", style="dim")
    left.append("✔ Toggle\n", style="white")
    left.append("  [3/e]  ", style="dim")
    left.append("✎ Edit\n", style="white")
    left.append("  [4/d]  ", style="dim")
    left.append("🗑 Delete\n", style="white")

    right = Text()
    right.append("\n")
    right.append("  FILTERS\n", style="bold bright_cyan")
    right.append("  [5/c]  ", style="dim")
    right.append("📂 Category\n", style="white")
    right.append("  [6/p]  ", style="dim")
    right.append("⭐ Priority\n", style="white")
    right.append("  [7/s]  ", style="dim")
    right.append("🔍 Status\n", style="white")
    right.append("  [8/f]  ", style="dim")
    right.append("🔎 Search\n", style="white")
    right.append("  [9/o]  ", style="dim")
    right.append("⚠ Overdue\n", style="white")
    right.append("\n")
    right.append("  SYSTEM\n", style="bold bright_cyan")
    right.append("  [b]    ", style="dim")
    right.append("💾 Backup\n", style="white")
    right.append("  [0/q]  ", style="dim")
    right.append("🚪 Exit\n", style="white")

    nudge = Text("\n\n\n")
    right.append_text(nudge)

    menu_table = Table.grid(padding=(0, 4), expand=True)
    menu_table.add_column(ratio=1)
    menu_table.add_column(ratio=1)
    menu_table.add_row(left, right)

    return Panel(
        menu_table,
        title="[bold bright_cyan]⚡ MENU ⚡[/bold bright_cyan]",
        border_style="bright_blue",
        padding=(0, 2),
    )


# ----- dashboard -----
def show_dashboard():
    clear_screen()
    print_banner()
    tasks = load_tasks()

    if tasks:
        stats = show_stats_line(tasks)
        console.print(Align.center(Panel(stats, border_style="bright_black", padding=(0, 1))))
        console.print()
        show_tasks(tasks, f"ALL TASKS  ({len(tasks)} total)")
    else:
        console.print(Align.center(
            Panel.fit(
                "[bold yellow]✦  Welcome to Aizen's Todo!  ✦[/bold yellow]\n\n"
                "[italic dim]Your task list is empty.\n"
                "Choose option 1 to add your first task.[/italic dim]",
                border_style="yellow",
                padding=(2, 6),
            )
        ))
    console.print()
    console.print(Align.center(make_menu_panel()))
    console.print()
    console.print(Align.center(SHORTCUTS))
    console.print()
