from .gui_login_ui import Ui_LoginWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6 import QtGui

# from typing import Annotated

from pieceful import Piece


@Piece("login_view")
class LoginWindow(QWidget):
    """
    Class for handling PySide LoginWidget
    ## Steps:
        Call LoginWindow
        User fills password
        User presses login button

    ## Important
    Parrent has to have method "login_successful" - called after sucessfull login

    Args:
        QWidget:
        Ui_LoginWindow:
    """

    def __init__(self) -> None:
        """Initialize login window
        parrent is some kind of controller object with method
        "login_successfull"

        Args:
            parrent: some kind of controller object
        """
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # self._add_events()

        self.ui.SetPasswordText.setVisible(False)
        self._is_in_pw_create_mode = False

        self.mousePressPos = None
        self.mouseMovePos = None

    def connect_login_button(self, callback):
        self.ui.LoginButton.clicked.connect(callback)

    def connect_exit_button(self, callback):
        self.ui.exitButton.clicked.connect(callback)

    def _add_events(self):
        pass
        # self.ui.LoginButton.clicked.connect(self.try_to_log_in)
        # self.ui.exitButton.clicked.connect(self._exit_button_clicked)

        # Initialize variables for tracking mouse movements

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == Qt.LeftButton:  # type: ignore
            self.mousePressPos = event.globalPosition()
            self.mouseMovePos = event.globalPosition()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == Qt.LeftButton:  # type: ignore
            # Calculate the new position of the window
            if self.mouseMovePos is None:
                return
            delta = QPointF(event.globalPosition() - self.mouseMovePos)
            new_pos = self.pos() + QPoint(int(delta.x()), int(delta.y()))
            self.move(new_pos)
            self.mouseMovePos = event.globalPosition()

    def get_password(self) -> str:
        return self.ui.PasswordEdit.text()

    def set_password_text(self, text: str) -> None:
        self.ui.SetPasswordText.setText(text)
