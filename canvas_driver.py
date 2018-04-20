from urllib.parse import urlparse
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# This file contains all functions relating to WebDriver and its automation and scraping.

# put discrete functionality into functions so that they can be called from UI events seperately
# always use driver as an argument to keep the same driver in play!
def init(driver_choice, dev, URL):
    # driver_choice is the type of driver chosen by the user at login?
    driver = ""
    if driver_choice == 0:
        driver = webdriver.Firefox()
    elif driver_choice == 1:
        driver = webdriver.Chrome()
    elif driver_choice == 2:
        print("Headless")
    driver.implicitly_wait(5)
    if dev == True:
        driver.get("http://192.168.156.2:3000/login/canvas")
        assert "Canvas" in driver.title
    else:
        driver.get(URL)
    return driver

def close_driver(driver):
    driver.close()

def get_base_url(driver):
    current_url = driver.current_url
    parsed_url = urlparse(current_url)
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
    return base_url

def login(driver, uname, pw, rname):
    # uname = "admin@canvasdev.net"
    # pw = "password"
    # rname = "admin@canvasdev.net"

    #authenticate with info from user
    if "login.ufl.edu" in get_base_url(driver):
        print("UF Canvas detected.")
        login_field = driver.find_element_by_xpath("//input[@id='username']")
        pw_field = driver.find_element_by_xpath("//input[@id='password']")
    else:
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
    # wait = WebDriverWait(driver, 10)
    # wait = WebDriverWait(driver, 10)
    try:
        dashboard_header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='ic-Dashboard-header__title']")))
        # element = WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.ID, "myDynamicElement"))
        # )
    except NoSuchElementException:
        print("Login process failed. Please restart and try again.")
        driver.close()
        sys.exit()
    # dashboard_header = wait.until(EC.visibility_of(dashboard_header))
    # print(dashboard_header.location_once_scrolled_into_view)
    # dashboard_header = wait.until(EC.visibility_of(dashboard_header))
    # footer = driver.find_element_by_partial_link_text("Open Source LMS")
    # print(driver.current_url)
    settings_url = get_base_url(driver) + "profile/settings"
    driver.get(settings_url)
    # print(driver.current_url)

    # profile_name = driver.find_element_by_id("global_nav_profile_display_name")
    # if profile_name.text() == rname:
    assert "Settings" in driver.title

    print("------------------------------------------------------")
    print("Login successful. Welcome " + rname + ".")
    print("------------------------------------------------------")


def go_courses(driver):
    driver.get(get_base_url(driver) + "courses")

# returns list of courses
# should only be called on the "All courses" page: .../courses
def get_courses(driver):
    courses = driver.find_elements_by_xpath("//span[@class = 'name']")
    return courses

def select_course(driver, short_name):
    # courses_sidebar = driver.find_element_by_id("global_nav_courses_link")
    # courses_sidebar.click()
    # driver.get(rootURL + "/courses")
    target_course = driver.find_element_by_partial_link_text(short_name)
    target_course.click()

def go_quizzes(driver):
    quizzes_link = driver.find_element_by_partial_link_text("Quizzes")
    quizzes_link.click()

def get_quizzes(driver):
    quizzes = driver.find_elements_by_xpath("//a[@class='ig-title']")
    return quizzes

def select_quiz(driver, quiz_name):
    target_quiz = driver.find_elements_by_partial_link_text(quiz_name)
    target_quiz[0].click()
    # print(*target_quiz, sep='\n')

# goes to edit screen and "Questions" tab of current quiz, showing question details
def go_questions(driver):
    # edit_link = driver.find_element_by_class_name("a.btn edit_assignment_link quiz-edit-button")
    # print(driver.current_url)
    edit_link = driver.current_url + "/edit"
    driver.get(edit_link)
    edit_link = driver.find_element_by_partial_link_text("Questions")
    edit_link.click()
    show_details = driver.find_element_by_id("show_question_details")
    show_details.click()

