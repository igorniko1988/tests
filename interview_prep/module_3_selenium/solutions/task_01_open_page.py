def get_title(driver, base_url):
    driver.get(f"{base_url}/login.html")
    return driver.title
