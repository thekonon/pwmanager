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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QLabel,
    QLineEdit, QListView, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_PasswordGUI(object):
    def setupUi(self, PasswordGUI):
        if not PasswordGUI.objectName():
            PasswordGUI.setObjectName(u"PasswordGUI")
        PasswordGUI.resize(617, 527)
        self.PasswordView = QListView(PasswordGUI)
        self.PasswordView.setObjectName(u"PasswordView")
        self.PasswordView.setGeometry(QRect(10, 40, 256, 411))
        self.formLayoutWidget = QWidget(PasswordGUI)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(290, 40, 291, 411))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 0))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.SiteEdit = QLineEdit(self.formLayoutWidget)
        self.SiteEdit.setObjectName(u"SiteEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.SiteEdit)

        self.checkBox = QCheckBox(self.formLayoutWidget)
        self.checkBox.setObjectName(u"checkBox")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.checkBox)

        self.AddSiteButton = QPushButton(self.formLayoutWidget)
        self.AddSiteButton.setObjectName(u"AddSiteButton")
        self.AddSiteButton.setMinimumSize(QSize(0, 50))

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.AddSiteButton)

        self.GetPasswordButton = QPushButton(self.formLayoutWidget)
        self.GetPasswordButton.setObjectName(u"GetPasswordButton")
        self.GetPasswordButton.setMinimumSize(QSize(0, 50))

        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.GetPasswordButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(4, QFormLayout.SpanningRole, self.verticalSpacer)

        self.SiteEdit_2 = QLineEdit(self.formLayoutWidget)
        self.SiteEdit_2.setObjectName(u"SiteEdit_2")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.SiteEdit_2)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(60, 0))

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        QWidget.setTabOrder(self.PasswordView, self.SiteEdit)
        QWidget.setTabOrder(self.SiteEdit, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.SiteEdit_2)
        QWidget.setTabOrder(self.SiteEdit_2, self.AddSiteButton)
        QWidget.setTabOrder(self.AddSiteButton, self.GetPasswordButton)

        self.retranslateUi(PasswordGUI)

        QMetaObject.connectSlotsByName(PasswordGUI)
    # setupUi

    def retranslateUi(self, PasswordGUI):
        PasswordGUI.setWindowTitle(QCoreApplication.translate("PasswordGUI", u"Form", None))
        self.label.setText(QCoreApplication.translate("PasswordGUI", u"Site:", None))
        self.checkBox.setText(QCoreApplication.translate("PasswordGUI", u"Generate random password", None))
        self.AddSiteButton.setText(QCoreApplication.translate("PasswordGUI", u"Add", None))
        self.GetPasswordButton.setText(QCoreApplication.translate("PasswordGUI", u"Copy - GET", None))
        self.label_2.setText(QCoreApplication.translate("PasswordGUI", u"Password", None))
    # retranslateUi

