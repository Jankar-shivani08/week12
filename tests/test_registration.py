import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ---------- Locators (change these if your HTML uses different attributes) ----------
# at the top of tests/test_registration.py, after the imports:
USERNAME = (By.NAME, "username")     # or By.ID if you confirmed it
PASSWORD = (By.NAME, "pwd")
SUBMIT   = (By.NAME, "sb")
URL      = "http://127.0.0.1:5000/"  # change if your form is on /login, /register, etc.


@pytest.fixture
def setup_teardown():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager(driver_version="155.0.8059.85").install()
        ),
        options=options,
    )
    yield driver
    driver.quit()


def wait_for(driver, locator, timeout=10):
    """Wait until the element is present, then return it."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )


def get_alert_text(driver, timeout=10):
    WebDriverWait(driver, timeout).until(EC.alert_is_present())
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text


def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get(URL)

    wait_for(driver, USERNAME).clear()
    wait_for(driver, PASSWORD).send_keys("Password123")
    wait_for(driver, SUBMIT).click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get(URL)

    wait_for(driver, USERNAME).send_keys("John Doe")
    wait_for(driver, PASSWORD).clear()
    wait_for(driver, SUBMIT).click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get(URL)

    wait_for(driver, USERNAME).send_keys("Jane")
    wait_for(driver, PASSWORD).send_keys("abc1")
    wait_for(driver, SUBMIT).click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 characters long."


def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get(URL)

    wait_for(driver, USERNAME).send_keys("Alice")
    wait_for(driver, PASSWORD).send_keys("abc123")
    wait_for(driver, SUBMIT).click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/submit"))
    assert "/submit" in driver.current_url

    body_text = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    ).text
    assert "Hello, Alice! Welcome to the website" in body_text