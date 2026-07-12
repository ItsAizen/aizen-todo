<pre>
┏━┓╻╺━┓┏━╸┏┓╻   ╺┳╸┏━┓╺┳┓┏━┓
┣━┫┃┏━┛┣╸ ┃┗┫    ┃ ┃ ┃ ┃┃┃ ┃
╹ ╹╹┗━╸┗━╸╹ ╹    ╹ ┗━┛╺┻┛┗━┛
</pre>

<p align="center">
  <strong>A beautiful CLI todo manager for programmers &amp; entrepreneurs</strong><br>
  <sub>Interactive dashboard · Quick CLI commands · Color-coded priorities · Persistent storage</sub>
</p>

<p align="center">
  <a href="https://github.com/ItsAizen/aizen-todo">
    <img src="https://img.shields.io/github/v/release/ItsAizen/aizen-todo?style=flat&logo=github&color=brightgreen" alt="GitHub Release">
  </a>
  <a href="https://pypi.org/project/aizen-todo/">
    <img src="https://img.shields.io/badge/python-≥3.8-blue?style=flat&logo=python" alt="Python">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat" alt="License">
  </a>
  <a href="https://github.com/ItsAizen/aizen-todo/stargazers">
    <img src="https://img.shields.io/github/stars/ItsAizen/aizen-todo?style=flat&logo=star" alt="Stars">
  </a>
</p>

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/ItsAizen"><b>Mehrdad Ansarifar</b></a></sub>
</p>

---

## ✦ At a glance

```
● 6 total  ● 4 active  ● 2 done  ▕━━━───────▏  33%

┏━━━━━━┯━━━━━━━━━━━━━━┯━━━━━━━━┯━━━━━━━━━━━━━━┯━━━━━━━━━━┯━━━━━━━━━┓
┃    # │ TITLE        │ CATEGORY│   PRIORITY   │   DUE    │  STATUS ┃
┠──────┼──────────────┼─────────┼──────────────┼──────────┼─────────┨
┃    1 │ Deploy CI/CD │ Coding  │ CRITICAL ████│ Jul 22   │ ◷ PENDING
┃    2 │ Q3 roadmap   │ Business│ HIGH     ████│ Jul 18   │ ✓ DONE  │
┃    3 │ Team sync    │ Work    │ MEDIUM   ███▒│    —     │ ◷ PENDING
┃    4 │ Read book    │ Learning│ LOW      ██▒▒│ Aug 01   │ ◷ PENDING
┃    5 │ Fix CSS      │ Coding  │ HIGH     ████│ Jul 13   │ ✓ DONE  │
┃    6 │ Morning run  │ Personal│ TRIVIAL  █▒▒▒│    —     │ ◷ PENDING
┗━━━━━━┷━━━━━━━━━━━━━━┷━━━━━━━━┷━━━━━━━━━━━━━━┷━━━━━━━━━━┷━━━━━━━━━┛

╔═══════════════════╤═══════════════════╗
║  TASKS            │  FILTERS          ║
║  [1/a] ➕ Add     │  [5/c] 📂 Category║
║  [2/t] ✔ Toggle   │  [6/p] ⭐ Priority║
║  [3/e] ✎ Edit     │  [7/s] 🔍 Status  ║
║  [4/d] 🗑 Delete   │  [8/f] 🔎 Search  ║
║                   │  [9/o] ⚠ Overdue  ║
║                   │  SYSTEM           ║
║                   │  [b]   💾 Backup   ║
║                   │  [0/q] 🚪 Exit     ║
╚═══════════════════╧═══════════════════╝
```

---

## ✦ Features

