import json
import uuid
import shutil
from datetime import datetime, date

from aizen_todo.config import CONFIG_DIR, TASKS_FILE, BACKUP_DIR


def ensure_dirs():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def load_tasks():
    ensure_dirs()
    if not TASKS_FILE.exists():
        return []
    try:
        with open(TASKS_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    ensure_dirs()
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2, default=str)


def backup_tasks():
    ensure_dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if TASKS_FILE.exists():
        copies = sorted(BACKUP_DIR.glob("tasks_*.json"), reverse=True)
        for c in copies[9:]:
            c.unlink()
        shutil.copy2(TASKS_FILE, BACKUP_DIR / f"tasks_{ts}.json")


def create_task(title, description="", category="Work", priority=3,
                due_date=None, status="pending"):
    return {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "due_date": due_date,
        "status": status,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }


def get_stats(tasks):
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == "done")
    pending = sum(1 for t in tasks if t["status"] == "pending")
    in_progress = sum(1 for t in tasks if t["status"] == "in_progress")
    cancelled = sum(1 for t in tasks if t["status"] == "cancelled")
    active = total - done - cancelled
    overdue = sum(
        1 for t in tasks
        if t["status"] not in ("done", "cancelled") and t.get("due_date")
        and str(t["due_date"]) < date.today().isoformat()
    )
    return total, done, pending, in_progress, cancelled, active, overdue
