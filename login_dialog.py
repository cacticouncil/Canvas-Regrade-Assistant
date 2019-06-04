# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_dialog.ui',
# licensing of 'login_dialog.ui' applies.
#
# Created: Tue Jun  4 17:08:03 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoginBox(object):
    def setupUi(self, LoginBox):
        LoginBox.setObjectName("LoginBox")
        LoginBox.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginBox)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(LoginBox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEmail = QtWidgets.QLineEdit(LoginBox)
        self.lineEmail.setObjectName("lineEmail")
        self.verticalLayout.addWidget(self.lineEmail)
        self.linePw = QtWidgets.QLineEdit(LoginBox)
        self.linePw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.linePw.setObjectName("linePw")
        self.verticalLayout.addWidget(self.linePw)
        self.label_3 = QtWidgets.QLabel(LoginBox)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lineURL = QtWidgets.QLineEdit(LoginBox)
        self.lineURL.setPlaceholderText("")
        self.lineURL.setObjectName("lineURL")
        self.verticalLayout.addWidget(self.lineURL)
        self.label_2 = QtWidgets.QLabel(LoginBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.cmbDriver = QtWidgets.QComboBox(LoginBox)
        self.cmbDriver.setObjectName("cmbDriver")
        self.cmbDriver.addItem("")
        self.cmbDriver.addItem("")
        self.verticalLayout.addWidget(self.cmbDriver)
        self.cbDev = QtWidgets.QCheckBox(LoginBox)
        self.cbDev.setObjectName("cbDev")
        self.verticalLayout.addWidget(self.cbDev)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnLogin = QtWidgets.QPushButton(LoginBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLogin.sizePolicy().hasHeightForWidth())
        self.btnLogin.setSizePolicy(sizePolicy)
        self.btnLogin.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnLogin.setObjectName("btnLogin")
        self.horizontalLayout.addWidget(self.btnLogin)
        self.btnCancel = QtWidgets.QPushButton(LoginBox)
        self.btnCancel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LoginBox)
        QtCore.QMetaObject.connectSlotsByName(LoginBox)

    def retranslateUi(self, LoginBox):
        LoginBox.setWindowTitle(QtWidgets.QApplication.translate("LoginBox", "Log In", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("LoginBox", "Enter your email and password for Canvas.", None, -1))
        self.lineEmail.setPlaceholderText(QtWidgets.QApplication.translate("LoginBox", "Email", None, -1))
        self.linePw.setPlaceholderText(QtWidgets.QApplication.translate("LoginBox", "Password", None, -1))
        self.label_3.setToolTip(QtWidgets.QApplication.translate("LoginBox", "A headless driver will not be visible at any time.", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("LoginBox", "Enter the root Canvas URL.", None, -1))
        self.lineURL.setText(QtWidgets.QApplication.translate("LoginBox", "https://ufl.instructure.com/", None, -1))
        self.label_2.setToolTip(QtWidgets.QApplication.translate("LoginBox", "A headless driver will not be visible at any time.", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("LoginBox", "Choose a web browser driver.", None, -1))
        self.cmbDriver.setItemText(0, QtWidgets.QApplication.translate("LoginBox", "Mozilla Firefox", None, -1))
        self.cmbDriver.setItemText(1, QtWidgets.QApplication.translate("LoginBox", "Google Chrome", None, -1))
        self.cbDev.setText(QtWidgets.QApplication.translate("LoginBox", "Dev Testing", None, -1))
        self.btnLogin.setText(QtWidgets.QApplication.translate("LoginBox", "Log In", None, -1))
        self.btnCancel.setText(QtWidgets.QApplication.translate("LoginBox", "Cancel", None, -1))

