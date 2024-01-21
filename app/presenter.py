from .validator import validate_raw_password
from pieceful import Piece, get_piece
from typing import Annotated

from .model import Model
from .crypt_tools import CryptoManager
from .views.login import LoginWindow
from .constant import MAIN_PW
from .exceptions import PasswordError

from PySide6.QtWidgets import QApplication


@Piece("presenter")
class Presenter:
    def __init__(
        self,
        login_view: Annotated[LoginWindow, "login_view"],
        model: Annotated[Model, "model"],
        crypto_manager: Annotated[CryptoManager, "crypto_manager"],
    ) -> None:
        self.login_view = login_view
        self.model = model
        self.crypto_manager = crypto_manager

    def connect_login_view(self):
        self.login_view.connect_login_button(self.try_login)
        self.login_view.connect_exit_button(self.exit_app)

    def try_login(self) -> None:
        given_password = self.login_view.get_password()

        try:
            main_password_encrypted = self.model.get_password(MAIN_PW)
        except ValueError:
            print("Setup password than try it again")

            self.login_view.ui.LoginButton.clicked.disconnect(self.try_login)
            self.login_view.connect_login_button(self.setup_new_password)
            return

        main_password = self.crypto_manager.decrypt_string(main_password_encrypted)

        if given_password == main_password:
            print("success!")
            self.do_login()
        else:
            print("wrong password")

    def setup_new_password(self):
        given_password = self.login_view.get_password()
        try:
            validate_raw_password(given_password)
        except PasswordError as ex:
            print(ex)
            self.login_view.set_password_text(ex.msg)

        self.model.save_password(
            "MAINPW", self.crypto_manager.encrypt_string(given_password)
        )

    def do_login(self):
        self.exit_app()

    def exit_app(self):
        get_piece("app", QApplication).quit()
