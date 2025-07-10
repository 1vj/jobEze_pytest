import pytest
import logging
import allure
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.JobezePGObject.HomePage import HomePage
from webdriver import WebDriverHelperNew
import time

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
        self.wait = WebDriverWait(self.driver, 20)

    @allure.title("Search jobs by location and skill with error handling")
    def test_search_job_by_location(self):
        log.info("Starting test_search_job_by_location")

        # Step 1: Enter location only, expect error for missing skill
        with allure.step("Step 1: Enter location only, expect error"):
            self.web_driver_functions.enter_text(self.home_page.LOCATION_INPUT, "Jodhpur", "Entering location")
            # time.sleep(50)
            self.web_driver_functions.click_element(self.home_page.JOB_SEARCH_BUTTON, "Search without skill")

            try:
                error = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'error-message2')]"))
                )
                assert "please enter a skill" in error.text.lower()
                log.info(" Correct error displayed for missing skill")
            except Exception as e:
                log.error(f" Error message not displayed as expected: {e}")
                assert False, "Missing skill error not shown"

        # Step 2: Clear location, enter skill only
        with allure.step("Step 2: Enter skill only"):
            try:
                location_input = self.driver.find_element(*self.home_page.LOCATION_INPUT)
                location_input.clear()
            except Exception as e:
                log.warning(f"Failed to clear location input: {e}")

            self.web_driver_functions.enter_text(self.home_page.SKILL_TEXTBOx, "Python", "Entering skill")
            self.web_driver_functions.click_element(self.home_page.JOB_SEARCH_BUTTON, "Search with skill only")

            try:
                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "jbscroll")))
                log.info("Job results displayed for skill only")
                self.driver.back()
            except:
                log.warning("Job results not shown for skill only")

        # Step 3: Enter both skill and location
        with allure.step("Step 3: Enter both skill and location"):
            self.web_driver_functions.enter_text(self.home_page.SKILL_TEXTBOx, "Python", "Re-entering skill")
            self.web_driver_functions.enter_text(self.home_page.LOCATION_INPUT, "Alberta", "Re-entering location")
            self.web_driver_functions.click_element(self.home_page.JOB_SEARCH_BUTTON, "Search with both")
            time.sleep(10)

            job_containers = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "jbscroll"))
            )

            assert len(job_containers) >= 2, "Expected at least two jbscroll containers"

            for index, container in enumerate(job_containers):
                log.info(f"------ Inspecting Card {index + 1} ------")

                # Get the card inside the container
                try:
                    card = container.find_element(
                        By.XPATH, ".//div[contains(@class, 'card') and contains(@class, 'mb-3')]"
                    )
                except Exception as e:
                    log.error(f"Card not found in container {index + 1}: {str(e)}")
                    continue

                card_text = card.text.lower()

                if index == 0:
                    # Validate location in card 1
                    log.info(f"Card 1 summary: {card_text[:100]}...")
                    assert "alberta" in card_text, "Card 1 missing location 'Alberta'"

                elif index == 1:
                    # Validate skill in card 2
                    skill_xpath = ".//div[contains(@class, 'MuiStack-root') and contains(@class, 'css-1rkgh5')]//span"
                    skill_elements = container.find_elements(By.XPATH, skill_xpath)
                    skills = [el.text.strip().lower() for el in skill_elements if el.text.strip()]
                    log.info(f"Card 2 skills: {skills}")
                    assert "python" in skills, "Card 2 does not contain skill 'Python'"
