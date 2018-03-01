from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# This file contains all functions relating to WebDriver and its automation and scraping.

# put discrete functionality into functions so that they can be called from UI events seperately
# always use driver as an argument to keep the same driver in play!
def init():
    driver = webdriver.Firefox()
    driver.get("http://192.168.156.2:3000/login/canvas")
    driver.implicitly_wait(3)
    assert "Canvas" in driver.title
    return driver

def login(driver, uname, pw, rname):
    uname = "admin@canvasdev.net"
    pw = "password"
    rname = "admin@canvasdev.net"

    #authenticate with info from user
    login_field = driver.find_element_by_name("pseudonym_session[unique_id]")
    pw_field = driver.find_element_by_name("pseudonym_session[password]")

    login_field.clear()
    pw_field.clear()

    login_field.send_keys(uname)
    pw_field.send_keys(pw)
    pw_field.send_keys(Keys.RETURN)

    # login_button = driver.find_element_by_class_name("Button Button--login")
    # login_button.click()

    #verify success
    # profile_sidebar = driver.find_element_by_css_selector("a.ic-app-header__menu-list-link")
    # profile_sidebar.click()

    # find Dashboard heading to force implicit wait
    dashboard_header = driver.find_element_by_xpath("//h1[@class='ic-Dashboard-header__title']")
    print(driver.current_url)
    settings_url = "http://192.168.156.2:3000/profile/settings"
    driver.get(settings_url)
    print(driver.current_url)

    # profile_name = driver.find_element_by_id("global_nav_profile_display_name")
    # if profile_name.text() == rname:
    assert rname in driver.title
    print("Login successful. Welcome " + rname + ".")

def select_course(driver, rootURL, short_name):
    # courses_sidebar = driver.find_element_by_id("global_nav_courses_link")
    # courses_sidebar.click()
    driver.get(rootURL + "/courses")
    target_course = driver.find_element_by_partial_link_text(short_name)
    target_course.click()

def go_quizzes(driver):
    quizzes_link = driver.find_element_by_partial_link_text("Quizzes")
    quizzes_link.click()

def select_quiz(driver, quiz_name):
    target_quiz = driver.find_elements_by_partial_link_text(quiz_name)
    target_quiz[0].click()
    # print(*target_quiz, sep='\n')

# goes to edit screen and "Questions" tab of current quiz, showing question details
def go_edit(driver):
    # edit_link = driver.find_element_by_class_name("a.btn edit_assignment_link quiz-edit-button")
    print(driver.current_url)
    edit_link = driver.current_url + "/edit"
    driver.get(edit_link)
    edit_link = driver.find_element_by_partial_link_text("Questions")
    edit_link.click()
    show_details = driver.find_element_by_id("show_question_details")
    show_details.click()

