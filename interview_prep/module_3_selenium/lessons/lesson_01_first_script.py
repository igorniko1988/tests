from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

wait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=(Exception,))

def test_check_open_page():
    driver.get('https://www.selenium.dev/')
    driver.close()
    wait.until(EC.visibility_of_all_elements_located(By.ID,'sadsadsadas'))
    driver.find_element(By.ID, 'asdasdas')