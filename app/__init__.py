import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from pieceful import PieceFactory
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))


@PieceFactory
def app() -> QApplication:
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)

    app = QApplication(sys.argv)
    return app


from .presenter import Presenter  # noqa: E402, F401
