from selenium.webdriver.common.by import By


def find_username_by_id(driver):
    return driver.find_element(By.ID, "username")


def find_login_button_by_css(driver):
    return driver.find_element(By.CSS_SELECTOR, "button.btn.primary")


def find_help_link_by_xpath(driver):
    return driver.find_element(By.XPATH, "//a[text()='Help']")


def find_password_by_testid(driver):
    return driver.find_element(By.CSS_SELECTOR, "[data-testid='password']")
