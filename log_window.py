from PySide2 import QtCore, QtGui

class Ui_LogWindow(object):

    def setupUi(self, LogWindow):
        LogWindow.setObjectName('LogWindow')
        LogWindow.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(LogWindow)
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.txtLog = QtGui.QTextBrowser(LogWindow)
        self.txtLog.setObjectName('txtLog')
        self.verticalLayout.addWidget(self.txtLog)
        self.progressBar = QtGui.QProgressBar(LogWindow)
        self.progressBar.setProperty('value', 24)
        self.progressBar.setObjectName('progressBar')
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.retranslateUi(LogWindow)
        QtCore.QMetaObject.connectSlotsByName(LogWindow)

    def retranslateUi(self, LogWindow):
        LogWindow.setWindowTitle(QtGui.QApplication.translate('LogWindow', 'Log', None, QtGui.QApplication.UnicodeUTF8))
