import sys
from src.cli import run_interactive_cli
from src.gui import run_gui


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_interactive_cli()
    else:
        run_gui()