| | |
|---|---|
| 🖥 **Interactive dashboard** | Full-screen TUI with banner, live stats, task table, and two-column menu |
| ⌨ **Dual-key navigation** | Every action responds to both a number (`1`–`9`) and a letter (`a`, `t`, `e`, …) |
| 🎨 **Color-coded priorities** | `CRITICAL` · `HIGH` · `MEDIUM` · `LOW` · `TRIVIAL` — each with distinct colors and progress bars |
| 📂 **9 built-in categories** | Work, Personal, Coding, Business, Learning, Health, Finance, Ideas, Urgent |
| 📅 **Due date tracking** | Overdue `⚠`, due-today `← today`, upcoming `soon` — all highlighted |
| 🔎 **Search & filters** | Filter by category, priority, status, keyword — or show only overdue |
| ⚡ **Full CLI mode** | `add`, `list`, `done`, `delete`, `stats`, `backup` — no interactive mode needed |
| 💾 **Auto-backups** | Keeps the last 10 snapshot copies; manual backups never overwrite |
| 🗃 **Persistent JSON storage** | All data in `~/.config/aizen-todo/tasks.json` — easy to back up or sync |
| 🎭 **Rich formatting** | Powered by [`rich`](https://github.com/Textualize/rich) — tables, panels, progress bars, and colors |

---

## ✦ Quick start

```bash
# Install
pip install git+https://github.com/ItsAizen/aizen-todo.git

# Jump right in
aizen-todo

# Or add tasks from the command line
aizen-todo add "Refactor auth module" -c Coding -p 1 --due 2026-07-25
aizen-todo add "Team retro notes" -c Work -p 3
aizen-todo add "Read 'Clean Code'" -c Learning -p 4 --due 2026-08-01
```

---

## ✦ Installation

### Via pip (from source)

```bash
git clone https://github.com/ItsAizen/aizen-todo.git
cd aizen-todo
pip install .
```

### Development

```bash
pip install -e ".[dev]"
```

### Verify

```bash
aizen-todo --version
# → Aizen's Todo v2.0.0
```

---

## ✦ Usage

### Interactive mode

Run `aizen-todo` with no arguments:

```bash
aizen-todo
```

The screen is divided into five sections:

1. **Banner** — the ASCII art title with current weekday and time
2. **Stats bar** — total / active / done counts with a progress bar
3. **Task table** — all tasks with their category, priority, due date, and status
4. **Two-column menu** — task operations on the left, filters & system on the right
5. **Shortcut bar** — quick reference for every keyboard shortcut

### Keyboard shortcuts

| Key | Letter | Action |
|-----|--------|--------|
| `1` | `a` | ➕ Add Task |
| `2` | `t` | ✔ Toggle Status (pending → in_progress → done → pending) |
| `3` | `e` | ✎ Edit Task |
| `4` | `d` | 🗑 Delete Task |
| `5` | `c` | 📂 Filter by Category |
| `6` | `p` | ⭐ Filter by Priority |
| `7` | `s` | 🔍 Filter by Status |
| `8` | `f` | 🔎 Search |
| `9` | `o` | ⚠ Overdue Tasks |
| `b` | — | 💾 Backup Data |
| `0` | `q` | 🚪 Exit |

### CLI commands

```bash
# ── Adding tasks ──
aizen-todo add "Fix login bug"                    # quick add
aizen-todo add "Write docs" -d "API v2" -c Work   # with description & category
aizen-todo add "Deploy" -p 1 --due 2026-07-20     # priority 1 (critical) with due date

# ── Listing and filtering ──
aizen-todo list                                    # all tasks
aizen-todo list --category Coding                  # by category
aizen-todo list --priority 1                       # by priority (1=CRITICAL)
aizen-todo list --status done                      # by status
aizen-todo list --overdue                          # overdue only
aizen-todo list --search "deploy"                  # keyword search

# ── Managing tasks ──
aizen-todo done "login bug"                        # mark done (by substring)
aizen-todo done a1b2c3d4                           # mark done (by ID)
aizen-todo delete "Write docs"                     # delete task

# ── System ──
aizen-todo stats                                   # show statistics
aizen-todo backup                                  # create a backup
aizen-todo --version                               # show version
aizen-todo --help                                  # show help
```

---

## ✦ Data storage

All data is stored in `~/.config/aizen-todo/`:

```
~/.config/aizen-todo/
├── tasks.json              # current task list (JSON)
└── backups/
    ├── tasks_20260712_143022.json
    ├── tasks_20260712_150101.json
    └── tasks_20260712_151230.json   # last 10 snapshots kept
```

Automatic backups trigger before destructive operations. Manual backups via `b` key or `aizen-todo backup` are always safe.

---

## ✦ Project structure

```
aizen-todo/
├── aizen_todo/
│   ├── __init__.py     # package version
│   ├── __main__.py     # entry point (`python -m aizen_todo`)
│   ├── config.py       # constants, paths, color maps
│   ├── data.py         # CRUD, persistence, backup logic
│   ├── ui.py           # banner, stats, tables, menus
│   ├── actions.py      # interactive screen handlers
│   └── cli.py          # click CLI commands
├── pyproject.toml       # packaging & dependencies
├── setup.py             # compatibility fallback
├── README.md
├── LICENSE
└── .gitignore
```

---

## ✦ Dependencies

| Package | Role |
|---------|------|
| [`rich`](https://github.com/Textualize/rich) | Beautiful terminal formatting (tables, panels, colors) |
| [`click`](https://github.com/pallets/click) | CLI argument parsing and command routing |

Both install automatically with `pip install .`.

---

## ✦ Author

**Mehrdad Ansarifar** — [@ItsAizen](https://github.com/ItsAizen)

- GitHub: [github.com/ItsAizen](https://github.com/ItsAizen)
- Project: [github.com/ItsAizen/aizen-todo](https://github.com/ItsAizen/aizen-todo)

---

## ✦ License

[MIT](LICENSE) © 2026 Mehrdad Ansarifar

---

<p align="center">
  <sub>If you find this useful, <a href="https://github.com/ItsAizen/aizen-todo/stargazers">⭐ star it on GitHub</a></sub>
</p>
