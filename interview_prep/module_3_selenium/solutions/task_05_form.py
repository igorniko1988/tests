from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def select_country(driver, base_url, country_name):
    driver.get(f"{base_url}/form.html")
    select = Select(driver.find_element(By.ID, "country"))
    select.select_by_visible_text(country_name)
    return select.first_selected_option.text


def tick_agree(driver, base_url):
    driver.get(f"{base_url}/form.html")
    checkbox = driver.find_element(By.ID, "agree")
    if not checkbox.is_selected():
        checkbox.click()
    return checkbox.is_selected()


def get_items(driver, base_url):
    driver.get(f"{base_url}/form.html")
    return [li.text for li in driver.find_elements(By.CSS_SELECTOR, "li.item")]


def get_admin_name(driver, base_url):
    driver.get(f"{base_url}/form.html")
    cell = driver.find_element(By.XPATH, "//table[@id='users']//tr[td[2]='admin']/td[1]")
    return cell.text
