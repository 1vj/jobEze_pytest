import logging
import time
from webdriver.WebDriverHelperNew import WebDriverHelper
from config.TestConfig import TestConfig

log = logging.getLogger(__name__)  # Set up logging


class SpanideaHome(WebDriverHelper):
    def __init__(self, driver):
        super().__init__(driver)  # Initialize the parent class
        self.data = TestConfig()

    def click_what_we_do_menu(self):
        """Clicks on the 'What We Do' menu item."""
        log.info("Attempting to click 'What We Do' menu")
        self.click_element("//a[normalize-space()='What we do']", "What We Do menu")

    def launch_application(self):
        """Launches the Spanidea application."""
        log.info(f"Launching application at {self.data.url1}")
        self.go_to_url(self.data.url1)
        time.sleep(2)  # Consider using a more robust wait method
        log.info("User able to launch the Spanidea application")

    def verify_current_url(self):
        """Verifies that the current URL matches the expected home page URL."""
        current_url = self.get_current_url()
        log.info("Fetched the current URL")
        expected_url = "https://spanidea.com/in/"
        log.info(f"Expected URL: {expected_url}, Current URL: {current_url}")
        assert current_url == expected_url, f"Expected URL '{expected_url}' does not match current URL '{current_url}'"
