from selenium.webdriver.common.by import By


def login(driver, base_url, username, password):
    driver.get(f"{base_url}/login.html")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-btn").click()
    return driver.find_element(By.ID, "flash").text
