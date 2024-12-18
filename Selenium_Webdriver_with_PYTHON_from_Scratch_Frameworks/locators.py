import re
from _ast import pattern
from enum import Enum
from pickle import FALSE

from selenium import webdriver
from selenium.common import NoSuchElementException, InvalidSelectorException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import logging
from enum import Enum

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from setuptools.msvc import msvc14_get_vc_env
class AssertionEnum(Enum):
    EQUAL = 1
    NO_EQUAL = 2

# Variable de configuración para activar/desactivar los logs en archivo
activar_logs = True  # Cambia a False para desactivar el archivo .log

# Configuración básica del logger
if activar_logs:
    logging.basicConfig(
        level=logging.DEBUG,   # Nivel mínimo que se registrará
        filename=f"{__file__[0:__file__.find('.py')]}.log",    # Archivo donde se guardarán los logs
        filemode='a',          # Modo: 'a' para append o 'w' para sobrescribir
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
else:
    logging.basicConfig(
        level=logging.DEBUG,  # Nivel mínimo
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


class ResultManager:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        try:
            self._logger_handler()
        except Exception as e:
            self.logger.exception("Exception occurred: {}".format(e))

    def _logger_handler(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def check_equals_to(self, actual_value, expected_value, step_msg):
        try:
            assert actual_value == expected_value
            self.logger.info(f"PASSED, Assert Equal - {step_msg}")
        except AssertionError as e:
            self.logger.error(f"FAILED, Assert NOT Equal - {step_msg}")
            self.logger.error(f"The given actual value: '{actual_value}' IS NOT EQUAL TO the expected value: {expected_value}")

    def check_not_equals_to(self, actual_value, expected_value, step_msg):
        try:
            assert actual_value != expected_value
            self.logger.info(f"PASSED, Assert NOT Equal - {step_msg}")
        except AssertionError as e:
            self.logger.error(f"FAILED, Assert Equal - {step_msg}")
            self.logger.error(
                f"The given actual value: '{actual_value}' IS EQUAL TO the expected value: {expected_value}")

    def check_true(self, actual_value, step_msg):
        try:
            assert actual_value == True
            self.logger.info(f"PASSED, Assert TRUE- {step_msg}")
        except AssertionError as e:
            self.logger.error(f"FAILED, Assert NOT TRUE - {step_msg}")
            self.logger.error(
                f"The given actual value: '{actual_value}' IS NOT TRUE")

    def check_false(self, actual_value, step_msg):
        try:
            assert actual_value == False
            self.logger.info(f"PASSED, Assert FALSE- {step_msg}")
        except AssertionError as e:
            self.logger.error(f"FAILED, Assert TRUE - {step_msg}")
            self.logger.error(
                f"The given actual value: '{actual_value}' IS NOT FALSE")

    def check_string_in(self, sub_str, look_in_str, step_msg):
        try:
            assert sub_str in look_in_str
            self.logger.info(f"PASSED, Assert FALSE- {step_msg}")
        except AssertionError as e:
            self.logger.error(f"FAILED, Assert TRUE - {step_msg}")
            self.logger.error(
                f"The given actual value: '{sub_str}' IS NOT IN {look_in_str}")

    def check_not_raises_any_exception(self, method, step_msg, *args, **kwargs):
        try:
            return_value = method(*args, **kwargs)
            self.logger.info(f"PASSED, Assert NOT RAISED exception- {step_msg}")
        except Exception as e:
            self.logger.error(f"FAILED, Assert RAISED exception - {step_msg}")
            self.logger.error(
                f"execution method {method.__name__} raised an exception: {e}")
        return return_value

    def check_lower(self, actual_value, expected_value, step_msg):
        try:
            assert actual_value < expected_value
            self.logger.info(f"PASSED, Assert Lower - {step_msg}")
        except AssertionError as e:
            self.logger.error(f"FAILED, Assert NOT lower - {step_msg}")
            self.logger.error(
                f"The given actual value: '{actual_value}' IS NOT LOWER than {expected_value}")

    def check_list_content(self, actual_list, expected_list, step_msg, assertion=AssertionEnum.EQUAL):

        def check_same_list(actual_list, expected_list, step_msg):
            try:
                assert actual_list == expected_list
                self.logger.info(f"PASSED, Assert Lists are Equals - {step_msg}")
            except AssertionError as e:
                self.logger.error(f"FAILED, Assert Lists are NOT Equals- {step_msg}")

        def check_not_same_list(actual_list, expected_list, step_msg):
            try:
                assert actual_list != expected_list
                self.logger.info(f"PASSED, Assert Lists are NOT Equals - {step_msg}")
            except AssertionError as e:
                self.logger.error(f"FAILED, Assert Lists are Equals- {step_msg}")

        MAPPING_ASSERTION = {
            AssertionEnum.EQUAL: check_same_list,
            AssertionEnum.NO_EQUAL: check_not_same_list,
        }
        MAPPING_ASSERTION[assertion](actual_list=actual_list, expected_list=expected_list, step_msg=step_msg)


class BrowserError(Exception):
    pass

class BrowserManager:


    def __init__(self, type_browser):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        try:
            self._logger_handler()
        except Exception as e:
            self.logger.exception("Exception occurred: {}".format(e))
        try:
            self.driver = getattr(webdriver, type_browser)()
        except AttributeError:
            self.logger.error(f"Error webdriver does not have attribute: {type_browser}")

    def _logger_handler(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def open_page(self, page_path):
        self.logger.info(f"Opening page: {page_path}")
        self.driver.get(page_path)

    def iterate_by_elements(valid_return=False):

        def decorator(func):
            def inner(self, *args, **kwargs):
                value = None
                for a_name in By.__dict__:
                    if a_name.startswith("_"):
                        continue
                    try:
                        a_value = getattr(By, a_name)
                        value = func(self, *args, a_value=a_value, **kwargs)
                        if not valid_return:
                            break
                        if value:
                            break
                    except (NoSuchElementException,InvalidSelectorException,TimeoutException) as e:
                        pass
                    except TypeError as e:
                        self.logger.exception(f"Error occurred: {e}")
                        raise BrowserError("Error occurred: {}".format(e))
                return value
            return inner
        return decorator

    @iterate_by_elements()
    def enter_key(self, element=None, key=None, a_value=None):
        return self.driver.find_element(a_value, element).send_keys(key)

    @iterate_by_elements()
    def click_on_element(self, bro_obj=None,element=None, a_value=None):
        bro_obj = bro_obj or self.driver
        return bro_obj.find_element(a_value, element).click()

    @iterate_by_elements(True)
    def get_text_from_element(self, element=None, a_value=None):
        return self.driver.find_element(a_value, element).text

    @iterate_by_elements()
    def clean_element(self, element=None, a_value=None):
        return self.driver.find_element(a_value, element).clear()

    @iterate_by_elements()
    def selector_elemet(self, element=None, method=None, a_value=None):
        my_selector = Select(self.driver.find_element(a_value, element))
        if isinstance(method, str):
            return my_selector.select_by_visible_text(method)
        elif isinstance(method, int):
            return my_selector.select_by_index(method)
        else:
            raise BrowserError(f"Invalid option for method {method}")

    def get_list_of_dropdown_elements(self, dropelement=None, key=None, selecelemet=None,  timeout=1):
        self.enter_key(element=dropelement, key=key)
        time.sleep(timeout)
        return self.driver.find_elements(By.CSS_SELECTOR, selecelemet)

    @iterate_by_elements(True)
    def get_list_element(self, element=None, a_value=None):
        return self.driver.find_elements(a_value, element)

    def get_single_object_value_from_listed_elements(self, element=None, value=None):
        for single_element in self.get_list_element(element=element):
            if single_element.get_attribute("value") == value:
                return single_element

    @iterate_by_elements(True)
    def get_obj_element(self, bro_obj=None, element=None, a_value=None, wait_until=False):
        bro_obj = bro_obj or self.driver
        if wait_until:
            wait = WebDriverWait(bro_obj, 2)
            return wait.until(expected_conditions.presence_of_element_located((a_value, element)))
        return bro_obj.find_element(a_value, element)

    def get_element_value(self, element=None):
        return self.get_obj_element(element=element).get_attribute("value")

class WebWindowManipulator:

    def __init__(self, type_browser, page_path):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.browser_manager = BrowserManager(type_browser)
        self.browser_manager.open_page(page_path=page_path)
        self.action_chains = ActionChains(self.browser_manager.driver)

    def _action_base(self,element=None):
        try:
            return self.action_chains.move_to_element(self.browser_manager.get_obj_element(element=element))
        except Exception as e:
            self.logger.exception("Exception occurred: {}".format(e))

    def perform_move_to_element(self, element=None):
        self._action_base(element=element).perform()

    def perform_click_on_element(self,element=None):
        self._action_base(element=element).click().perform()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # exercice_running = int(input("Give the exercise number: "))
    exercice_running = 8
    result_manager = ResultManager()
    # ------Exercise:1--------------
    if exercice_running == 1:
        browser_instance = BrowserManager('Chrome')
        browser_instance.open_page(page_path="https://rahulshettyacademy.com/angularpractice/")
        for element, key in {"email": "hello@gmail.com", "exampleInputPassword1": "1234"}.items():
            browser_instance.enter_key(element, key)
        browser_instance.click_on_element("exampleCheck1")

        #  Xpath
        browser_instance.click_on_element("//input[@type='submit']")
        mesg = browser_instance.get_text_from_element("alert-success")
        print(f"Message contests : {mesg}")
        browser_instance.enter_key("(//input[@type='text'])[3]", "helloMexixcanRaul")
        browser_instance.clean_element("(//input[@type='text'])[3]")

    # ---------------Exercise 2
    elif exercice_running == 2:
        browser_instance = BrowserManager('Chrome')
        browser_instance.open_page(page_path="https://rahulshettyacademy.com/client")
        browser_instance.click_on_element("Forgot password?")
        # Two different ways to enter text to a child div
        browser_instance.enter_key("//form/div[1]/input", "demo@mail.com") # 1 using format: //form/div[<n>]/input
        browser_instance.enter_key("form div:nth-child(2) input", "Hello@1234") # 2 using form div:nth-child(<n>) input
        browser_instance.enter_key("form div:nth-child(3) input", "Hello@1234")
        #browser_instance.click_on_element("Save New Password") # Calling like will generate an error
        # browser_instance.click_on_element("//button[@type='submit']")  # This is one option
        browser_instance.click_on_element("//button[text()='Save New Password']")  # This is another option


    # --------------- Exercise 3: dropdown
    elif exercice_running == 3:
        browser_instance = BrowserManager('Chrome')
        browser_instance.open_page(page_path="https://rahulshettyacademy.com/angularpractice/")
        for method in ["Female", 0]:
            browser_instance.selector_elemet(element="exampleFormControlSelect1", method=method)
            time.sleep(2)

    #---------------- Exercise 4:
    elif exercice_running == 4:
        browser_instance = BrowserManager('Chrome')
        browser_instance.open_page(page_path="https://rahulshettyacademy.com/dropdownsPractise/")
        list_of_elements = browser_instance.get_list_of_dropdown_elements(
            "autosuggest", "ind", "li[class='ui-menu-item'] a")
        for element in list_of_elements:
            print(element.text)
            if element.text == "India":
                element.click()
                break

        value_attr = browser_instance.get_element_value("autosuggest")
        step_msg = "Check attribute value"
        result_manager.check_equals_to(actual_value=value_attr, expected_value="India", step_msg=step_msg)
        result_manager.check_equals_to(actual_value=value_attr, expected_value="Indiacha", step_msg=step_msg)

    elif exercice_running == 5:
        def checkboxes_radiobuttons(item, click=True):
            if click:
                item.click()
            return item.is_selected()

        browser_instance = BrowserManager('Chrome')
        browser_instance.open_page(page_path="https://rahulshettyacademy.com/AutomationPractice/")
        # --------------------------- Checkbox  --------------------------
        actual_check_obj = browser_instance.get_single_object_value_from_listed_elements(element="//input[@type='checkbox']", value="option2")
        step_msg = "Check 'checkbox' is selected"
        # result_manager.check_true(checkboxes_radiobuttons(actual_check_obj), step_msg)
        result_manager.check_true(checkboxes_radiobuttons(actual_check_obj,False), step_msg)
        # --------------------------- RadioButton  --------------------------
        radio_butn = browser_instance.get_list_element(element=".radioButton")[2]
        step_msg = "Check 'radiobutton' is selected"
        result_manager.check_true(checkboxes_radiobuttons(radio_butn, True), step_msg)
        # result_manager.check_true(checkboxes_radiobuttons(radio_butn, False), step_msg)
        # --------------------------- displayed text  --------------------------
        step_msg = "Check 'displayed-text' is displayed"
        display_object = browser_instance.get_obj_element(element="displayed-text")
        result_manager.check_true(display_object.is_displayed(), step_msg)
        # assert browser_instance.driver.find_element(By.ID, "displayed-text").is_displayed()
        # browser_instance.driver.find_element(By.ID, "hide-textbox").click()
        # assert not browser_instance.driver.find_element(By.ID, "displayed-text").is_displayed()
        step_msg = "Check NOT 'displayed-text' is displayed"
        browser_instance.driver.find_element(By.ID, "hide-textbox").click()
        result_manager.check_false(display_object.is_displayed(), step_msg)

    elif exercice_running == 6: # Handling Java/Javascript alerts
        # 1. Create browsr obj
        browser_instance = BrowserManager('Chrome')
        # 2. Get page
        browser_instance.open_page(page_path="https://rahulshettyacademy.com/AutomationPractice/")
        # 3 get name as input
        name = str(input("Enter your name: "))
        # 4. Set name in #name
        browser_instance.enter_key(element="#name", key=name)
        # 5. Press button
        browser_instance.click_on_element("alertbtn")
        local_alert = browser_instance.driver.switch_to.alert
        step_msg = f"Check {name} is present"
        result_manager.check_string_in(sub_str=name,look_in_str=local_alert.text,step_msg=step_msg)
        time.sleep(2)
        step_msg = f"Check closing alert is executed with no problems"
        result_manager.check_not_raises_any_exception(method=local_alert.accept, step_msg=step_msg)

    elif exercice_running == 7: # Explicit Waiting time
        # 1. Create browsr obj
        browser_instance = BrowserManager('Chrome')
        # 2. Get page
        browser_instance.open_page(page_path="https://rahulshettyacademy.com/seleniumPractise/#/")
        # Declar a kind of global timeout for each action made for the browser_instance
        browser_instance.driver.implicitly_wait(2)
        # 3. Set the word 'ber' on search space
        browser_instance.enter_key(element=".search-keyword", key="ber")
        # 4. Get a list of all the elements filter previously
        matching_elements = browser_instance.get_list_element(element="//div[@class='products']/div")
        # 5. Click on all the elements
        actual_list_text = []
        pattern = r"^(.*?)\n"
        """
        ^ → Inicio de la cadena.
        (.*?) → Captura cualquier carácter de forma no codiciosa.
        \n → Detiene la captura en el primer salto de línea.
        """
        for ele in matching_elements:
            browser_instance.click_on_element(bro_obj=ele, element="div/button")
            actual_list_text.append(re.match(pattern, ele.text).group(1))

        # Check the text of the found element is the expected
        step_msg = "Check the text of products filtered matches the expected values"
        EXPECTED_LIST_OF_ELEMENTS_NAMES = ["Cucumber - 1 Kg", "Raspberry - 1/4 Kg", "Strawberry - 1/4 Kg"]
        result_manager.check_list_content(actual_list=actual_list_text, expected_list=EXPECTED_LIST_OF_ELEMENTS_NAMES,step_msg=step_msg)



        browser_instance.click_on_element(element="img[alt='Cart']")
        browser_instance.click_on_element(element="//button[text()='PROCEED TO CHECKOUT']")

        browser_instance.enter_key(element=".promoCode", key="rahulshettyacademy")
        browser_instance.click_on_element(element=".promoBtn")
        # Using my method takes a lot more, this is a wrong path to follow to validating this kind of stuff
        step_msg = "Check the promo code has the expected value"
        obj = browser_instance.get_obj_element(element=".promoInfo", wait_until=True)
        result_manager.check_equals_to(actual_value=obj.text, expected_value="Code applied ..!", step_msg=step_msg)
        # wait = WebDriverWait(browser_instance.driver, 10)
        # wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".promoInfo")))
        # print(browser_instance.driver.find_element(By.CLASS_NAME, "promoInfo").text)
        # 6. Validate the sume prices
        prices = browser_instance.get_list_element(element="tr td:nth-child(5) p")  # Takes the elements place in the 5ht column
        sum = sum([int(price.text) for price in prices])
        total_amount = int(browser_instance.get_obj_element(element=".totAmt").text)
        step_msg = "Check the total amount has the expected value"
        result_manager.check_equals_to(actual_value=total_amount, expected_value=sum, step_msg=step_msg)
        discount = 0.1
        expected_price_with_discount = round(float(sum - (sum*discount)), 2)
        total_after_discoutn =float(browser_instance.get_obj_element(element=".discountAmt").text)
        step_msg = "Check the total amount has the expected value after discount"
        result_manager.check_equals_to(actual_value=total_after_discoutn, expected_value=expected_price_with_discount, step_msg=step_msg)
        step_msg = "Check the total amount after discount is lower that the original total amount"
        result_manager.check_lower(actual_value=total_after_discoutn, expected_value=total_amount, step_msg=step_msg)

    elif exercice_running == 8:
        web_manager = WebWindowManipulator(
            type_browser='Chrome',
            page_path="https://rahulshettyacademy.com/AutomationPractice/"
        )
        for key, value in {"Reload": "mousehover", "Top": "mousehover"}.items():
            result_manager.check_not_raises_any_exception(
                method=web_manager.perform_move_to_element,
                step_msg=f"Check the execution of the method is correctly done by moving to '{value}'",
                element=value
            )
            result_manager.check_not_raises_any_exception(
                method=web_manager.perform_move_to_element,
                step_msg=f"Check the execution of the method is correctly done by clicking on '{key}'",
                element=key
            )
            time.sleep(2)


    else:
        pass


    time.sleep(5)
