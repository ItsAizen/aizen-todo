import sys
import time
from datetime import datetime, date

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from aizen_todo.config import CATEGORIES, PRIORITIES, PRIORITY_COLORS, PRIORITY_BARS, STATUSES
from aizen_todo.data import create_task, load_tasks, save_tasks, backup_tasks
from aizen_todo.ui import (
    console, transition, section_title, show_tasks, show_task_detail,
    cat_badge, status_badge, pause, clear_screen, print_banner,
    make_menu_panel, show_stats_line, SHORTCUTS
)


def screen_add_task():
    transition()
    console.print(Align.center(section_title("✦  ADD NEW TASK  ✦")))
    console.print()

    title = Prompt.ask("[bold]Title[/bold]")
    if not title:
        console.print(Align.center("[red]Title cannot be empty![/red]"))
        pause()
        return

    desc = Prompt.ask("[bold]Description[/bold]", default="")

    console.print()
    console.print(Align.center("[bold]Categories:[/bold]  " + "  ".join(
        cat_badge(c) for c in CATEGORIES
    )))
    cat = Prompt.ask("[bold]Category[/bold]", default="Work")
    if cat not in CATEGORIES:
        CATEGORIES.append(cat)

    console.print()
    console.print(Align.center("[bold]Priority:[/bold]"))
    for k, v in PRIORITIES.items():
        c = PRIORITY_COLORS[k]
        console.print(Align.center(f"  [bold {c}]{k}[/bold {c}]  {v}  {PRIORITY_BARS[k]}"))
    pri = Prompt.ask("[bold]Priority (1-5)[/bold]", default="3")
    try:
        pri = int(pri)
        if pri not in PRIORITIES:
            pri = 3
    except ValueError:
        pri = 3

    due = Prompt.ask("[bold]Due date[/bold] [dim](YYYY-MM-DD)[/dim]", default="")
    if due:
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            console.print(Align.center("[red]Invalid date format. Skipping.[/red]"))
            due = ""

    task = create_task(title, desc, cat, pri, due if due else "")
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    console.print()
    console.print(Align.center(
        Panel.fit(
            f"[bold green]✓  Task added successfully![/bold green]\n[dim]ID: {task['id']}[/dim]",
            border_style="green",
            padding=(1, 4),
        )
    ))
    pause()


