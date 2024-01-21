import sys, pyperclip, string

from ..utils import PWGenerator, DBHandler, CryptoManager, WrongPasswordError

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QWidget,
    QDialog,
    QListWidgetItem,
)
from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    Slot,
    QStringListModel,
    QPointF,
    QEvent,
    QPoint,
)

from PySide6 import QtGui
from .gui_login_ui import Ui_LoginWindow
from .gui_pwmanager_ui import Ui_PasswordGUI


def PysideSysAttrSetter(fnc):
    """
    This decorator adds system enviroment, mostly wanted to test this approach
    """

    def add_sys_variables(self):
        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
        fnc(self)

    return add_sys_variables


class PasswordIsMissing(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg


class PasswordToShortError(ValueError):
    def __init__(self, msg: str):
        """
        Error is raised when password is too short

        Args:
            msg (string): Extra information
        """
        self.msg = msg


class PasswordHasNoDigitError(ValueError):
    def __init__(self, msg: str):
        """
        Error is raised when password has no digit

        Args:
            msg (string): Extra information
        """
        self.msg = msg


class PasswordHasNoSpecialCharacterError(ValueError):
    def __init__(self, msg: str):
        """
        Error is raised when password has no special character from string.punctation

        Args:
            msg (string): Extra information
        """
        self.msg = msg


class ListItem:
    def __init__(self, text="", parent=None):
        self.data = []
        self.text = "Hi!" if not text else text


class LoginWindow(QWidget, Ui_LoginWindow):
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

    def __init__(self, parrent) -> None:
        """Initialize login window
        parrent is some kind of controller object with method
        "login_successfull"

        Args:
            parrent: some kind of controller object
        """
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.parrent = parrent
        self._add_events()

        self.SetPasswordText.setVisible(False)
        self._is_in_pw_create_mode = False

    def _add_events(self):
        self.LoginButton.clicked.connect(self.try_to_log_in)
        self.PasswordEdit.installEventFilter(self)
        self.exitButton.clicked.connect(self._exit_button_clicked)
        # Initialize variables for tracking mouse movements
        self.mousePressPos = None
        self.mouseMovePos = None

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.mousePressPos = event.globalPosition()
            self.mouseMovePos = event.globalPosition()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            # Calculate the new position of the window
            if self.mouseMovePos is None:
                return
            delta = QPointF(event.globalPosition() - self.mouseMovePos)
            new_pos = self.pos() + QPoint(int(delta.x()), int(delta.y()))
            self.move(new_pos)
            self.mouseMovePos = event.globalPosition()

    def try_to_log_in(self):
        try:
            if self._is_pw_valid_password(self.PasswordEdit.text()):
                self.parrent.login_successful()
            else:
                print("Login was not successful - wrong password")
        except PasswordIsMissing as ex:
            print(ex.msg)
            print("Setup password than try it again")

    # def eventFilter(self, obj, event: QEvent):
    #     if obj is self.PasswordEdit and event.type() == QEvent.Type.KeyPress:
    #         # Check if the pressed key is the Enter key
    #         if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
    #             # Call the login method when the Enter key is pressed
    #             self.try_to_log_in()
    #             return True  # Event handled
    #     return False  # Event not handled

    def _is_pw_valid_password(self, password: str) -> bool:
        """
        Returns True if password is the main password

        1) Find hsh password in DB
        2) Try password: str as a key
        3) If it passes -> you have right pass

        Returns:
            bool: True if password is correct
        """
        # Get the main password
        try:
            pw_binary = self._find_main_password()
        except PasswordIsMissing as ex:
            # If there is no main password - > ask user to create one
            self._set_create_password_mode()
            raise PasswordIsMissing("Password creation is required")

        hsh_handle = CryptoManager(password)
        try:
            hsh_handle.decrypt_string(pw_binary)
            return True
        except WrongPasswordError:
            return False

    def _find_main_password(self) -> bytes:
        """
        Returns a main password if exists, otherwise PasswordIsMissing is thowrn

        Raises:
            ValueError: _description_

        Returns:
            bytes: password in bytes if exist
        """
        db_password = DBHandler()
        try:
            pw_binary = db_password.get_password("MAINPW")
            return pw_binary
        except ValueError as ex:
            raise PasswordIsMissing("MainPassword was not found - add new one")

    def _set_new_main_pw(self) -> None:
        new_password = self.PasswordEdit.text()
        try:
            self._password_is_valid(new_password)
            db_handle = DBHandler()
            hsh_handle = CryptoManager(new_password)
            pw_bytes = hsh_handle.encrypt_string(new_password)
            db_handle.save_password("MAINPW", pw_bytes)
        except PasswordToShortError as ex:
            print(ex)
            self.SetPasswordText.setText(ex.msg)
        except PasswordHasNoDigitError as ex:
            print(ex)
            self.SetPasswordText.setText(ex.msg)
        except PasswordHasNoSpecialCharacterError as ex:
            print(ex)
            self.SetPasswordText.setText(ex.msg)

    def _password_is_valid(self, password: str) -> bool:
        """Check if password meet all critteria, returns True
        otherwise one of exception is rissen

        Args:
            password (str): _description_

        Raises:
            PasswordToShortError: is thrown if password has less than 4 chars
            PasswordHasNoDigitError
            PasswordHasNoSpecialCharacterError

        Returns:
            bool: True if password is ok
        """
        min_password_lengt = 4
        if len(password) < min_password_lengt:
            raise PasswordToShortError(
                f"Password must be at least {min_password_lengt} characters"
            )
        if not any(c.isdigit() for c in password):
            raise PasswordHasNoDigitError("Password must contain at least 1 digit")
        if not any(c in string.punctuation for c in password):
            raise PasswordHasNoSpecialCharacterError(
                "Pasword must contain at least special character"
            )
        return False

    def _set_create_password_mode(self):
        """Changes window to set up new main password"""
        if not self._is_in_pw_create_mode:
            self._is_in_pw_create_mode = True
            # Display text to user
            self.SetPasswordText.setVisible(True)

            # Change login button to create new password button
            self.LoginButton.setText("Create new password")
            self.LoginButton.clicked.disconnect(self.try_to_log_in)
            self.LoginButton.clicked.connect(self._set_new_main_pw)

    def _exit_button_clicked(self):
        self.parrent.close_application()


class PWManagerWindow(QWidget, Ui_PasswordGUI):
    def __init__(self, password="Konon") -> None:
        super().__init__()
        # Settup GUI
        self.setupUi(self)

        # Connect events to insturments
        self._add_events()

        # Set up database communication
        self.db_handle = DBHandler()

        # Set up random password generator
        self.pw_gen = PWGenerator(12)

        # Set up crypto manager
        self.hsh_handle = CryptoManager(password)

    def _add_events(self):
        self.AddSiteButton.clicked.connect(self.add_site_button_clicked)
        self.GetPasswordButton.clicked.connect(self.get_password_button_clicked)

        # Create a ListModel for handling displaying passwords
        self.list_model = QStringListModel()

        # Fill QListView instrument with sites
        self._display_sites()

    def add_site_button_clicked(self):
        new_site = self._get_new_site_name()
        new_random_password = self.pw_gen.get_random_password()
        random_password_bytes = self.hsh_handle.encrypt_string(new_random_password)
        self.db_handle.save_password(new_site, random_password_bytes)
        self._display_sites()

    def get_password_button_clicked(self):
        site = self.PasswordView.currentIndex().data()
        password_bytes = self.db_handle.get_password(site)
        password_string = self.hsh_handle.decrypt_string(password_bytes)
        pyperclip.copy(password_string)

    def _get_new_site_name(self) -> str:
        return self.SiteEdit.text()

    def _display_sites(self):
        # Get sites from database
        db_handle = DBHandler()
        self.list_model.setStringList(db_handle.get_all_sites())

        # Update QListView instrument
        self.PasswordView.setModel(self.list_model)


class MainGuiHandler(QMainWindow):
    """
    Call this class to create Password manager app

    Args:
        QMainWindow: _description_
        Ui_LoginWindow (_type_): _description_
    """

    @PysideSysAttrSetter
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow(self)
        self.login_window.show()

        # Bypass login - testing
        # self.login_successful()

        # Run the main loop
        self.app.exec()
        # self.close_application()

    def login_successful(self):
        """
        This method is executed after correct login password is passed
        """
        print("Login was successfull")
        # Close Login window
        self.login_window.close()

        # Create window for PWManager and show it
        self.pw_manager_window = PWManagerWindow(self.login_window.PasswordEdit.text())
        self.pw_manager_window.show()

    def close_application(self):
        sys.exit()


if __name__ == "__main__":
    gui = MainGuiHandler()
