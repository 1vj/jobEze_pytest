import logging
import time

from webdriver.WebDriverHelperNew import WebDriverHelper
from config.TestConfig import TestConfig

log = logging.getLogger(__name__)


class HrmAdmin(WebDriverHelper):
    def __init__(self, driver):
        """
        Initializes the HrmLogin page object with the WebDriver instance.

        :param driver: WebDriver instance used for interacting with the browser.
        """
        super().__init__(driver)  # Initialize the WebDriverHelper with the driver
        self.driver = driver
        self.data = TestConfig()  # Initialize the test configuration data

        # Log the initialization for debugging
        log.info("HrmLogin initialized with WebDriver")

    def clickAdminTab(self):
        self.find_element('clickable', 'xpath', "//aside[@class='oxd-sidepanel']//li[1]", 50).click()

    def getListOfAdminMenu(self):
        log.info("fetch the list of the admin menu")
        element = self.find_element('visible', 'xpath', "//li[contains(@class,'oxd-topbar-body-nav-tab')]", 50)
        menus = self.get_elements(element_xpath="//li[contains(@class,'oxd-topbar-body-nav-tab')]")
        actual_field = []
        for value in menus:
            text = value.get_attribute('innerText')
            log.info(f"{text}")
            actual_field.append(text)
        return actual_field

    def verify_admin_menu_option(self, admin_menu):
        self.clickAdminTab()
        time.sleep(2)
        actual_list = self.getListOfAdminMenu()
        log.info(f"{actual_list}")
        assert admin_menu == actual_list
