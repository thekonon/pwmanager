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
from PySide6.QtCore import Qt, QThread, Signal, Slot, QStringListModel, QPointF, QPoint
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


class ListItem(object):
    def __init__(self, text="", parent=None):
        super(ListItem, self).__init__()
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
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressPos = event.globalPosition()
            self.mouseMovePos = event.globalPosition()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # Calculate the new position of the window
            delta = QPointF(event.globalPosition() - self.mouseMovePos)
            new_pos = self.pos() + QPoint(delta.x(), delta.y())
            self.move(new_pos)
            self.mouseMovePos = event.globalPosition()

    def try_to_log_in(self):
        try:
            if self._is_pw_valid_password(self.PasswordEdit.text()):
                self.parrent.login_successful(self.PasswordEdit.text())
            else:
                print("Login was not successful - wrong password")
        except PasswordIsMissing as ex:
            print(ex.msg)
            print("Setup password than try it again")

    def eventFilter(self, obj, event):
        if obj is self.PasswordEdit and event.type() == event.KeyPress:
            # Check if the pressed key is the Enter key
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                # Call the login method when the Enter key is pressed
                if not self._is_in_pw_create_mode:
                    self.try_to_log_in()
                else:
                    self._set_new_main_pw()
                return True  # Event handled
        return False  # Event not handled

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
            
            # Save encrypted password if it is ok
            db_handle = DBHandler()
            hsh_handle = CryptoManager(new_password)
            pw_bytes = hsh_handle.encrypt_string(new_password)
            db_handle.save_password("MAINPW", pw_bytes)
            
            # Changes mode to login
            self._set_login_mode()
            # Remove password - force user to write it again
            self.PasswordEdit.setText("")
            
        except PasswordToShortError as ex:
            print(ex)
            self.SetPasswordText.text = ex.msg
        except PasswordHasNoDigitError as ex:
            print(ex)
            self.SetPasswordText.text = ex.msg
        except PasswordHasNoSpecialCharacterError as ex:
            print(ex)
            self.SetPasswordText.text = ex.msg

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
            raise PasswordToShortError(f'Password must be at least {min_password_lengt} characters')
        if not any(c.isdigit() for c in password):
            raise PasswordHasNoDigitError('Password must contain at least 1 digit')
        if not any(c in string.punctuation for c in password):
            raise PasswordHasNoSpecialCharacterError('Pasword must contain at least special character')
        return False
    
    def _set_login_mode(self):
        """
        Changes window to set up new main password
        """
        # If it is already in set password mode - > do nothing
        if self._is_in_pw_create_mode:
            self._is_in_pw_create_mode = False
            # Display text to user
            self.SetPasswordText.setVisible(False)
            
            # Change login button to create new password button
            self.LoginButton.setText("Log in")
            self.LoginButton.clicked.connect(self.try_to_log_in)
            self.LoginButton.clicked.disconnect(self._set_new_main_pw)
    
    def _set_create_password_mode(self):
        """
        Changes window to set up new main password
        """
        # If it is already in set password mode - > do nothing
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

    def add_site_button_clicked(self) -> None:
        """
        Adds new site
        """
        # Step 1 get site name and password
        site = self._get_new_site_name()
        if self.generatePasswordCHB.isChecked():
            password = self.pw_gen.get_random_password()
        else:
            password = self.PasswordEdit.text()
            
        # Step 2 encrypt password using main password
        random_password_bytes = self.hsh_handle.encrypt_string(password)
        
        # Step 3 save site + password
        self.db_handle.save_password(site, random_password_bytes)
        self._display_sites()

    def get_password_check_box_clicked(self):
        print("Coping password")
        site = self.PasswordView.currentIndex().data()
        password_bytes = self.db_handle.get_password(site)
        try:
            password_string = self.hsh_handle.decrypt_string(password_bytes)
        except WrongPasswordError as ex:
            print("MainPW was not able to decrypt selected sites PW")
            print(ex.msg)
            return None
        pyperclip.copy(password_string)
        print("Password copied!")

    def _get_new_site_name(self) -> str:
        return self.SiteEdit.text()

    def _generate_pw_clicked(self) -> None:
        self.PasswordEdit.setText("")
        self.PasswordEdit.setEnabled(not self.generatePasswordCHB.isChecked())

    def _add_events(self):
        self.AddSiteButton.clicked.connect(self.add_site_button_clicked)
        self.GetPasswordButton.clicked.connect(self.get_password_check_box_clicked)
        self.generatePasswordCHB.clicked.connect(self._generate_pw_clicked)

        # Create a ListModel for handling displaying passwords
        self.list_model = QStringListModel()

        # Fill QListView instrument with sites
        self._display_sites()
    
    def _display_sites(self):
        """
        Refresh sites list
        """
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

        # Bypass login - testing - insert mainPW
        # self.login_successful(password="")
        
        # Run the main loop
        self.app.exec()
        # self.close_application()
        
    def login_successful(self, password: str = ""):
        """
        This method is executed after correct login password is passed
        
        password is then used for decrypting
        """
        print("Login was successfull")
        # Close Login window
        self.login_window.close()
        
        # If no password is given - try to take it from password edit
        if not password:
            password = self.login_window.PasswordEdit.text()

        # Create window for PWManager and show it
        self.pw_manager_window = PWManagerWindow(password)
        self.pw_manager_window.show()
    
    def close_application(self):
        sys.exit()
        


if __name__ == "__main__":
    gui = MainGuiHandler()
