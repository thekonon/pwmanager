import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from pieceful import PieceFactory


@PieceFactory
def app() -> QApplication:
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)

    app = QApplication(sys.argv)
    return app
