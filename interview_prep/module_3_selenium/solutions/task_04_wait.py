from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_dynamic_text(driver, base_url):
    driver.get(f"{base_url}/dynamic.html")
    driver.find_element(By.ID, "start").click()
    result = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "result"))
    )
    return result.text
