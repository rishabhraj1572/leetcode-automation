from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pyautogui
import requests
from cookies import *

# question_link="https://leetcode.com/problems/merge-two-sorted-lists"
# question_link=input("Enter Question Link : ")

def login():
    LOGIN_EMAIL = "LEETCODE_EMAIL"
    LOGIN_PASSWORD = "LEETCODE_PASS"
    LOGIN_URL = "https://leetcode.com/accounts/login/"
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(LOGIN_URL)
        
        wait = WebDriverWait(driver, 10)
        email_input = wait.until(EC.presence_of_element_located((By.ID, "id_login")))
        
        email_input.clear()
        email_input.send_keys(LOGIN_EMAIL)

        password_input = wait.until(EC.presence_of_element_located((By.ID, "id_password")))
        password_input.clear()
        password_input.send_keys(LOGIN_PASSWORD)

        password_input.send_keys(Keys.RETURN)

        time.sleep(5)

        if "https://leetcode.com/" in driver.current_url:
            print("Login successful!")
            cookies = driver.get_cookies()
            with open("cookies.txt", "w") as file:
                for cookie in cookies:
                    file.write(f"{cookie['name']} = {cookie['value']}\n")
            print("Cookies have been saved to cookies.txt.")
            get_questions()
        else:
            print("Login failed. Please check your credentials or the login process.")
    finally:
        driver.quit()

def get_questions():    
    import requests
    url = "https://leetcode.com/graphql/"
    headers = {
        "Content-Type": "application/json",
        "cookie":f'{get_cookies_content_with_semicolon("cookies.txt")}',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }

    payload = {
        "query": """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
                ) {
                    total: totalNum
                    questions: data {
                        acRate
                        difficulty
                        freqBar
                        frontendQuestionId: questionFrontendId
                        isFavor
                        paidOnly: isPaidOnly
                        status
                        title
                        titleSlug
                        topicTags {
                            name
                            id
                            slug
                        }
                        hasSolution
                        hasVideoSolution
                    }
                }
            }
        """,
        "variables": {
            "categorySlug": "all-code-essentials",
            "skip": 0,
            "limit": 50,
            "filters": {}
        },
        "operationName": "problemsetQuestionList"
    }
    response = requests.post(url, json=payload, headers=headers)

    response_json=response.json()
    questions = response_json["data"]["problemsetQuestionList"]["questions"]

    count = 0
    for question in questions:
        if question["status"] is None:
            question = f"https://leetcode.com/problems/{question['titleSlug']}"
            # print(f"https://leetcode.com/problems/{question['titleSlug']}")
            solve(question)

            count += 1
            if count == 3:
                break

def solve(question_link):
    cookies = parse_cookies_from_file('cookies.txt')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(question_link)
    for name, value in cookies.items():
            driver.add_cookie({'name': name, 'value': value})

    driver.refresh()


    wait = WebDriverWait(driver, 10)
    code_area = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "view-lines")))

    driver.execute_script("arguments[0].scrollIntoView(true);", code_area)
    code_area.click()

    def find_code(text):
        pattern = r'```cpp(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            code = matches[0].strip()
            return code
        else:
            print('no code found')

    import g4f
    from g4f.client import Client
    import re


    def GPT(question_link):
        client = Client()

        message = f'solve this leetcode question in c++ and give only class Solution snippet : {question_link}'
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"{message}"}],
        )
        # print(response.choices[0].message.content)
        return find_code(response.choices[0].message.content)

    code = f"""
    [C++]
    {GPT(question_link)}
    [/C++]
    """

    # JavaScript to parse and set the value in the Monaco Editor
    js_code = """
    function parseCode(code) {
        if (code.indexOf('[C++]') > -1) {
            const start = code.indexOf('[C++]') + '[C++]'.length;
            let end = null;
            if (code.indexOf("[/C++]") > -1) {
                end = code.indexOf("[/C++]");
            }
            return (end) ? code.slice(start, end) : code.slice(start);
        } else {
            const codeblock = /```\s*([^]+?.*?[^]+?[^]+?)```/g;
            const match =  codeblock.exec(code);
            if (match) {
                return match[1];
            } else {
                return code;
            }
        }
    }

    let parsedSourceCode = parseCode(arguments[0]);
    window.monaco.editor.getModels()[0].setValue(parsedSourceCode);
    """
    driver.execute_script(js_code, code)
    time.sleep(5)
    # pyautogui.hotkey('ctrl', 'enter')
    submit_button = driver.find_element(By.CSS_SELECTOR, '[data-e2e-locator="console-submit-button"]')
    submit_button.click()

    time.sleep(20)


login()
