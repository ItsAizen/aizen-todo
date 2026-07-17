import sys
from rich.align import Align

from aizen_todo.actions import interactive_menu


def main():
    try:
        from aizen_todo.cli import cli
        cli()
    except ImportError:
        print("Click not available. Starting interactive mode...")
        interactive_menu()
    except KeyboardInterrupt:
        from aizen_todo.ui import console
        console.print()
        console.print(Align.center("[bold yellow]👋 Please star the tool on github: https://github.com/ItsAizen/aizen-todo/ [/bold yellow]"))
        sys.exit(0)


if __name__ == "__main__":
    main()