# (hopefully temporary) function for hardcoded minimal functionality
def get_single_question(driver):
    # md_question = driver.find_element_by_xpath("//div[@class='answer_text'][contains(text(),'new answer 1')]")
    # print(md_question.text)
    # probably going to have to do some string manipulation in order to iteratively select this stuff
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    q_md = driver.find_element_by_xpath("//span[@class='name question_name'][contains(text(),'Q MD')]")
    q_md = wait.until(EC.visibility_of(q_md))
    # Elements must be scrolled into view before using actions!
    print(q_md.location_once_scrolled_into_view)
    xpath_edit_icon = "//div[@id='question_6']//div[@class='links']//a[@href='#']//i[@class='icon-edit standalone-icon']"
    q_edit_icon = driver.find_element_by_xpath(xpath_edit_icon)
    actions.move_to_element(q_md)
    # actions.move_to_element(q_edit_icon)
    # actions.click(q_edit_icon)
    actions.perform()
    # xpath_correct_answer = "//div[@class='answer answer_for_color1 correct_answer answer_idx_0']//table[@style='width: 100%; position: relative; _height: 10px; min-height: 10px;']//tbody//tr//td//div[@class='select_answer answer_type']//input[@type='text']"
    # xpath_correct_answer = "//div[@id='question_6']//div[@class='answer_text'][contains(text(),'new new answer 1')]"
    # correct_answer = driver.find_element_by_xpath(xpath_correct_answer)
    # actions.move_to_element(correct_answer)
    # actions.perform()
    # print(correct_answer.get_attribute("value"))
    # use dict or list to hold answer info from this quiz view
    # choice_answers_dict = dict([("choice 1", correct_answer), ("choice 2", correct_answer)])
    # ans1 = correct_answer.text
    # print(ans1)
    # answers = [ans1]
    xpath_correct_answers = "//div[@id='question_6']//div[contains(@class, 'correct_answer')]//div[@class='answer_text']"
    correct_answers_raw = driver.find_elements_by_xpath(xpath_correct_answers)
    # first correct answer for dropdown will always be visible
    correct_answers = [correct_answers_raw[0].text]
    answers_dropdown = driver.find_element_by_xpath("//div[@id='question_6']//div[@class='text']//div[@class='multiple_answer_sets_holder']//select[@class='blank_id_select']")
    select = Select(answers_dropdown)
    # select next option in dropdown, can throw this into a loop later
    select.select_by_index(1)
    correct_answers_raw = driver.find_elements_by_xpath(xpath_correct_answers)
    correct_answers.append(correct_answers_raw[1].text)
    # correct_answer = driver.find_element_by_xpath("//div[@class='answer_text'][contains(text(),'new answer 2')]")
    # print(correct_answer.text)
    # answers.append(correct_answer.text)
    # correct_answers = [correct_answers_raw[0].text]
    # attempt to deal with invisible elements displaying as blank strings (the way Selenium works)
    # for ans in correct_answers_raw:
    #     if ans.text != "":
    #         correct_answers.append(ans.text)
    #     else:
    #         select.select_by_index(1)
    #         correct_answers_raw = driver.find_elements_by_xpath(xpath_correct_answers)

    print("Answers list contains:")
    for ans in correct_answers:
        print(ans)
    # print(ans.text)
    # print("Stored answer value: " + correct_answer.text)
    return correct_answers

# take in correct_answers: list of answers from MD question
def regrade_single(driver, correct_answers):
    cancel_button = driver.find_element_by_id("cancel_button")
    cancel_button.click()
    moderate_link = driver.find_element_by_partial_link_text("Moderate This Quiz")
    moderate_link.click()
    student_link = driver.find_element_by_partial_link_text("Lana")
    student_link.click()
    q_6 = driver.find_element_by_xpath("//span[@class='name question_name'][contains(text(),'Question 6')]")
    print(q_6.location_once_scrolled_into_view)
    actions = ActionChains(driver)
    actions.move_to_element(q_6)
    actions.perform()
    # find the answers chosen by the student
    chosen_answers_xpath = "//div[@id = 'question_6']//div[contains(@title, 'You selected')]//div[@class = 'answer_text']"
    chosen_answers = driver.find_elements_by_xpath(chosen_answers_xpath)
    # for ans in chosen_answers:
        # print(ans.text)
    #compare to input list
    for i in range(len(correct_answers)):
        print("Correct answer: " + correct_answers[i] + ". Student answered: " + chosen_answers[i].text)
        if correct_answers[i] == chosen_answers[i].text:
            print("Student answered correctly. Regrade needed.")
        else:
            print("Student answered incorrectly. No regrade needed.")

# take in questions that need to be regraded as a list, along with the type of question
def get_all_questions(driver, questions):
    go_edit(driver)
    question = driver.find_element_by_xpath("//div[@id='question_6']")
    print(question.get_attribute('text'))

# do not rely on app to correct quiz, let user do so in Canvas natively
# def correct_quiz(driver):
    # print("Placeholder")

# if running file directly
if __name__ == '__main__':
    drv = init()
    login(drv, 1, 1, 1)
    select_course(drv, "http://192.168.156.2:3000", "PRC2000")
    go_quizzes(drv)
    select_quiz(drv, "Quiz 1")
    go_edit(drv)
    correct_answers = get_single_question(drv)
    regrade_single(drv, correct_answers)
    # drv.close()
