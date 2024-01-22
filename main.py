# from res import MainGuiHandler
from app import Presenter
from pieceful import get_piece
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    # main_gui = MainGuiHandler()

    app = get_piece("app", QApplication)
    presenter = get_piece("presenter", Presenter)
    presenter.show_window()
    app.exec()
