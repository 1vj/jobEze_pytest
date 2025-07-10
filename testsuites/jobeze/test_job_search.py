import pytest
import time
import logging
import allure
import json
from Pages.JobezePGObject.HomePage import HomePage
from webdriver import WebDriverHelperNew
from selenium.webdriver.common.by import By

log = logging.getLogger(__name__)


def load_test_data():
    with open("config/test_data.json", "r") as file:
        return json.load(file)


@allure.feature("Jobeze Home Page Tests")
class TestHomePage:

    @pytest.fixture(autouse=True)
    def class_setup(self, browser):
        self.driver = browser
        self.home_page = HomePage(self.driver)
        self.test_data = load_test_data()
        self.web_driver_functions = WebDriverHelperNew.WebDriverHelper(self.driver)

    @allure.title("Verify Home link redirects to base URL")
    @allure.tag("Smoke")
    def test_click_home_link(self):
        with allure.step("Clicking Home link and validating redirection"):
            expected_url = self.test_data["home_url"]
            log.info("Clicking on Home link")
            self.home_page.click_home_link()
            current_url = self.driver.current_url
            log.info(f"Current URL after click: {current_url}")
            assert current_url == expected_url, f"Expected '{expected_url}' but got '{current_url}'"
        
        

    @allure.title("Verify jobs menu expands and submenu is visible")
    @allure.tag("Sanity")
    def test_search_job_by_location(self):
        with allure.step("Step 1: Enter location only, click search, expect error"):
            try:
                self.web_driver_functions.enter_text(self.home_page.LOCATION_INPUT, "Jodhpur", "Entering location only")
                print("Successfully entered location")
            except Exception as e:
                print(f"Failed to enter location: {e}")
            
            self.web_driver_functions.click_element(self.home_page.JOB_SEARCH_BUTTON, "Clicking search without skill")

            # Check if error message for missing skill is displayed
            try:
                error_element = self.driver.find_element(By.XPATH, "//p[@class='error-message2 px-4 py-2 shadow-lg']")
                if error_element.is_displayed():
                    print("Error displayed as expected: Please enter a skill")
            except Exception:
                print("Expected error message not found")

        with allure.step("Step 2: Clear location, enter skill only, click search, redirect to new page"):
            try:
                self.driver.find_element(self.home_page.LOCATION_INPUT).clear()
                print("Cleared location input")
            except Exception as e:
                print(f"Failed to clear location: {e}")

            try:
                self.web_driver_functions.enter_text(self.home_page.SKILL_TEXTBOx, "Python", "Entering skill only")
                print("Successfully entered skill")
            except Exception as e:
                print(f"Failed to enter skill: {e}")
            
            self.web_driver_functions.click_element(self.home_page.JOB_SEARCH_BUTTON, "Clicking search with skill only")
            
            # Assuming redirection occurs here — wait or validate new page
            self.driver.back()  # Go back to previous page

        with allure.step("Step 3: Enter both skill and location, click search"):
            try:
                self.web_driver_functions.enter_text(self.home_page.SKILL_TEXTBOx, "Python", "Re-entering skill")
                self.web_driver_functions.enter_text(self.home_page.LOCATION_INPUT, "Jodhpur", "Re-entering location")
                print("Successfully entered both values")
            except Exception as e:
                print(f"Failed to enter both inputs: {e}")

            self.web_driver_functions.click_element(self.home_page.JOB_SEARCH_BUTTON, "Final search with both inputs")

            # Optional: add assertion or check for result page

