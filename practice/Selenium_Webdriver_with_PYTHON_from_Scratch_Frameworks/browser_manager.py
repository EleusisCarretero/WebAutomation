from selenium import webdriver
# from .loger_manager import LoggerManager
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class BrowserManagerClassError(Exception):
    pass

class BrowserManagerClass:

    def __init__(self, logger_manager, type_browser="Chrome", path_page=None, *args):
        """
        :param type_browser: str, Type of browser to use
        """
        self.driver = None
        self.chrome_otions = None
        self.logger = logger_manager.get_logger(self.__class__.__name__)
        self.initialize_webdriver(type_browser, *args)
        if path_page:
            self.define_path_page(path_page)
        self.action_chains = webdriver.ActionChains(self.driver)
        


    def initialize_webdriver(self, type_browser, *args):

        if type_browser == "Chrome" and args:
            self.chrome_otions = webdriver.ChromeOptions()
            for option in args:
                self.chrome_otions.add_argument(option)
        try:
            self.driver = getattr(webdriver, type_browser)(self.chrome_otions)
        except AttributeError:
            self.logger.error(f"Error webdriver does not have attribute: {type_browser}")

    def define_path_page(self, path_page):
        try:
            self.driver.get(path_page)
            self.logger.info(f"Opening page: {path_page}")
        except Exception as e:
            self.logger.error(f"Exception occurred: {e}")
            raise BrowserManagerClassError(f"Error trying to set page {path_page}") from e

    def __getattr__(self, item):
        """
        Wraps the self.driver to include a try and except to include more information
        :param item: it is the self.driver attribute, or method to be called
        :return: the self.driver method or attribute given
        """
        attr = None
        try:
            attr = getattr(self.driver, item)
        except AttributeError:
            try:
                attr = getattr(self.action_chains, item)
            except AttributeError as e:
                self.logger.error(f"Exception occurred: {e}")
                raise BrowserManagerClassError(f"Error: {attr} does not have that attributes {item}") from e
    
        if callable(attr):
            def method_wrapper(*args, **kwargs):
                try:
                    self.logger.info(f"Calling method {item} with args {args}, kwargs {kwargs}")
                    return attr(*args, **kwargs)
                except AttributeError as e:
                    self.logger.error(f"Exception occurred: {e}")
                    raise BrowserManagerClassError(f"Error calling {attr} : {item}") from e
            return method_wrapper
        else:
            return attr

if __name__ == '__main__':
    # test the logger
    from loger_manager import LoggerManager
    tmp = LoggerManager(active_logs=True)
    local_manager = BrowserManagerClass(
        tmp,
        "Chrome",
        "https://rahulshettyacademy.com/seleniumPractise/#/offers",
        "--start-maximized"
    )