def screen_mark_task():
    transition()
    tasks = load_tasks()
    if not tasks:
        console.print(Align.center("[yellow]No tasks to update.[/yellow]"))
        pause()
        return

    console.print(Align.center(section_title("✔  TOGGLE TASK STATUS  ✔")))
    show_tasks(tasks)

    try:
        idx_text = Prompt.ask("[bold]Task # to toggle[/bold] [dim](or 0 to cancel)[/dim]")
        idx = int(idx_text) - 1
        if idx == -1:
            return
        if 0 <= idx < len(tasks):
            task = tasks[idx]
            cycles = {"pending": "in_progress", "in_progress": "done", "done": "pending", "cancelled": "pending"}
            new_status = cycles.get(task["status"], "pending")
            task["status"] = new_status
            task["updated_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            console.print()
            console.print(Align.center(
                Panel.fit(
                    f"[bold]'{task['title']}'[/bold]  →  {status_badge(new_status)}",
                    border_style="green",
                    padding=(1, 4),
                )
            ))
        else:
            console.print(Align.center("[red]Invalid task number.[/red]"))
    except ValueError:
        console.print(Align.center("[red]Invalid input.[/red]"))
    pause()


def screen_edit_task():
    transition()
    tasks = load_tasks()
    if not tasks:
        console.print(Align.center("[yellow]No tasks to edit.[/yellow]"))
        pause()
        return

    console.print(Align.center(section_title("✎  EDIT TASK  ✎")))
    show_tasks(tasks)

    try:
        idx_text = Prompt.ask("[bold]Task # to edit[/bold] [dim](or 0 to cancel)[/dim]")
        idx = int(idx_text) - 1
        if idx == -1:
            return
        if 0 <= idx < len(tasks):
            task = tasks[idx]
            transition()
            console.print(Align.center(section_title(f"EDITING: {task['title']}")))
            show_task_detail(task)

            title = Prompt.ask("[bold]Title[/bold]", default=task["title"])
            desc = Prompt.ask("[bold]Description[/bold]", default=task.get("description", ""))
            console.print()
            console.print(Align.center("[bold]Categories:[/bold]  " + "  ".join(
                cat_badge(c) for c in CATEGORIES
            )))
            cat = Prompt.ask("[bold]Category[/bold]", default=task.get("category", "Work"))
            console.print()
            for k, v in PRIORITIES.items():
                c = PRIORITY_COLORS[k]
                console.print(Align.center(f"  [bold {c}]{k}[/bold {c}]  {v}  {PRIORITY_BARS[k]}"))
            pri = Prompt.ask("[bold]Priority (1-5)[/bold]", default=str(task.get("priority", 3)))
            try:
                pri = int(pri)
                if pri not in PRIORITIES:
                    pri = task.get("priority", 3)
            except ValueError:
                pri = task.get("priority", 3)
            due = Prompt.ask("[bold]Due date[/bold] [dim](YYYY-MM-DD)[/dim]", default=task.get("due_date", ""))
            if due:
                try:
                    datetime.strptime(due, "%Y-%m-%d")
                except ValueError:
                    console.print(Align.center("[red]Invalid date. Keeping original.[/red]"))
                    due = task.get("due_date", "")

            tasks[idx].update({
                "title": title, "description": desc, "category": cat,
                "priority": pri, "due_date": due,
                "updated_at": datetime.now().isoformat(),
            })
            save_tasks(tasks)
            console.print()
            console.print(Align.center(Panel.fit(
                "[bold green]✓  Task updated![/bold green]", border_style="green", padding=(1, 4)
            )))
        else:
            console.print(Align.center("[red]Invalid task number.[/red]"))
    except ValueError:
        console.print(Align.center("[red]Invalid input.[/red]"))
    pause()


def screen_delete_task():
    transition()
    tasks = load_tasks()
    if not tasks:
        console.print(Align.center("[yellow]No tasks to delete.[/yellow]"))
        pause()
        return

    console.print(Align.center(section_title("🗑  DELETE TASK  🗑")))
    show_tasks(tasks)

    try:
        idx_text = Prompt.ask("[bold red]Task # to delete[/bold red] [dim](or 0 to cancel)[/dim]")
        idx = int(idx_text) - 1
        if idx == -1:
            return
        if 0 <= idx < len(tasks):
            task = tasks[idx]
            if Confirm.ask(f"Delete '[bold]{task['title']}[/bold]'?"):
                backup_tasks()
                deleted = tasks.pop(idx)
                save_tasks(tasks)
                console.print()
                console.print(Align.center(
                    Panel.fit(
                        f"[bold red]✗  Deleted:[/bold red] [bold]{deleted['title']}[/bold]",
                        border_style="red",
                        padding=(1, 4),
                    )
                ))
        else:
            console.print(Align.center("[red]Invalid task number.[/red]"))
    except ValueError:
        console.print(Align.center("[red]Invalid input.[/red]"))
    pause()


def screen_filter_category():
    transition()
    tasks = load_tasks()
    if not tasks:
        console.print(Align.center("[yellow]No tasks.[/yellow]"))
        pause()
        return

    cats = sorted(set(t.get("category", "Other") for t in tasks))
    console.print(Align.center(section_title("📂  FILTER BY CATEGORY  📂")))
    console.print()
    console.print(Align.center("  ".join(cat_badge(c) for c in cats)))
    console.print()
    cat = Prompt.ask("[bold]Category[/bold] [dim](or 0 to cancel)[/dim]")
    if cat == "0":
        return
    filtered = [t for t in tasks if t.get("category", "").lower() == cat.lower()]
    if filtered:
        show_tasks(filtered, f"📂  {cat}  📂")
    else:
        console.print(Align.center(f"[yellow]No tasks in '[bold]{cat}[/bold]'.[/yellow]"))
    pause()


def screen_filter_priority():
    transition()
    tasks = load_tasks()
    if not tasks:
        console.print(Align.center("[yellow]No tasks.[/yellow]"))
        pause()
        return

    console.print(Align.center(section_title("⭐  FILTER BY PRIORITY  ⭐")))
    console.print()
    for k, v in PRIORITIES.items():
        c = PRIORITY_COLORS[k]
        console.print(Align.center(f"  [bold {c}]{k}[/bold {c}]  {v}  {PRIORITY_BARS[k]}"))
    console.print()
    try:
        p_text = Prompt.ask("[bold]Priority (1-5)[/bold] [dim](or 0 to cancel)[/dim]")
        p = int(p_text)
        if p == 0:
            return
        if p in PRIORITIES:
            filtered = [t for t in tasks if t.get("priority") == p]
            if filtered:
                show_tasks(filtered, f"⭐  PRIORITY: {PRIORITIES[p]}  ⭐")
            else:
                console.print(Align.center(f"[yellow]No tasks with priority {p}.[/yellow]"))
        else:
            console.print(Align.center("[red]Invalid priority level.[/red]"))
    except ValueError:
        console.print(Align.center("[red]Invalid input.[/red]"))
    pause()


def screen_filter_status():
    transition()
    tasks = load_tasks()
    if not tasks:
        console.print(Align.center("[yellow]No tasks.[/yellow]"))
        pause()
        return

    console.print(Align.center(section_title("🔍  FILTER BY STATUS  🔍")))
    console.print()
    for s in STATUSES:
        console.print(Align.center(f"  {status_badge(s)}"))
    console.print()
    s = Prompt.ask("[bold]Status[/bold] [dim](or 0 to cancel)[/dim]").lower()
    if s == "0":
        return
    if s in STATUSES:
        filtered = [t for t in tasks if t["status"] == s]
        if filtered:
            show_tasks(filtered, f"STATUS: {s.replace('_', ' ').upper()}")
        else:
            console.print(Align.center(f"[yellow]No tasks with status '{s}'.[/yellow]"))
    else:
        console.print(Align.center("[red]Invalid status.[/red]"))
    pause()


def screen_search():
    transition()
    tasks = load_tasks()
    if not tasks:
        console.print(Align.center("[yellow]No tasks.[/yellow]"))
        pause()
        return

    console.print(Align.center(section_title("🔎  SEARCH TASKS  🔎")))
    console.print()
    query = Prompt.ask("[bold]Search for[/bold] [dim](or 0 to cancel)[/dim]").lower()
    if query == "0":
        return
    filtered = [
        t for t in tasks
        if query in t["title"].lower()
        or query in t.get("description", "").lower()
        or query in t.get("category", "").lower()
    ]
    if filtered:
        show_tasks(filtered, f"🔎  RESULTS: '{query}'  🔎")
    else:
        console.print(Align.center(f"[yellow]No tasks matching '[bold]{query}[/bold]'.[/yellow]"))
    pause()


def screen_overdue():
    transition()
    tasks = load_tasks()
    today = date.today().isoformat()
    overdue = [
        t for t in tasks
        if t["status"] not in ("done", "cancelled")
        and t.get("due_date") and str(t["due_date"]) < today
    ]
    if overdue:
        console.print(Align.center(section_title(f"⚠  OVERDUE ({len(overdue)})  ⚠")))
        show_tasks(overdue, f"⚠  OVERDUE ({len(overdue)})  ⚠")
    else:
        console.print(Align.center(
            Panel.fit(
                "[bold green]✓  No overdue tasks!  You're on track.[/bold green]",
                border_style="green",
                padding=(1, 4),
            )
        ))
    pause()


def screen_backup():
    backup_tasks()
    console.print()
    console.print(Align.center(
        Panel.fit(
            "[bold green]✓  Backup created successfully![/bold green]",
            border_style="green",
            padding=(1, 4),
        )
    ))
    pause()


def screen_exit():
    console.print()
    console.print(Align.center(
        Panel.fit(
            "[bold bright_cyan]✦  Until next time! Stay organized.  ✦[/bold bright_cyan]\n\n"
            "[dim]\"The best time to plant a tree was 20 years ago.\n"
            "The second best time is now.\"[/dim]",
            border_style="bright_blue",
            padding=(2, 6),
        )
    ))
    console.print()
    time.sleep(1.5)
    sys.exit(0)


def interactive_menu():
    while True:
        show_dashboard()
        choice = Prompt.ask("[bold]Choice[/bold]").strip().lower()

        action_map = {
            "1": screen_add_task, "a": screen_add_task,
            "2": screen_mark_task, "t": screen_mark_task,
            "3": screen_edit_task, "e": screen_edit_task,
            "4": screen_delete_task, "d": screen_delete_task,
            "5": screen_filter_category, "c": screen_filter_category,
            "6": screen_filter_priority, "p": screen_filter_priority,
            "7": screen_filter_status, "s": screen_filter_status,
            "8": screen_search, "f": screen_search,
            "9": screen_overdue, "o": screen_overdue,
            "b": screen_backup,
            "0": screen_exit, "q": screen_exit,
        }

        if choice in action_map:
            action_map[choice]()
        else:
            console.print(Align.center("[red]Invalid choice. Try again.[/red]"))
            time.sleep(1)
