import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def browser():
    # remove comments from below code to run on jenken
    # options = Options()
    # options.add_argument("--headless=new")
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # comment for jenkin
    driver.maximize_window() # comment for jenkin
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("browser")
        if driver:
            test_name = item.name
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
            driver.save_screenshot(path)
            print(f"\n[Screenshot saved]: {path}")
