from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
profile_url = "https://www.linkedin.com/in/sherlyn-saavedra/"
driver.get(profile_url)

try:
    name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".top-card-layout__title"))).text
    headline = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".top-card-layout__headline"))).text
    print("Name:", name)
    print("Headline:", headline)
except Exception as e:
    print("Unable to retrieve data:", e)

driver.quit()