import pytest
import logging
import allure
import json
from Pages.JobezePGObject.HomePage import HomePage

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
    @allure.tag("Regression")
    def test_expand_jobs_menu(self):
        with allure.step("Clicking Jobs menu and checking for submenu visibility"):
            log.info("Clicking on Jobs menu")
            self.home_page.click_jobs_menu()
            visible = self.home_page.is_submenu_visible()
            log.info(f"Is submenu visible: {visible}")
            assert visible, "Submenu is not visible after clicking Jobs menu"

    @allure.title("Verify login and signup buttons are visible")
    @allure.tag("Sanity", "UI")
    def test_login_and_sign_up_buttons_visible(self):
        with allure.step("Checking visibility of Login button"):
            visible_login = self.home_page.is_login_button_visible()
            log.info(f"Login button visible: {visible_login}")
            assert visible_login, "Login button is not visible"

        with allure.step("Checking visibility of Sign Up button"):
            visible_signup = self.home_page.is_sign_up_button_visible()
            log.info(f"Sign Up button visible: {visible_signup}")
            assert visible_signup, "Sign Up button is not visible"
