from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
        else:
            print("Login failed. Please check your credentials or the login process.")
    finally:
        driver.quit()
