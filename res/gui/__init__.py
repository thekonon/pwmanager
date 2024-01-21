import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))

from .gui import MainGuiHandler  # noqa: F401, E402
