import sys
import os

import typer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fpcli import app  # Use imports after modifying sys.path


if __name__ == "__main__":
    app()
