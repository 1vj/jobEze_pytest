import logging
import time

from webdriver.WebDriverHelperNew import WebDriverHelper
from config.TestConfig import TestConfig

log = logging.getLogger(__name__)


class HrmLogin(WebDriverHelper):
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

    def set_username(self, text):
        username_field = self.find_element('visible', 'xpath', "//input[@name='username']", 10)
        username_field.send_keys(text)
        log.info("Username set to: %s", text)

    def set_password(self, text):
        password_field = self.find_element('visible', 'xpath', "//input[@name='password']", 10)
        password_field.send_keys(text)
        log.info("Password set.")

    def click_login_button(self):
        self.find_element('visible', 'xpath', "//button[@type='submit']", 10).click()
        log.info("Login button clicked.")

    def click_admin_tab(self):
        self.find_element('visible', 'xpath', "//aside[@class='oxd-sidepanel']//li[1]", 50).click()
        log.info("Admin tab clicked.")

    def login_to_hrm_application(self, username, password):
        self.driver.get(self.data.url)
        self.driver.maximize_window()
        time.sleep(2)  # Consider replacing this with WebDriverWait for better handling
        self.set_username(username)
        self.set_password(password)
        self.click_login_button()

    def verify_current_url(self):
        url = self.driver.current_url
        log.info("Fetched current URL: %s", url)
        expected_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
        log.info("Verifying the URL...")
        assert url == expected_url, f"Expected URL: {expected_url}, but got: {url}"

    def click_on_admin_menu(self, admin_url):
        self.click_admin_tab()
        time.sleep(2)  # Consider replacing this with WebDriverWait for better handling
        url = self.driver.current_url
        log.info("Fetched current URL: %s", url)
        log.info("Verifying if URL matches admin URL...")
        assert url == admin_url, f"Expected URL: {admin_url}, but got: {url}"
