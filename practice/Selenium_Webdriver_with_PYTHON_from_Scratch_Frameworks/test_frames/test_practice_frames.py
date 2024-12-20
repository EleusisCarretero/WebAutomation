import time
import pytest
from Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.result_manager import ResultManagerClass
from  Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.loger_manager import LoggerManager
from Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.browser_manager import BrowserManagerClass
from selenium.webdriver.common.by import By


class TestFrames:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.ID_FRAME = "courses-iframe"
        self.DEFAULT_PAGE = "https://rahulshettyacademy.com/AutomationPractice/"
        self.logger_manager = LoggerManager(active_logs=True)
        self.result = ResultManagerClass(self.logger_manager)
        self.broser_manager = BrowserManagerClass(logger_manager=self.logger_manager, type_browser="Chrome", path_page=self.DEFAULT_PAGE)
        self.initial_step()
    
    def initial_step(self):
        TIMEOUT = 2
        # 1. Initialize timeout
        self.broser_manager.implicitly_wait(TIMEOUT)
        step_msg = f"Check switching to {self.ID_FRAME} successfully"
        self.result.check_not_raises_any_exception(
            self.broser_manager.switch_to.frame,
            step_msg,
            self.ID_FRAME)
        assert self.result.step_status
    
    @pytest.mark.parametrize(
        "button",
        [
        ("fa-youtube"),
        ("fa-linkedin"),
        ("theme-btn"),
        ("register-btn")
        ]
    )
    def test_login_buttom(self, button):
        SUB_ERROR_FRAME =  "sub-frame-error"
        ICON_ERROR = "icon icon-generic"
        XPATH_FORMAT = f'//div[@id="{SUB_ERROR_FRAME}"]/div[@class="{ICON_ERROR}"]'
        # 1. Click on login button
        step_msg = f"Check the login button {button} exist"
        obj_btn = self.result.check_not_raises_any_exception(
            self.broser_manager.find_element,
            step_msg,
            By.CLASS_NAME,
            button
        )
        assert self.result.step_status
        step_msg = f"Check the login button {button} is clickable"
        self.result.check_not_raises_any_exception(
            obj_btn.click,
            step_msg,
        )
        assert self.result.step_status
        # 2. Check the expected error exists
        step_msg = f"Check the Error icon {ICON_ERROR} exists"
        self.result.check_not_raises_any_exception(
            self.broser_manager.find_element,
            step_msg,
            By.XPATH,
            XPATH_FORMAT
        )
        assert self.result.step_status

    def teardown_method(self):
        # 1. Switch back to default
        MOUSER = "mousehover"
        R_LOAD = "Reload"
        step_msg = f"Check going back to default page {self.DEFAULT_PAGE} succesfully"
        self.result.check_not_raises_any_exception(
            self.broser_manager.switch_to.default_content,
            step_msg)
        assert self.result.step_status
        # 2. Move to mousehover
        step_msg = f"Check moving to {MOUSER} succesfully"

        def action_over_mouser(by_how, elemet_to, method=None):
            element = self.broser_manager.find_element(by_how, elemet_to)
            action = self.broser_manager.move_to_element(element)
            if method:
                action = getattr(self.broser_manager, method)
                action().perform()
            else:
                action.perform()

        self.result.check_not_raises_any_exception(
            action_over_mouser,
            step_msg,
            By.ID,
            MOUSER
        )

        assert self.result.step_status
        # 3. Click on reload window
        step_msg = f"Check Clicking on {R_LOAD} succesfully"
        self.result.check_not_raises_any_exception(
            action_over_mouser,
            step_msg,
            By.LINK_TEXT,
            R_LOAD,
            "click"
        )

        assert self.result.step_status
        # 4. Close browser
        step_msg = "Check closing bowser successfully"
        self.result.check_not_raises_any_exception(
            self.broser_manager.close,
            step_msg,
        )

        assert self.result.step_status
