# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_pwmanager.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListView,
    QPushButton, QSizePolicy, QWidget)

class Ui_PasswordGUI(object):
    def setupUi(self, PasswordGUI):
        if not PasswordGUI.objectName():
            PasswordGUI.setObjectName(u"PasswordGUI")
        PasswordGUI.resize(558, 457)
        self.PasswordView = QListView(PasswordGUI)
        self.PasswordView.setObjectName(u"PasswordView")
        self.PasswordView.setGeometry(QRect(10, 40, 256, 371))
        self.GetPasswordButton = QPushButton(PasswordGUI)
        self.GetPasswordButton.setObjectName(u"GetPasswordButton")
        self.GetPasswordButton.setGeometry(QRect(320, 350, 161, 51))
        self.AddSiteButton = QPushButton(PasswordGUI)
        self.AddSiteButton.setObjectName(u"AddSiteButton")
        self.AddSiteButton.setGeometry(QRect(320, 80, 161, 61))
        self.SiteEdit = QLineEdit(PasswordGUI)
        self.SiteEdit.setObjectName(u"SiteEdit")
        self.SiteEdit.setGeometry(QRect(320, 50, 161, 22))
        self.label = QLabel(PasswordGUI)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(320, 30, 49, 16))

        self.retranslateUi(PasswordGUI)

        QMetaObject.connectSlotsByName(PasswordGUI)
    # setupUi

    def retranslateUi(self, PasswordGUI):
        PasswordGUI.setWindowTitle(QCoreApplication.translate("PasswordGUI", u"Form", None))
        self.GetPasswordButton.setText(QCoreApplication.translate("PasswordGUI", u"Copy - GET", None))
        self.AddSiteButton.setText(QCoreApplication.translate("PasswordGUI", u"Add", None))
        self.label.setText(QCoreApplication.translate("PasswordGUI", u"Site:", None))
    # retranslateUi

