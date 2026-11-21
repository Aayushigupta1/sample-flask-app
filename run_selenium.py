from selenium import webdriver
from selenium.webdriver.common.by import By

# Open Chrome browser
driver = webdriver.Chrome()

try:
    # Test 1: Open Flask application
    driver.get("http://127.0.0.1:5000")

    assert "Welcome to New Dashboard" in driver.page_source

    print("TEST 1 PASSED: Home page loaded successfully")

    # Test 2: Check feature flag
    driver.get("http://127.0.0.1:5000/feature-status")

    status = driver.find_element(By.TAG_NAME, "body").text

    assert '"new_feature":true' in status

    print("TEST 2 PASSED: Feature flag is enabled")

    # Test 3: Check health endpoint
    driver.get("http://127.0.0.1:5000/health")

    health = driver.find_element(By.TAG_NAME, "body").text

    assert "Application Running" in health

    print("TEST 3 PASSED: Health check successful")

finally:
    driver.quit()