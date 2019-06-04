from PySide2 import QtCore, QtGui, QtWidgets # Import the PySide modules
import sys, logging #need sys so that we can pass argv to QApplication
import os, datetime
import bs, canvas_driver #import WebDriver, scraper files
import mainwindow, login_dialog, log_window  #import UI py files created with pyuic/QT Designer

# class textStream(object):
    # def write(self, text):


class LogThread(QtCore.QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        sys.stdout = sys.__stdout__
        self.wait()

    def run(self):
        print("something")
        sys.stdout = QTextStream(printed_text=self.normalOutputWritten)

class LoginWindow(QtWidgets.QDialog, login_dialog.Ui_LoginBox):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.btnCancel.clicked.connect(self.closeApp)
        self.btnLogin.clicked.connect(self.store)
        self.cbDev.clicked.connect(self.dev_cred)

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
            # self.openLogWindow()
            self.login_canvas(email, pw)
            self.hide()
            self.openMain()
        else:
            print("Invalid credentials.")

    def dev_cred(self):
        if self.cbDev.isChecked() == True:
            self.lineEmail.clear()
            self.lineEmail.setText("admin@canvasdev.net")
            self.linePw.clear()
            self.linePw.setText("password")
            self.lineURL.clear()
            self.lineURL.setText("http://192.168.156.2:3000/")
        else:
            self.lineEmail.clear()
            self.linePw.clear()
            self.lineURL.clear()
            self.lineURL.setText("https://ufl.instructure.com/")

    def login_canvas(self, uname, pw):
        global drv
        global driver_choice
        driver_choice = self.cmbDriver.currentIndex()
        dev = False
        URL = self.lineURL.text()
        if self.cbDev.isChecked() == True:
            dev = True
            # uname = "admin@canvasdev.net"
            # pw = "password"
        drv = canvas_driver.init(driver_choice, dev, URL)
        rname = uname
        canvas_driver.login(drv, uname, pw, rname)

    def openLogWindow(self):
        global dialog
        dialog = LogWindow()
        dialog.show()

    # function to open main window as child after correct login
    def openMain(self):
        # self.hide()
        global form
        form = MainApp()
        form.show()

class LogWindow(QtWidgets.QDialog, log_window.Ui_LogWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

class MainApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
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
        self.populate_courses() # pre-populate the courses list
        self.btnCoursesConf.clicked.connect(self.select_course)
        self.btnQuizzesConf.clicked.connect(self.select_quiz)
        self.btnRegrade.clicked.connect(self.regrade)
        self.btnEdit.clicked.connect(self.edit_quiz)
        self.listQuestions.currentItemChanged.connect(self.enable_regrade)
        self.listQuestions.currentItemChanged.connect(self.disable_edit)
        self.listCourses.currentItemChanged.connect(self.disable_regrade)
        self.listCourses.currentItemChanged.connect(self.disable_edit)
        self.listQuizzes.currentItemChanged.connect(self.disable_regrade)
        self.listQuizzes.currentItemChanged.connect(self.enable_edit)

    def closeEvent(self, event):
        print("Closing")
        self.closeApp()
        self.destory()

    # exit
    def closeApp(self):
        global drv
        canvas_driver.close_driver(drv)
        sys.exit()

    def logout(self):
        global drv
        canvas_driver.close_driver(drv)
        self.close()
        global dialog
        dialog.show()

    def enable_regrade(self):
        self.btnRegrade.setDisabled(False)

    def disable_regrade(self):
        self.btnRegrade.setDisabled(True)

    def enable_edit(self):
        self.btnEdit.setDisabled(False)

    def disable_edit(self):
        self.btnEdit.setDisabled(True)

    def populate_courses(self):
        global drv
        canvas_driver.go_courses(drv)
        courses = canvas_driver.get_courses(drv)
        for course in courses:
            self.listCourses.addItem(course.text)

    def select_course(self):
        global drv
        # if self.listQuizzes.count() > 0:
        self.listQuizzes.clear()
        self.listQuestions.clear()
        canvas_driver.go_courses(drv)
        selected_course = self.listCourses.currentItem().text()
        canvas_driver.select_course(drv, selected_course)
        self.populate_quizzes()

    def populate_quizzes(self):
        global drv
        self.listQuizzes.clear()
        canvas_driver.go_quizzes(drv)
        quizzes = canvas_driver.get_quizzes(drv)
        for quiz in quizzes:
            self.listQuizzes.addItem(quiz.text)

    def edit_quiz(self):
        global drv
        self.listQuestions.clear()
        canvas_driver.go_quizzes(drv)
        selected_quiz = self.listQuizzes.currentItem().text()
        canvas_driver.select_course(drv, selected_quiz)

    def select_quiz(self):
        global drv
        # if self.listQuestions.count() > 0:
        self.listQuestions.clear()
        canvas_driver.go_quizzes(drv)
        selected_quiz = self.listQuizzes.currentItem().text()
        canvas_driver.select_course(drv, selected_quiz)
        self.populate_questions()

    def go_edit(self):
        global drv
        canvas_driver.go_edit(drv)

    def populate_questions(self):
        global drv
        self.listQuestions.clear()
        canvas_driver.go_questions(drv)
        print("Course selected: " + self.listCourses.currentItem().text())
        print("Quiz selected: " + self.listQuizzes.currentItem().text())
        questions = canvas_driver.get_question_names(drv)
        for question in questions:
            if question != "":
                self.listQuestions.addItem(question)

    def regrade(self):
        global drv
        # need to consider case where more than one question is selected
        # test if selectedItems() always returns list, if so then you know what to do
        # selected_question = self.listQuestions.currentItem().text()
        selected_questions_raw = self.listQuestions.selectedItems()
        selected_questions = []
        selected_questions_types = []
        selected_questions_ids = []
        print("Questions selected:")
        for q in selected_questions_raw:
            question_type = canvas_driver.get_question_type(drv, q.text())
            if canvas_driver.check_supported(question_type) == True:
                selected_questions.append(q.text())
                q_id = canvas_driver.get_question_id(drv, q.text())
                selected_questions_ids.append(q_id)
                selected_questions_types.append(question_type)
                print(q.text() + " will be regraded.")
            else:
                print(q.text() + " is of an unsupported type. No regrading will be carried out.")
        if len(selected_questions) > 0:
            print("------------------------------------------------------")
            print("Valid questions selected. Beginning regrading process.")
            print("------------------------------------------------------")
            list_answers = canvas_driver.get_answers_multiple(drv, selected_questions, selected_questions_types, selected_questions_ids)
            print("------------------------------------------------------")
            print("Answers retrieved. Continuing.")
            print("------------------------------------------------------")
            canvas_driver.go_moderate_regrade(drv, selected_questions_ids, list_answers, selected_questions_types)
        else:
            print("No valid questions selected. No further actions taken.")
            # print(q_number)
            # print(question_type)
        # q_number = canvas_driver.get_question_number(drv, selected_question)
        # need function for identifying type of question
        # question_type = canvas_driver.get_question_type(drv, selected_question)
        # call appropriate function depending on question type, or indicate unsupported
        # for i in range(len(selected_questions)):
        #     if "multiple_dropdowns_question" in selected_questions_types[i]:
        #         print("Question is a multiple dropdown question. Beginning regrading.")
        #         q_type = "md"
        #         # answers = canvas_driver.get_answers(drv, selected_question, q_type)
        #         # canvas_driver.go_moderate_regrade(drv, q_number, answers, q_type)
        #     elif "multiple_answers_question" in selected_questions_types[i]:
        #         print("Question is a multiple answer question. Beginning regrading.")
        #         q_type = "ma"
        #         # answers = canvas_driver.get_answers(drv, selected_question, q_type)
        #         # canvas_driver.go_moderate_regrade(drv, q_number, answers, q_type)
        #     else:
        #         print("Question type unsupported.")

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
    cwd = os.getcwd()
    # sys.stdout = open(cwd + "\log.txt", "w")
    print("*** " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " ***")
    email = ""
    pw = ""
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    global dialog
    global drv
    global driver_choice
    drv = ""
    dialog = LoginWindow()
    dialog.show()
    driver_choice = ""
    # form.show()                         # Show the form
    app.exec_()                         # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
