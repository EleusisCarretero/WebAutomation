import re
import time
import pytest
from Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.result_manager import ResultManagerClass
from  Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.loger_manager import LoggerManager
from Selenium_Webdriver_with_PYTHON_from_Scratch_Frameworks.browser_manager import BrowserManagerClass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class TestSortTable:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.DEFAULT_PAGE = "https://rahulshettyacademy.com/angularpractice"
        self.logger_manager = LoggerManager(active_logs=True)
        self.result = ResultManagerClass(self.logger_manager)
        self.broser_manager = BrowserManagerClass(
            self.logger_manager,
            "Chrome",
            self.DEFAULT_PAGE,
            "--start-maximized")
        self.step_move_to_shop()

    def click_on_element(self, by, element, obj=None):
        obj = obj or self.broser_manager
        obj.find_element(by, element).click()
    
    def step_move_to_shop(self):
        SHOP_EXTENSION = "shop"
        SHOP_CSS_SELECTOR = "a[href*='shop']"
        # 1. Click on shop button
        self.result.check_not_raises_any_exception(
            method=self.click_on_element,
            step_msg="Check clicking on shop button successfully",
            by=By.CSS_SELECTOR,
            element=SHOP_CSS_SELECTOR
        )
        assert self.result.step_status
        # 2. Move to shop page and check the path is the expected
        shop_secundary_page = f"{self.DEFAULT_PAGE}/{SHOP_EXTENSION}"
        windows = self.broser_manager.window_handles
        self.broser_manager.switch_to.window(windows[0])
        self.result.check_equals_to(
            actual_value=self.broser_manager.current_url,
            expected_value=shop_secundary_page,
            step_msg="Check the url is the expected"
        )

        
    @pytest.mark.parametrize(
        ("expected_cell_name",
        "expected_price",
        "qty_of_cell"),
        [
        ("iphone X", 24.99, 5),
        ("Samsung Note 8", 24.99, 10),
        ("Nokia Edge", 24.99, 17),
        ("Blackberry", 24.99, 7)
        ]
    )
    def test_validate_cell_name(self, expected_cell_name, expected_price, qty_of_cell):
        # 1. Get the list of the entire cellphone displayed
        XPATH_SEQUENCE = "//app-card-list[contains(@class, 'row')]/app-card[contains(@class, 'col-lg-3')]"
        XPATH_TITLE_SEQUENCE = "//div[@class='card h-100']/div[@class='card-body']/h4[@class='card-title']"
        XPATH_PRICE_SEQUENCE = "./h5"
        XPATH_BTN_ADD = "//button[@class='btn btn-info']"
        CHECKOUT_BTN_SELECTOR = "a.nav-link.btn.btn-primary"
        patter_qty_itmes = r'\(\s*(\d+)\s*\)'
        cell_phone_list = self.result.check_not_raises_any_exception(
            self.broser_manager.find_elements,
            "Check getting the cell phone object list succesfully",
            By.XPATH,
            XPATH_SEQUENCE
        )
        assert self.result.step_status

        for cell in cell_phone_list:
            cell_name = cell.find_element(By.XPATH, XPATH_TITLE_SEQUENCE)
            if cell_name.text == expected_cell_name:
                break
        card_body = cell_name.find_element(By.XPATH, "..")
        cell_prince = card_body.find_element(By.XPATH, XPATH_PRICE_SEQUENCE).text
        # 2. Check the price
        self.result.check_equals_to(
            actual_value=float(cell_prince[1:]),
            expected_value=expected_price,
            step_msg="Check the cellphone price matches the expected price"
        )
        assert self.result.step_status
        # 3. add it to the card
        card_footer = cell_name.find_element(By.XPATH, "../..")
        for _ in range(qty_of_cell):
            self.result.check_not_raises_any_exception(
                method=self.click_on_element,
                step_msg=f"Check adding cellphone {cell_name.text} to the card witht no error",
                by=By.XPATH,
                element=XPATH_BTN_ADD,
                obj=card_footer
            )
        assert self.result.step_status
        # 4. Check 'checkout' button has the number
        tmp_txt = self.broser_manager.find_element(By.CSS_SELECTOR, CHECKOUT_BTN_SELECTOR).text
        actual_items_in_checkout = re.search(patter_qty_itmes, tmp_txt)
        self.result.check_equals_to(
            actual_value=int(actual_items_in_checkout.group(1)),
            expected_value=qty_of_cell,
            step_msg="Check the items registered in checkout button is the expected"
        )
        assert self.result.step_status
    
    def teardown_method(self):
        # 4. Close browser
        step_msg = "Check closing bowser successfully"
        self.result.check_not_raises_any_exception(
            self.broser_manager.close,
            step_msg,
        )
        assert self.result.step_status
