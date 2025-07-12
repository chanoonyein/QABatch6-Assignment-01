from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BuzzPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait= WebDriverWait(driver,10)

        # --- Locators ---
        self.BASE_LOCATION=''
        self.BUZZ_TAB = (By.XPATH, "//span[text()='Buzz']")
        self.POST_INPUT = (By.XPATH, '//textarea[@placeholder="What\'s on your mind?"]')
        self.POST_BUTTON = (By.XPATH, "//button[@type='submit']")
        # self.FIRST_POST_TEXT = (By.CSS_SELECTOR, ".orangehrm-buzz-post-body p")
        self.COMMENT_LINK = (By.XPATH, self.BASE_LOCATION+"//i[contains(@class,'bi-chat-text-fill')]")
        self.COMMENT_INPUT = (By.XPATH, self.BASE_LOCATION+"//input[@placeholder='Write your comment...']")
        self.LIKE_BUTTON = (By.XPATH, self.BASE_LOCATION+ "//*[local-name()='svg']")
        self.LIKED_STATE=(By.XPATH, self.BASE_LOCATION+ "//div[contains(@class,'orangehrm-like-animation')]")
        self.POST_MENU_TRIGGER = (By.XPATH,self.BASE_LOCATION+"//i[contains(@class, 'bi-three-dots')]")
        self.DELETE_OPTION = (By.XPATH, "//p[text()='Delete Post']")
        self.CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[text()=' Yes, Delete ']")
        self.SUCCESS_ALERT = (By.CSS_SELECTOR, ".oxd-toast")
    # --- Actions ---
    def go_to_buzz(self):
        self.wait.until(EC.element_to_be_clickable(self.BUZZ_TAB)).click()

    def create_post(self,content):
        post_box = self.wait.until(EC.element_to_be_clickable(self.POST_INPUT))
        post_box.click()
        post_box.send_keys(content)
        self.wait.until(EC.element_to_be_clickable(self.POST_BUTTON)).click()

    # def get_first_post_text(self):
    #     return self.wait.until(EC.visibility_of_element_located(self.FIRST_POST_TEXT)).text

    def get_base_location(self,content):
        self.BASE_LOCATION= f"//p[contains(.,'{content}')]/ancestor::div[contains(@class, 'oxd-grid-item--gutters')][1]"
        self.COMMENT_LINK = (By.XPATH, self.BASE_LOCATION + "//i[contains(@class,'bi-chat-text-fill')]")
        self.COMMENT_INPUT = (By.XPATH, self.BASE_LOCATION + "//input[@placeholder='Write your comment...']")
        self.LIKE_BUTTON = (By.XPATH, self.BASE_LOCATION + "//*[local-name()='svg']")
        self.POST_MENU_TRIGGER = (By.XPATH, self.BASE_LOCATION + "//i[contains(@class, 'bi-three-dots')]")
        self.LIKED_STATE = (By.XPATH, self.BASE_LOCATION + "//div[contains(@class,'orangehrm-like-animation')]")

    def comment_on_post(self, comment_text):
        self.wait.until(EC.element_to_be_clickable(self.COMMENT_LINK)).click()
        comment_input = self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT))
        comment_input.send_keys(comment_text + Keys.RETURN)

    def like_post(self):
        #self.wait.until(EC.element_to_be_clickable(self.LIKE_BUTTON)).click()
        # Assert the post is liked (e.g., by checking class or icon change)
        try:
            self.wait.until(EC.presence_of_element_located(self.LIKED_STATE))
        except TimeoutException:
            assert False, "Post was not deleted successfully"

    def delete_post(self):
        self.wait.until(EC.element_to_be_clickable(self.POST_MENU_TRIGGER)).click()
        self.wait.until(EC.element_to_be_clickable(self.DELETE_OPTION)).click()
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_DELETE_BUTTON)).click()

    def wait_for_success_alert(self, expected_text=None):
        alert = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_ALERT))
        alert_text = alert.text.strip()
        print("[Alert Found]:", alert_text)
        if expected_text:
            assert expected_text in alert_text, f"Expected alert text '{expected_text}' not found in '{alert_text}'"
        return alert_text