def get_question_names(driver):
    print("------------------------------------------------------")
    print("Searching for valid questions...")
    # actions = ActionChains(driver)
    # wait = WebDriverWait(driver, 10)
    # cancel_button = driver.find_element_by_xpath("//a[@id='cancel_button']")
    # wait.until(EC.visibility_of(cancel_button))
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # xpath_q = "//div[@class='display_question question multiple_dropdowns_question' or @class='display_question question multiple_answers_question']//span[@class='name question_name']"
    # xpath_q = "//span[@class='name question_name']/../.."
    xpath_all_q_id = "//span[@class='name question_name']/../.."
    # xpath_q_md = "//div[@class='display_question question multiple_dropdowns_question']"
    # xpath_q_ma = "//div[@class='display_question question multiple_answers_question']"
    # q_md = driver.find_elements_by_xpath(xpath_q_md)
    # q_ma = driver.find_elements_by_xpath(xpath_q_ma)
    # q_all = q_md + q_ma
    all_q_id = driver.find_elements_by_xpath(xpath_all_q_id)
    valid_q_names = []
    for q in all_q_id:
        if "multiple_answers_question" in q.get_attribute("class"):
            # print(q.find_element_by_xpath(".//span[@class='name question_name']").text)
            valid_q_name = q.find_element_by_xpath(".//span[@class='name question_name']").text
            valid_q_names.append(valid_q_name)
        if "multiple_dropdowns_question" in q.get_attribute("class"):
            # print(q.find_element_by_xpath(".//span[@class='name question_name']").text)
            valid_q_name = q.find_element_by_xpath(".//span[@class='name question_name']").text
            valid_q_names.append(valid_q_name)
    if len(valid_q_names) > 0:
        print("Valid questions found.")
        print("------------------------------------------------------")
        return valid_q_names
    else:
        print("No valid questions found.")

# returns the question id given a name. ID should be used to identify and find questions over all other methods.
def get_question_id(driver, q_name):
    # gets universal question id given name
    print("Retrieving question ID.")
    xpath_matching_q_id = "//span[@class='name question_name'][contains(text(), '" + q_name + "')]/../.."
    matching_q_id_raw = driver.find_element_by_xpath(xpath_matching_q_id)
    matching_q_id = matching_q_id_raw.get_attribute("id")
    return matching_q_id


def get_question_number(driver, question_name):
    questions_raw = get_questions(driver)
    # questions_raw is a list of Selenium WebElements, need to extract text
    questions = []
    for q in questions_raw:
        questions.append(q.text)
    q_number = questions.index(question_name)
    return q_number + 1

# returns question type via WebElement class attribute
def get_question_type(driver, q_name):
    print("Identifying question type...")
    xpath_matching_q_id = "//span[@class='name question_name'][contains(text(), '" + q_name + "')]/../.."
    matching_q_id_raw = driver.find_element_by_xpath(xpath_matching_q_id)
    q_type = matching_q_id_raw.get_attribute("class")
    # q_number = get_question_number(driver, question_name)
    # q_name_number = "question_" + str(q_number)
    # q = driver.find_element_by_xpath("//div[@id='" + q_name_number +"']")
    # q_type = q.get_attribute("class")
    print("Question is type: " + q_type)
    # print(type(q_type))
    return q_type

