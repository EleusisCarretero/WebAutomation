from Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.Assigment_child_window_practice import BrowserManager, LoggerManager, ResultManager
from selenium.webdriver.common.by import By
import pytest


class TestFrames:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.IFRAME = "mce_0_ifr"
        self.BODY = "tinymce"
        self.logger_manager = LoggerManager(active_logs=True)
        self.result = ResultManager(self.logger_manager)
        self.broser_manager = BrowserManager(logger_manager=self.logger_manager, type_browser="Chrome", path_page="https://the-internet.herokuapp.com/iframe")
    
    def test_write_iframe(self):
        Text = "Dumy text"
        TIMEOUT = 2
        # 1. Initialize timeout
        self.broser_manager.implicitly_wait(TIMEOUT)
        # 2. Swith to iframe
        self.result.check_not_raises_any_exception(
            self.broser_manager.switch_to.frame,
            f"Check chaging to {self.IFRAME} frames succesfully",
            self.IFRAME
        )
        # 3. Clean
        self.broser_manager.find_element(By.ID, self.BODY).clear()
        # 4. Send text to be writtem
        self.broser_manager.find_element(By.ID, self.BODY).send_keys(Text)
        my_written_tx = self.broser_manager.find_element(By.ID, self.BODY).text
        # 5. Check the text is correclty written
        step_msg = "Check the text has been correctly written in the frame"
        self.result.check_equals_to(actual_value=my_written_tx,expected_value=Text,step_msg=step_msg)
        self.result.check_not_raises_any_exception(
            self.broser_manager.switch_to.default_content,
            f"Check chaging to default page succesfully",
        )
