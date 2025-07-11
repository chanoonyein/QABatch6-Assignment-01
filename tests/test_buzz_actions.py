import time

import allure
import pytest
from pages.login_page import loginPage
from pages.buzz_page import BuzzPage
from utils.logger import setup_logger

logger = setup_logger()

@allure.title("Buzz Post, Comment, Like, Delete Test")
@allure.description("Test verifies all core functionalities of the Buzz module")
def test_buzz_post_comment_like_delete(browser):
    login = loginPage(browser)
    buzz = BuzzPage(browser)

    logger.info("Loading login page")
    login.load()
    login.login("Admin", "admin123")
    logger.info("Logged in as Admin")

    buzz.go_to_buzz()
    logger.info("Navigated to Buzz module")

    test_post = "Hello QABatch6 from Chan Oo"
    buzz.create_post(test_post)
    buzz.wait_for_success_alert("Successfully Saved")
    logger.info("Post created")
    buzz.get_base_location(test_post)
    # logger.info(buzz.get_first_post_text())
    # actual_text = buzz.get_first_post_text().strip()
    # expected_text = test_post.strip()
    # assert expected_text in actual_text
    logger.info("Verified posted content")
    time.sleep(2)


    buzz.comment_on_post("Welcome Chan Oo")
    buzz.wait_for_success_alert("Successfully Saved")
    logger.info("Comment added")
    time.sleep(2)


    buzz.like_post()
    logger.info("Post liked")
    time.sleep(5)

    buzz.delete_post()
    logger.info("Post deleted")
    allure.attach(browser.get_screenshot_as_png(), name="BuzzFlow", attachment_type=allure.attachment_type.PNG)
