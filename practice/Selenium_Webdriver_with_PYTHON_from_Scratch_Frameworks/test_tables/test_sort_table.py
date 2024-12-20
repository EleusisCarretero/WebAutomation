import time
import pytest
from Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.result_manager import ResultManagerClass
from  Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.loger_manager import LoggerManager
from Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.browser_manager import BrowserManagerClass
from selenium.webdriver.common.by import By


class TestSortTable:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.DEFAULT_PAGE = "https://rahulshettyacademy.com/seleniumPractise/#/offers"
        self.logger_manager = LoggerManager(active_logs=True)
        self.result = ResultManagerClass(self.logger_manager)
        self.broser_manager = BrowserManagerClass(
            self.logger_manager,
            "Chrome",
            self.DEFAULT_PAGE,
            "--start-maximized",
            "headless")


    def test_simple_sort_table(self):
        TABLE_TITLE_XPTAH = "//span[text()='Veg/fruit name']"
        # 1. Get original list and sorte them
        original_items_names_unsorted = [item.text for item in self.broser_manager.find_elements(By.XPATH, "//tr//td[1]")]
        original_items_names_sorted = sorted(original_items_names_unsorted)
        # 2. Click on title table to sort the list
        self.result.check_not_raises_any_exception(
            method=self.click_on_find_element,
            step_msg=f"Check clicking on table title {TABLE_TITLE_XPTAH} succesfully",
            by=By.XPATH,
            element=TABLE_TITLE_XPTAH
        )
        assert self.result.step_status
        # 3. Get elements sorted by the broser page
        browser_items_names_sorted = [item.text for item in self.broser_manager.find_elements(By.XPATH, "//tr//td[1]")]
        # 4. Compare both sorted lists
        self.result.check_equals_to(
            actual_value=browser_items_names_sorted,
            expected_value=original_items_names_sorted,
            step_msg="Check the browser has sorted the list correclty"
        )
        assert self.result.step_status

    def click_on_find_element(self, by, element):
        self.broser_manager.find_element(by,element).click()
    