# get md answers given a question name. Maybe use index in questions list to make it easier?
def get_answers(driver, q_id, q_type):
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    xpath_q = "//div[@id='" + q_id + "']"
    # print(xpath_q)
    q = driver.find_element_by_xpath(xpath_q)
    q = wait.until(EC.visibility_of(q))
    temp = q.location_once_scrolled_into_view
    # q_number = questions.index(question_name)
    # q_number = get_question_number(driver, question_name)
    # q_name_number = "question_" + str(q_number)
    print("Question ID: " + q_id)
    xpath_edit_icon = "//div[@id='" + q_id + "']//div[@class='links']//a[@href='#']//i[@class='icon-edit standalone-icon']"
    q_edit_icon = driver.find_element_by_xpath(xpath_edit_icon)
    actions.move_to_element(q)
    actions.perform()
    xpath_correct_answers = "//div[@id='" + q_id + "']//div[contains(@class, 'correct_answer')]//div[@class='answer_text']"
    correct_answers_raw = driver.find_elements_by_xpath(xpath_correct_answers)
    correct_answers = []

    # for multiple dropdown questions
    if "multiple_dropdowns_question" in q_type:
        answers_dropdown = driver.find_element_by_xpath("//div[@id='" + q_id + "']//div[@class='text']//div[@class='multiple_answer_sets_holder']//select[@class='blank_id_select']")
        select = Select(answers_dropdown)
        # select next option in dropdown, can throw this into a loop later
        choices = [choice for choice in answers_dropdown.find_elements_by_tag_name("option")]
        # for choice in choices:
            # print(choice.get_attribute("value"))
        i = 0
        for choice in choices:
            select.select_by_value(choice.get_attribute("value"))
            correct_answers_raw = driver.find_elements_by_xpath(xpath_correct_answers)
            correct_answers.append(correct_answers_raw[i].text)
            # print("Grabbed answer choice.")
            i = i + 1

    # for multiple answer (checkbox) questions
    if "multiple_answers_question" in q_type:
        correct_answers_raw = driver.find_elements_by_xpath(xpath_correct_answers)
        i = 0
        for ans_raw in correct_answers_raw:
            correct_answers.append(correct_answers_raw[i].text)
            # print("Grabbed answer choice.")
            i = i + 1

    # verify answers
    print("Answers list contains:")
    for ans in correct_answers:
        print(ans)
    # return to quiz top page
    # cancel_button = driver.find_element_by_id("cancel_button")
    # cancel_button.click()
    return correct_answers

def get_answers_multiple(driver, s_q, s_q_types, s_q_ids):
    # Take in list of questions, get type of each question and put in another list
    # with the same index? Then call individual regrade functions already written in loop
    # List of list of correct answers
    list_correct_ans = []
    for i in range(len(s_q)):
        print("Grabbing answers for " + s_q[i])
        list_correct_ans.append(get_answers(driver, s_q_ids[i], s_q_types[i]))
    # return to the quiz top page
    cancel_button = driver.find_element_by_id("cancel_button")
    cancel_button.click()
    return list_correct_ans

# check if question type is supported
def check_supported(q_type):
    if "multiple_dropdowns_question" in q_type:
        return True
    elif "multiple_answers_question" in q_type:
        return True
    else:
        return False

# goes to moderate quiz page, then calls regrade for each valid student who has taken quiz
def go_moderate_regrade(driver, q_ids, list_correct_answers, q_types):
    print("*Beginning regrading.*")
    moderate_link = driver.find_element_by_partial_link_text("Moderate This Quiz")
    moderate_link.click()
    moderate_url = driver.current_url
    students = get_student_names(driver)
    for i, student in enumerate(students):
        student_link = driver.find_element_by_partial_link_text(student)
        print("*** Viewing student " + str(i+1) + " of " + str(len(students)) + ": "  + student + " ***")
        student_link.click()
        # if q_type =="md":
            # regrade(driver, q_number, correct_answers, q_type)
        regrade_multiple(driver, q_ids, list_correct_answers, q_types)
        # elif q_type == "ma":
            # print("MA question support coming soon.")
            # regrade(driver, q_number, correct_answers, q_type)
            # regrade_multiple(driver, q_numbers, list_correct_ans, q_types)
        # go_back_moderate(driver)
        driver.get(moderate_url)
    print("------------------------------------------------------")
    print("Regrading completed.")
    print("*** " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " ***")
    print("------------------------------------------------------")

def go_back_moderate(driver):
    back_to_quiz_link = driver.find_element_by_xpath("//a[contains(text(),'Back to Quiz')]")
    back_to_quiz_link.click()
    moderate_link = driver.find_element_by_partial_link_text("Moderate This Quiz")
    moderate_link.click()

