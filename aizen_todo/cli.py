from datetime import datetime, date

try:
    import click
except ImportError:
    click = None

from aizen_todo import VERSION
from aizen_todo.ui import console, show_stats_line, show_tasks
from aizen_todo.data import create_task, load_tasks, save_tasks, backup_tasks
from aizen_todo.actions import interactive_menu


if click:
    @click.group(invoke_without_command=True)
    @click.pass_context
    @click.option("--version", "-v", is_flag=True, help="Show version")
    def cli(ctx, version):
        if version:
            console.print(f"[bold cyan]Aizen's Todo v{VERSION}[/bold cyan]")
            return
        if ctx.invoked_subcommand is None:
            interactive_menu()

    @cli.command()
    @click.argument("title")
    @click.option("--desc", "-d", default="", help="Description")
    @click.option("--category", "-c", default="Work", help="Category")
    @click.option("--priority", "-p", default=3, type=int, help="Priority 1-5")
    @click.option("--due", help="Due date YYYY-MM-DD")
    def add(title, desc, category, priority, due):
        """Add a new task"""
        task = create_task(title, desc, category, priority, due or "")
        tasks = load_tasks()
        tasks.append(task)
        save_tasks(tasks)
        console.print(f"[bold green]✔ Task added:[/bold green] {title} [dim]({task['id']})[/dim]")

    @cli.command()
    @click.option("--category", "-c", help="Filter by category")
    @click.option("--priority", "-p", type=int, help="Filter by priority")
    @click.option("--status", "-s", help="Filter by status")
    @click.option("--overdue", is_flag=True, help="Show overdue only")
    @click.option("--search", help="Search tasks")
    def list(category, priority, status, overdue, search):
        """List all tasks"""
        tasks = load_tasks()
        if not tasks:
            console.print("[yellow]📭 No tasks yet.[/yellow]")
            return

        if overdue:
            today = date.today().isoformat()
            tasks = [t for t in tasks if t["status"] not in ("done", "cancelled") and t.get("due_date") and str(t["due_date"]) < today]
        if category:
            tasks = [t for t in tasks if t.get("category", "").lower() == category.lower()]
        if priority:
            tasks = [t for t in tasks if t.get("priority") == priority]
        if status:
            tasks = [t for t in tasks if t.get("status") == status.lower()]
        if search:
            q = search.lower()
            tasks = [t for t in tasks if q in t["title"].lower() or q in t.get("description", "").lower()]

        console.print(show_stats_line(tasks))
        show_tasks(tasks)

    @cli.command()
    @click.argument("task_id")
    def done(task_id):
        """Mark a task as done (by ID, exact title, or unique substring)"""
        tasks = load_tasks()
        found = False
        for t in tasks:
            if t["id"] == task_id or task_id.lower() in t["title"].lower():
                t["status"] = "done"
                t["updated_at"] = datetime.now().isoformat()
                found = True
                console.print(f"[bold green]✔ Marked done:[/bold green] {t['title']}")
                break
        if not found:
            console.print(f"[red]Task not found: {task_id}[/red]")
        else:
            save_tasks(tasks)

    @cli.command()
    @click.argument("task_id")
    def delete(task_id):
        """Delete a task (by ID, exact title, or unique substring)"""
        tasks = load_tasks()
        for i, t in enumerate(tasks):
            if t["id"] == task_id or task_id.lower() in t["title"].lower():
                backup_tasks()
                deleted = tasks.pop(i)
                save_tasks(tasks)
                console.print(f"[bold red]✗ Deleted:[/bold red] {deleted['title']}")
                return
        console.print(f"[red]Task not found: {task_id}[/red]")

    @cli.command()
    def stats():
        """Show task statistics"""
        tasks = load_tasks()
        console.print(show_stats_line(tasks))

    @cli.command()
    def backup():
        """Backup task data"""
        backup_tasks()
        console.print("[bold green]✔ Backup created![/bold green]")



