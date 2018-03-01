from PySide import QtCore, QtGui # Import the PySide module we'll need
import sys # We need sys so that we can pass argv to QApplication
import bs, canvas_driver #import WebDriver, scraper files
import mainwindow, login_dialog  #import UI py files created with pyuic/QT Designer
# This file holds our MainWindow and all design related things
# it also keeps events etc that we defined in Qt Designer

class LoginWindow(QtGui.QDialog, login_dialog.Ui_LoginBox):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.btnCancel.clicked.connect(self.closeApp)
        self.btnLogin.clicked.connect(self.store)

    # exit
    def closeApp(self):
        sys.exit()

    # gets credentials and checks, then calls openMain if valid
    def store(self):
        if self.lineEmail.text() != "" and self.linePw.text() != "":
            global email
            email = self.lineEmail.text()
            global pw
            pw = self.linePw.text()
            self.hide()
            self.openMain()
        else:
            print("Invalid credentials.")

    # function to open main window as child after correct login
    def openMain(self):
        # self.hide()
        global form
        form = MainApp()
        form.show()

class MainApp(QtGui.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        # Click to execute function
        # self.btnScrape.clicked.connect(self.scrape_page)
        # self.btnLogin.clicked.connect(self.login)
        self.actionExit.triggered.connect(self.closeApp)
        self.actionLogout.triggered.connect(self.logout)

        # exit
    def closeApp(self):
        sys.exit()

    def logout(self):
        self.close()
        global dialog
        dialog.show()

    def login(self):
        self.lineUname.clear()
        self.linePw.clear()
        uname = self.lineUname.text()
        pw = self.linePw.text()
        a_url = "http://192.168.156.2:3000/courses/1/quizzes/1?module_item_id=1"
        bs.login(self.get_arg_url(), uname, pw, a_url)

    def get_arg_url(self):
        return self.lineURL.text()

    def scrape_page(self):
        self.hide()
        # arg_url = "http://192.168.156.2:3000/login/canvas"
        # self.listWidget.clear() # clear box
        # href_list = bs.grab_hrefs(self.get_arg_url())
        # for href in href_list:
        #     self.listWidget.addItem(href) # call scraping and list all hrefs on page

def main():
    email = ""
    pw = ""
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    global dialog
    dialog = LoginWindow()
    dialog.show()
    # form.show()                         # Show the form
    app.exec_()                         # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