# returns string list of valid student names in order listed order
def get_student_names(driver):
    print("Getting students.")
    student_links = driver.find_elements_by_xpath("//a[@class='student_name']")
    students = []
    for student in student_links:
        students.append(student.text)
    return students

def regrade(driver, q_id, correct_answers, q_type):
    print("Regrading function called.")
    # Q_name_number = "Question " + str(q_number + 1)
    # q_name_number = "question_" + str(q_number + 1)
    try:
        q = driver.find_element_by_xpath("//div[@id='" + q_id + "']")
    except NoSuchElementException:
        print("Question not found. Student did not receive this question.")
        print("Moving to next question or student.")
        return False
    q_name = driver.find_element_by_xpath("//div[@id='" + q_id + "']//span[@class='name question_name']").text
    print("Current question: " + q_name)
    temp = q.location_once_scrolled_into_view
    actions = ActionChains(driver)
    actions.move_to_element(q)
    actions.perform()
    # find the answers chosen by the student
    chosen_answers_xpath = "//div[@id = '" + q_id + "']//div[contains(@title, 'You selected')]//div[@class = 'answer_text']"
    chosen_answers = driver.find_elements_by_xpath(chosen_answers_xpath)
    #compare to input list. Need to implement if student answered right initial answer but wrong actual answer
    # check point value and compare to number of answer choices, distribute points accordingly
    q_points_raw = driver.find_element_by_xpath("//div[@id = '" + q_id + "']//span[@class = 'points question_points']")
    q_points = q_points_raw.text.split()[1]
    print("This question is worth " + q_points + " point(s).")

    # for multiple dropdown questions
    if "multiple_dropdowns_question" in q_type:
        print("There are " + str(len(correct_answers)) + " different answer choices.")
        points_per_choice = float(q_points) / float(len(correct_answers))
        print("Each answer choice is worth: " + str(round(points_per_choice, 2)))
        # check what kind of point regrade needs to happen
        regrade_counter = 0
        regrade_points = 0
        points_field = driver.find_element_by_xpath("//div[@id = '" + q_id + "']//input[@class = 'question_input']")
        # points_earned is a string
        points_earned = points_field.get_attribute("value")
        update_scores_button = driver.find_element_by_xpath("//button[@type='submit']")
        for i in range(len(correct_answers)):
            print("Correct answer: " + correct_answers[i] + ". Student answered: " + chosen_answers[i].text)
            if correct_answers[i] == chosen_answers[i].text:
                print("Student answered correctly.")
                regrade_counter = regrade_counter + 1
                regrade_points = points_per_choice * regrade_counter
                # print("Student received " + str(regrade_points) + " back on " + Q_name_number + ".")
            elif correct_answers[i] == chosen_answers[i].text and points_earned == q_points:
                print("Student answered correctly and received credit. No regrade needed.")
            elif points_earned != "0" and chosen_answers[i].text != correct_answers[i]:
                print("Student answered incorrectly.")
                # regrade_counter = regrade_counter - 1
                # regrade_points = points_per_choice * regrade_counter
                # print("Student deducted " + str(regrade_points) + " from " + Q_name_number + ".")
                # regrade_points = int(float(points_earned)) - regrade_points
                # print(str(regrade_points))
            else:
                print("Student answered incorrectly. No regrade needed.")
        round(regrade_points, 2)

    # for multiple answer (checkbox) type questions
    # each correct choice is worth total/correct_choices, each wrong subtracts that amount
    # but point value cannot drop below zero, obviously
    if "multiple_answers_question" in q_type:
        xpath_num_choices = "//div[@id = '" + q_id + "']//div[@class = 'answer_text']"
        num_choices = driver.find_elements_by_xpath(xpath_num_choices)
        #print("There are " + str(len(num_choices))) + " possible answer choices, but only " + str(len(correct_answers)) + " correct answers."
        points_per_choice = float(q_points) / float(len(correct_answers))
        print("Each answer choice is worth: " + str(round(points_per_choice, 2)))
        regrade_counter = 0
        regrade_points = 0
        points_field = driver.find_element_by_xpath("//div[@id = '" + q_id + "']//input[@class = 'question_input']")
        # points_earned is a string
        points_earned = points_field.get_attribute("value")
        update_scores_button = driver.find_element_by_xpath("//button[@type='submit']")
        # loop through each chosen choice and check correctness
        correct = False
        for ans in chosen_answers:
            for i in range(len(correct_answers)):
                if ans.text == correct_answers[i]:
                    correct = True
                    break
                else:
                    correct = False
            print("Correct answer: " + correct_answers[i] + ". Student answered: " + ans.text)
            if correct == True:
                print("Student answered correctly.")
                regrade_counter = regrade_counter + 1
            else:
                print("Student answered incorrectly.")
                regrade_counter = regrade_counter - 1

        regrade_points = regrade_counter * points_per_choice
        round(regrade_points, 2)
        if regrade_points < 0:
            regrade_points = 0

    round(regrade_points, 2)
    points_field.clear()
    points_field.send_keys(str(regrade_points))
    # update_scores_button = driver.find_element_by_xpath("//button[@type='submit']")
    # move the button into view
    actions = ActionChains(driver)
    # actions.move_to_element(update_scores_button)
    # print(update_scores_button.location_once_scrolled_into_view)
    actions.perform()
    # print(update_scores_button.location_once_scrolled_into_view)
    # update score
    # update_scores_button.click()
    # re-find field because page refreshed after updating score
    points_field = driver.find_element_by_xpath("//div[@id = '" + q_id + "']//input[@class = 'question_input']")
    points_earned = points_field.get_attribute("value")
    # print("Updating scores.")
    print("Student has earned " + points_earned + " on " + q_name + ".")
    return True

