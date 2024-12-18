import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class LoggerManager:
    def __init__(self, active_logs=True):
        self.active_logs = active_logs
        self._setup_logger()

    def _setup_logger(self):
        if self.active_logs:
            logging.basicConfig(
                level=logging.DEBUG,
                filename=f"{__file__[0:__file__.find('.py')]}.log",
                filemode='a',
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

    def get_logger(self, name):
        return logging.getLogger(name)


class ResultManager:
    def __init__(self, logger_manager):
        self.logger = logger_manager.get_logger(self.__class__.__name__)

    def check_equals_to(self, actual_value, expected_value, step_msg):
        try:
            assert actual_value == expected_value
            self.logger.info(f"PASSED, Assert Equals - {step_msg}")
        except AssertionError as e:
            self.logger.error(f"FAILED, Assert NOT Equals - {step_msg}")
            self.logger.error(f"The given actual value: '{actual_value}' IS NOT EQUAL TO the expected value: {expected_value}")

    def check_not_equals_to(self, actual_value, expected_value, step_msg):
        try:
            assert actual_value != expected_value
            self.logger.info(f"PASSED, Assert NOT Equals - {step_msg}")
        except AssertionError as e:
            self.logger.error(f"FAILED, Assert Equals - {step_msg}")
            self.logger.error(f"The given actual value: '{actual_value}' IS EQUAL TO the expected value: {expected_value}")



class BrowserManagerError(Exception):
    pass

class BrowserManager:

    def __init__(self, logger_manager, type_browser="Chrome", path_page=None):
        """
        :param type_browser: str, Type of browser to use
        """
        self.driver = None
        self.logger = logger_manager.get_logger(self.__class__.__name__)
        self.initialize_webdriver(type_browser=type_browser)
        if path_page:
            self.define_path_page(path_page)

    def initialize_webdriver(self, type_browser):
        try:
            self.driver = getattr(webdriver, type_browser)()
        except AttributeError:
            self.logger.error(f"Error webdriver does not have attribute: {type_browser}")

    def define_path_page(self, path_page):
        try:
            self.driver.get(path_page)
            self.logger.info(f"Opening page: {path_page}")
        except Exception as e:
            self.logger.error(f"Exception occurred: {e}")
            raise BrowserManagerError(f"Error trying to set page {path_page}") from e

    def __getattr__(self, item):
        """
        Wraps the self.driver to include a try and except to include more information
        :param item: it is the self.driver attribute, or method to be called
        :return: the self.driver method or attribute given
        """
        driver_attr = getattr(self.driver, item)
        if callable(driver_attr):
            def method_wrapper(*args, **kwargs):
                try:
                    self.logger.info(f"Calling method {item} with args {args}, kwargs {kwargs}")
                    return driver_attr(*args, **kwargs)
                except AttributeError as e:
                    self.logger.error(f"Exception occurred: {e}")
                    raise BrowserManagerError(f"Error: {driver_attr} does not have that attributes {item}") from e
            return method_wrapper
        else:
            return driver_attr


if __name__ == '__main__':
    MAIN_BROWSER = "Chrome"
    MAIN_PAGE = "https://rahulshettyacademy.com/loginpagePractise/"
    SECONDARY_PAGE = "https://rahulshettyacademy.com/documents-request"
    EMAIL_PATTERN_EXTRACTOR = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    DUMMY_PASSWORD = "<PASSWORD>"
    EXPECTED_ALERT_TEXT = "Incorrect username/password."
    logger_manager = LoggerManager(active_logs=True)
    result = ResultManager(logger_manager)

    # 1. Define BroweserManager obj and open main page,
    local_manager = BrowserManager(logger_manager,MAIN_BROWSER, MAIN_PAGE)
    # 2. Click on https://rahulshettyacademy.com/documents-request
    local_manager.find_element(
        By.XPATH,
        f'//div[@class="float-right"]/a[@href="{SECONDARY_PAGE}"]').click()
    # 3. Move to secondary page
    local_manager.define_path_page(SECONDARY_PAGE)
    wait = WebDriverWait(local_manager.driver, 20)
    wait.until(expected_conditions.presence_of_element_located((
                By.XPATH,
                '//div[@class="auto-container"]/div[@class="inner-box"]/h1[text()="Documents request"]')))
    # 4. Copy the whole text
    whole_red_text = local_manager.find_element(By.XPATH, '//div[@class="col-md-8"]/p[@class="im-para red"]').text
    # 5. extract the email
    matches = re.findall(EMAIL_PATTERN_EXTRACTOR, whole_red_text)
    step_msg = f"Check '{matches}' is not Empty"
    result.check_not_equals_to(actual_value=matches, expected_value=[], step_msg=step_msg)
    email = matches[0]
    # 6. Move back to the main window
    local_manager.define_path_page(MAIN_PAGE)
    # 7. Write the email and password & Evaluate they have been written
    credentials = {
        "username": email,
        "password": DUMMY_PASSWORD
    }
    for key, value in credentials.items():
        local_manager.find_element(By.ID, key).send_keys(value)
        actual_text = local_manager.find_element(By.ID, key).get_attribute("value")
        step_msg = f"Check '{actual_text}' is has the expected value"
        result.check_equals_to(actual_value=actual_text, expected_value=value, step_msg=step_msg)

    # 8. Click on sign in button
    wait = WebDriverWait(local_manager.driver, 5)
    local_manager.find_element(By.ID, "signInBtn").click()
    # 9. Wait until alter is displayed
    alert_obj = wait.until(expected_conditions.visibility_of_element_located((
        By.CLASS_NAME,
        'alert')))
    step_msg = f"Check the '{alert_obj.text}' has the expected value"
    result.check_equals_to(actual_value=alert_obj.text, expected_value=EXPECTED_ALERT_TEXT,step_msg=step_msg)
