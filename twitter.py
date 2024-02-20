from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

twitterURL = "https://twitter.com/i/flow/login"

def exec(driver: WebDriver, credentials: dict) -> None:
    driver.get(twitterURL)

    usernameInput = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@autocomplete=\"username\"]")))
    usernameInput.send_keys(credentials["username"])

    nextButton = driver.find_element(By.XPATH, "//div[@role=\"button\" and @class=\"css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-usiww2 r-13qz1uu r-2yi16 r-1qi8awa r-ymttw5 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l\"]")
    nextButton.click()

    passwordInput = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@autocomplete=\"current-password\"]")))
    passwordInput.send_keys(credentials["password"])

    signInButton = driver.find_element(By.XPATH, "//div[@role=\"button\" and @data-testid=\"LoginForm_Login_Button\"]")
    signInButton.click()