def update_score(driver):
    actions = ActionChains(driver)
    update_scores_button = driver.find_element_by_xpath("//button[@type='submit']")
    actions.move_to_element(update_scores_button)
    update_scores_button.location_once_scrolled_into_view
    update_scores_button.click()
    print("Updating scores.")

def regrade_multiple(driver, s_q_ids, list_correct_ans, s_q_type):
    for i in range(len(s_q_ids)):
        result = regrade(driver, s_q_ids[i], list_correct_ans[i], s_q_type[i])
        if result == False:
            continue
    update_score(driver)

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
    regrade_counter = 0
    for i in range(len(correct_answers)):
        print("Correct answer: " + correct_answers[i] + ". Student answered: " + chosen_answers[i].text)
        if correct_answers[i] == chosen_answers[i].text:
            print("Student answered correctly. Regrade needed.")
            regrade_counter = regrade_counter + 1
        else:
            print("Student answered incorrectly. No regrade needed.")

    # check point value and compare to number of answer choices, distribute points accordingly
    q_6_points_raw = driver.find_element_by_xpath("//div[@id = 'question_6']//span[@class = 'points question_points']")
    q_6_points = q_6_points_raw.text.split()[1]
    print("This question is worth " + q_6_points + " point(s).")
    print("There are " + str(len(correct_answers)) + " different answer choices.")
    points_per_choice = int(q_6_points) / int(len(correct_answers))
    print("Each answer choice is worth: " + str(points_per_choice))
    regrade_points = points_per_choice * regrade_counter
    points_field = driver.find_element_by_xpath("//div[@id = 'question_6']//input[@class = 'question_input']")
    points_field.send_keys(str(regrade_points))
    update_scores_button = driver.find_element_by_xpath("//button[@type='submit']")
    print("Student received " + str(regrade_points) + " back on question 6.")
    # update_scores_button.click()
    print("Updating scores.")


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
    go_courses(drv)
    select_course(drv, "PRC2000")
    go_quizzes(drv)
    select_quiz(drv, "Quiz 1")
    go_edit(drv)
    correct_answers = get_single_question(drv)
    regrade_single(drv, correct_answers)
    # drv.close()
