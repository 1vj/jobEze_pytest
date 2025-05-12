import allure
import pytest
import logging
from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from utils.UtilsPackage import UtilsPackage

log = logging.getLogger(__name__)


class WebDriverHelper(UtilsPackage):

    def __init__(self, driver):
        super().__init__()
        if driver is None:
            raise ValueError("Driver cannot be None")
        self.driver = driver

    def find_element(self, condition: str, locator: tuple, wait_time: int = 30):
        """Finds an element using a locator tuple and a wait condition."""
        wait = WebDriverWait(self.driver, wait_time)
        locator_map = {
            'visible': EC.visibility_of_element_located,
            'selected': EC.element_to_be_selected,
            'clickable': EC.element_to_be_clickable,
            'presence': EC.presence_of_element_located
        }
        if condition not in locator_map:
            raise ValueError(f"Unknown condition: {condition}")
        try:
            return wait.until(locator_map[condition](locator))
        except Exception as e:
            pytest.fail(str(e))

    def get_elements(self, locator: tuple):
        return self.driver.find_elements(*locator)

    def click(self, element):
        try:
            element.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def clear_all_text(self, element):
        length = len(element.get_attribute('value'))
        element.send_keys(length * Keys.BACKSPACE)

    def enter_text(self, locator: tuple, text: str, comment: str):
        with allure.step(f"Enter text in {comment}"):
            log.info(f"Entering text '{text}' in {comment}")
            element = self.find_element('visible', locator)
            element.clear()
            element.send_keys(text)

    def click_element(self, locator: tuple, comment: str):
        with allure.step(f"Click element: {comment}"):
            log.info(f"Clicking element: {comment}")
            element = self.find_element('visible', locator)
            self.click(element)

    def assert_element_attribute(self, locator: tuple, attribute: str, comment: str):
        with allure.step(f"Asserting element attribute: {comment}"):
            log.info(f"Asserting {attribute} exists on {comment}")
            element = self.find_element('visible', locator)
            assert element.get_attribute(attribute)

    def get_element_attribute_value(self, locator: tuple, comment: str):
        with allure.step(f"Getting attribute value from {comment}"):
            log.info(f"Getting attribute value from {comment}")
            return self.find_element('visible', locator).get_attribute("value")

    def wait_for_text_in_element(self, locator: tuple, text: str, wait_time: int = 30):
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.text_to_be_present_in_element(locator, text))

    def is_element_enabled(self, locator: tuple):
        return self.find_element('presence', locator).is_enabled()

    def is_element_displayed(self, locator: tuple):
        return self.find_element('presence', locator).is_displayed()

    def wait_for_element_to_disappear(self, locator: tuple, wait_time: int = 30):
        WebDriverWait(self.driver, wait_time).until(EC.invisibility_of_element_located(locator))

    def scroll_to_element(self, locator: tuple):
        element = self.find_element('visible', locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def hover_over_element(self, locator: tuple):
        element = self.find_element('visible', locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def get_element_text(self, locator: tuple, comment: str = ""):
        with allure.step(f"Getting text from element: {comment}"):
            log.info(f"Getting text from element: {comment}")
            element = self.find_element('visible', locator)
            return element.text

    def select_option_from_dropdown(self, select_locator: tuple, option_text: str, comment: str):
        with allure.step(f"Selecting dropdown option {option_text} for {comment}"):
            select_elem = Select(self.find_element('visible', select_locator))
            select_elem.select_by_visible_text(option_text)

    def select_option_by_index(self, select_locator: tuple, index: int, comment: str = ""):
        with allure.step(f"Selecting option index {index} for {comment}"):
            select_elem = Select(self.find_element('visible', select_locator))
            select_elem.select_by_index(index)

    def select_option_by_value(self, select_locator: tuple, value: str, comment: str = ""):
        with allure.step(f"Selecting value {value} in {comment}"):
            select_elem = Select(self.find_element('visible', select_locator))
            select_elem.select_by_value(value)

    def get_all_dropdown_options(self, select_locator: tuple, comment: str = ""):
        with allure.step(f"Getting all options from dropdown: {comment}"):
            select_elem = Select(self.find_element('visible', select_locator))
            return [opt.text for opt in select_elem.options]

    def double_click(self, locator: tuple, comment: str = ""):
        with allure.step(f"Double-clicking on: {comment}"):
            element = self.find_element('visible', locator)
            ActionChains(self.driver).double_click(element).perform()

    def drag_and_drop(self, source: tuple, target: tuple):
        src_elem = self.find_element('visible', source)
        tgt_elem = self.find_element('visible', target)
        ActionChains(self.driver).drag_and_drop(src_elem, tgt_elem).perform()

    def upload_file(self, locator: tuple, file_path: str, comment: str = ""):
        with allure.step(f"Uploading file to: {comment}"):
            file_input = self.find_element('visible', locator)
            file_input.send_keys(file_path)

    def retry_click(self, locator: tuple, retries: int = 3, comment: str = ""):
        for attempt in range(retries):
            try:
                element = self.find_element('clickable', locator)
                element.click()
                return
            except exceptions.ElementClickInterceptedException:
                if attempt < retries - 1:
                    log.warning(f"Retrying click {attempt+1}/{retries}: {comment}")
                else:
                    pytest.fail(f"Failed to click after {retries} attempts: {comment}")

    def wait_for_element_attribute(self, locator: tuple, attribute: str, expected_value: str, wait_time: int = 30):
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: driver.find_element(*locator).get_attribute(attribute) == expected_value
        )

    def check_element_attribute_value(self, locator: tuple, attribute: str, expected_value: str, comment: str = ""):
        element = self.find_element('visible', locator)
        actual_value = element.get_attribute(attribute)
        assert actual_value == expected_value, \
            f"Expected {attribute} to be {expected_value}, but got {actual_value}"

    def toggle_checkbox(self, locator: tuple, comment: str = ""):
        checkbox = self.find_element('clickable', locator)
        checkbox.click()

    def set_checkbox(self, locator: tuple, desired_state: bool, comment: str = ""):
        checkbox = self.find_element('clickable', locator)
        if checkbox.is_selected() != desired_state:
            checkbox.click()

    def get_element_count(self, locator: tuple):
        return len(self.driver.find_elements(*locator))

    def does_element_exist(self, locator: tuple):
        return len(self.driver.find_elements(*locator)) > 0

    def wait_until_element_contains_text(self, locator: tuple, expected_text: str, wait_time: int = 30):
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: expected_text in driver.find_element(*locator).text
        )

    def focus_on_element(self, locator: tuple):
        element = self.find_element('visible', locator)
        self.driver.execute_script("arguments[0].focus();", element)

    def get_element_css_value(self, locator: tuple, css_property: str, comment: str = ""):
        element = self.find_element('visible', locator)
        return element.value_of_css_property(css_property)

    def get_elements_text(self, locator: tuple, comment: str = ""):
        return [el.text for el in self.get_elements(locator)]

    def open_new_tab_with_url(self, url: str):
        self.driver.execute_script(f"window.open('{url}');")

    def go_to_url(self, url: str):
        self.driver.get(url)

    def check_current_url(self, expected_url: str):
        assert self.driver.current_url == expected_url

    def get_current_url(self):
        return self.driver.current_url

    def refresh(self):
        self.driver.refresh()

    def accept_system_alert(self):
        self.driver.switch_to.alert.accept()

    def dismiss_system_alert(self):
        self.driver.switch_to.alert.dismiss()

    def get_text_system_alert(self):
        return self.driver.switch_to.alert.text

    def wait_for_alert_to_appear(self, wait_time: int = 30):
        WebDriverWait(self.driver, wait_time).until(EC.alert_is_present())

    def switch_to_iframe(self, iframe_element):
        self.driver.switch_to.frame(iframe_element)

    def switch_to_default_content_from_iframe(self):
        self.driver.switch_to.default_content()

    def quit_driver(self):
        self.driver.quit()

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def wait_for_element_to_appear(self, locator: tuple, wait_time: int = 30):
        WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))

    def clear_and_enter_text(self, locator: tuple, text: str, comment: str = ""):
        element = self.find_element('visible', locator)
        element.clear()
        element.send_keys(text)
