from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

loginURL = "https://github.com/login"

def exec(driver: WebDriver, credentials: dict) -> None:
    # open url
    driver.get(loginURL)

    # find and file username input
    usernameInput = driver.find_element(By.NAME, "login")
    usernameInput.send_keys(credentials["username"])

    # find and file password input
    passwordInput = driver.find_element(By.NAME, "password")
    passwordInput.send_keys(credentials["password"])

    # find loign button and click it
    loginButton = driver.find_element(By.XPATH, "//input[@type=\"submit\"]")
    loginButton.click()