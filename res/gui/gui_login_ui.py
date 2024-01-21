# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_login.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
import logo_rc


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(545, 528)
        LoginWindow.setStyleSheet(
            "QWidget {\n"
            "    background-color: #181818; /* Set the background color to a hex color code (e.g., yellow) */\n"
            "}"
        )
        self.verticalLayout = QVBoxLayout(LoginWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(
            30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.welcomeTo = QLabel(LoginWindow)
        self.welcomeTo.setObjectName("welcomeTo")
        font = QFont()
        font.setFamilies(["Cambria"])
        font.setPointSize(36)
        font.setUnderline(False)
        self.welcomeTo.setFont(font)
        self.welcomeTo.setStyleSheet("color: #fff")
        self.welcomeTo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.welcomeTo)

        self.exitButton = QPushButton(LoginWindow)
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setMaximumSize(QSize(30, 30))
        self.exitButton.setText("")
        icon = QIcon()
        icon.addFile(":/Button/xbutton.png", QSize(), QIcon.Normal, QIcon.Off)
        self.exitButton.setIcon(icon)
        self.exitButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_3.addWidget(self.exitButton)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.Logo = QLabel(LoginWindow)
        self.Logo.setObjectName("Logo")
        self.Logo.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.Logo)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.PasswordEdit = QLineEdit(LoginWindow)
        self.PasswordEdit.setObjectName("PasswordEdit")
        font1 = QFont()
        font1.setFamilies(["Cambria"])
        font1.setPointSize(18)
        self.PasswordEdit.setFont(font1)
        self.PasswordEdit.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: rgba(255, 0, 0, 0); /* Completely transparent background */\n"
            "    border: 3px solid transparent; /* Visible 3px transparent border */\n"
            "    border-color: blue;\n"
            "    border-radius: 23px;\n"
            "    padding: 15px;\n"
            "    color: white;\n"
            "    min-width: 300%;\n"
            "}\n"
            "\n"
            "QLineEdit:hover {\n"
            "    background-color: rgba(30, 30, 30, 0.2);\n"
            "}\n"
            ""
        )
        self.PasswordEdit.setInputMethodHints(
            Qt.ImhHiddenText
            | Qt.ImhNoAutoUppercase
            | Qt.ImhNoPredictiveText
            | Qt.ImhSensitiveData
        )
        self.PasswordEdit.setEchoMode(QLineEdit.Password)
        self.PasswordEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.PasswordEdit)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.LoginButton = QPushButton(LoginWindow)
        self.LoginButton.setObjectName("LoginButton")
        font2 = QFont()
        font2.setFamilies(["Cambria"])
        font2.setPointSize(26)
        self.LoginButton.setFont(font2)
        self.LoginButton.setStyleSheet(
            "QPushButton {\n"
            "    border-radius: 23px;\n"
            "    padding: 15px; /* Adjust padding as needed */\n"
            "    background-color: rgba(255, 0, 0, 0);\n"
            "    color: white;\n"
            "    border: 3px solid;\n"
            "    border-image: linear-gradient(to right, #ff6b6b, #5564eb); /* Gradient color border */\n"
            "    min-width: 200%; /* Adjust width as needed */\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgba(0, 0, 0, 0.2); /* Semi-transparent background on hover */\n"
            "}\n"
            ""
        )

        self.horizontalLayout_2.addWidget(self.LoginButton)

        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.SetPasswordText = QLabel(LoginWindow)
        self.SetPasswordText.setObjectName("SetPasswordText")
        self.SetPasswordText.setEnabled(True)
        font3 = QFont()
        font3.setFamilies(["Cambria"])
        font3.setPointSize(12)
        font3.setBold(False)
        self.SetPasswordText.setFont(font3)
        self.SetPasswordText.setStyleSheet("QLabel {\n" "    color: red;\n" "}")
        self.SetPasswordText.setAlignment(Qt.AlignCenter)
        self.SetPasswordText.setOpenExternalLinks(False)

        self.verticalLayout.addWidget(self.SetPasswordText)

        QWidget.setTabOrder(self.PasswordEdit, self.LoginButton)
        QWidget.setTabOrder(self.LoginButton, self.exitButton)

        self.retranslateUi(LoginWindow)

        QMetaObject.connectSlotsByName(LoginWindow)

    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(
            QCoreApplication.translate("LoginWindow", "Form", None)
        )
        self.welcomeTo.setText(
            QCoreApplication.translate("LoginWindow", "WELCOME TO", None)
        )
        self.Logo.setText(
            QCoreApplication.translate(
                "LoginWindow",
                '<html><head/><body><p><img src=":/logo/logo.png" width="400" height="200"></p></body></html>',
                None,
            )
        )
        self.PasswordEdit.setInputMask("")
        self.PasswordEdit.setText("")
        self.PasswordEdit.setPlaceholderText(
            QCoreApplication.translate("LoginWindow", "PASSWORD", None)
        )
        self.LoginButton.setText(
            QCoreApplication.translate("LoginWindow", "Log in", None)
        )
        self.SetPasswordText.setText(
            QCoreApplication.translate(
                "LoginWindow", "No main password found in the DB, create new one!", None
            )
        )

    # retranslateUi
