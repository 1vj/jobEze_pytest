import allure
import pytest
import time
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


import logging

from utils.UtilsPackage import UtilsPackage

log = logging


class WebDriverHelper(UtilsPackage):

    def __init__(self, driver) -> object:
        UtilsPackage.__init__(self)
        # self.driver = self.create_driver()
        # if driver is None:
        #     raise ValueError("Driver cannot be None")
        self.driver = driver

    def create_driver(self):
        return webdriver.Chrome()  # Return an instance, not a generator

    def find_element(self, condition, locator, value, wait_time):
        """
        This function handles the way that an element is searched
        """

        element = ""
        if wait_time:
            # Custom wait time
            wait = WebDriverWait(self.driver, wait_time)
        else:
            wait = WebDriverWait(self.driver, 30)

        try:

            if condition == 'visible':
                if locator == 'xpath':
                    element = wait.until(EC.visibility_of_element_located((By.XPATH, value)))
                elif locator == 'id':
                    element = wait.until(EC.visibility_of_element_located((By.ID, value)))
                elif locator == 'css':
                    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, value)))
                elif locator == 'classname':
                    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, value)))
                elif locator == 'tagname':
                    element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, value)))
                elif locator == 'linktext':
                    element = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, value)))
                elif locator == 'partiallinktext':
                    element = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, value)))
                elif locator == 'name':
                    element = wait.until(EC.visibility_of_element_located((By.NAME, value)))
                return element

            elif condition == 'selected':
                if locator == 'xpath':
                    element = wait.until(EC.element_to_be_selected((By.XPATH, value)))
                elif locator == 'id':
                    element = wait.until(EC.element_to_be_selected((By.ID, value)))
                elif locator == 'css':
                    element = wait.until(EC.element_to_be_selected((By.CSS_SELECTOR, value)))
                elif locator == 'classname':
                    element = wait.until(EC.element_to_be_selected((By.CLASS_NAME, value)))
                elif locator == 'tagname':
                    element = wait.until(EC.element_to_be_selected((By.TAG_NAME, value)))
                elif locator == 'linktext':
                    element = wait.until(EC.element_to_be_selected((By.LINK_TEXT, value)))
                elif locator == 'partiallinktext':
                    element = wait.until(EC.element_to_be_selected((By.PARTIAL_LINK_TEXT, value)))
                elif locator == 'name':
                    element = wait.until(EC.element_to_be_selected((By.NAME, value)))
                return element

            elif condition == 'clickable':
                if locator == 'xpath':
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, value)))
                elif locator == 'id':
                    element = wait.until(EC.element_to_be_clickable((By.ID, value)))
                elif locator == 'css':
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, value)))
                elif locator == 'classname':
                    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, value)))
                elif locator == 'tagname':
                    element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, value)))
                elif locator == 'linktext':
                    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, value)))
                elif locator == 'partiallinktext':
                    element = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, value)))
                elif locator == 'name':
                    element = wait.until(EC.element_to_be_clickable((By.NAME, value)))
                return element

            elif condition == 'presence':
                if locator == 'xpath':
                    element = wait.until(EC.presence_of_element_located((By.XPATH, value)))
                elif locator == 'id':
                    element = wait.until(EC.presence_of_element_located((By.ID, value)))
                elif locator == 'css':
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
                elif locator == 'classname':
                    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, value)))
                elif locator == 'tagname':
                    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, value)))
                elif locator == 'linktext':
                    element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, value)))
                elif locator == 'partiallinktext':
                    element = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, value)))
                elif locator == 'name':
                    element = wait.until(EC.presence_of_element_located((By.NAME, value)))
                return element

        except Exception as e:
            pytest.fail(str(e))
            self.driver.quit()

        # return element

    def clear_all_text(self, element):
        """
        This function clears all text in
        a given input element
        """
        length = len(element.get_attribute('value'))
        element.send_keys(length * Keys.BACKSPACE)

    def click(self, element):
        """
        This function handles element click
        exceptions where part of the element
        is not clickable
        """
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def check_element_xpath_present(self, xpath):
        """
        This function checks that the given xpath
        is present within the page
        """
        assert len(self.driver.find_elements_by_xpath(xpath)) >= 1

    def check_element_xpath_not_present(self, xpath):
        """
        This function checks that the given xpath
        is not present within the page
        """
        assert len(self.driver.find_elements_by_xpath(xpath)) == 0

    def check_page_contains_string(self, string):
        """
        This function checks that the given string
        present within the page
        """
        self.check_element_xpath_present("//*[contains(text(), '" + string + "')]")

    def check_page_does_not_contain_string(self, string):
        """
        This function checks that the given string
        is not present within the page
        """
        self.check_element_xpath_not_present("//*[contains(text(), '" + string + "')]")

    def open_new_tab_with_url(self, url):
        """
        This function opens a new
        tab with a specified url
        """
        self.driver.execute_script("window.open('" + url + "');")

    def check_current_url(self, url):
        """
        This function checks the current
        url with the specified url
        """
        assert self.driver.current_url == url

    def go_to_url(self, url):
        """
        This function redirects the browser
        to the specified url
        """
        self.driver.get(url)

    def go_to_page(self, page):
        """
        This function redirects the browser
        to the current url with a specified page
        """
        self.go_to_url(self.driver.current_url + page)

    def refresh(self):
        """
        This function refreshes the current
        browser page
        """
        self.driver.get(self.driver.current_url)

    def get_current_url(self):
        """
        This function returns the current browser url
        """
        return self.driver.current_url

    def accept_system_alert(self):
        """
        This function accepts a system alert
        """
        self.driver.switch_to.alert.accept()

    def get_text_system_alert(self):
        """
        This function extract text from a system alert
        """
        return self.driver.switch_to.alert.text

    def get_elements_by_xpath(self, element_xpath):
        """
        This function returns a list of elements that are found by the specified xpath
        """
        return self.driver.find_elements(By.XPATH, element_xpath)

    def type_into_system_alert(self, keys):
        """
        This function types text into a system alert
        """
        self.driver.switch_to.alert.send_keys(keys)

    def switch_to_iframe(self, iframe_element):
        """
        This function switches the browser to the
        iframe element. This function is mainly
        used to find elements within an iframe
        since any elements within an iframe cannot
        be found regularly by the browser
        """
        self.driver.switch_to.frame(iframe_element)

    def check_is_selected(self, element_xpath):
        """
        This method determines if an element is
        selected or not. It returns true if the
        element is selected and false if it is not.
        It is widely used on check boxes, radio buttons
        and options in a select.
        """
        return self.driver.find_element(By.XPATH, element_xpath).is_selected()

    def switch_to_window(self, window_no):
        """
        This method provides option to
        handle multiple windows using 'window_handles'.
        :param window_no: this is a index no. of window
        on which you want to switch
        """
        window = self.driver.window_handles
        self.driver.switch_to.window(window[window_no])

    def scroll_to_given_element(self, locator, value, wait_time):
        """
            This method provides option to
            scroll to given element on the UI .
            :param condition: Wait condition to check the element present in ui
            locator: This is type of an element locator
            value : this is a locator on the
            window, where we need to scroll to that position
            wait_time : Max wait time to find the element
        """
        element = self.find_element('presence', locator, value, wait_time)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def switch_to_default_content_from_iframe(self):
        """
        This method provides option to
        Switch back to default contentf fro  iframe
        """
        self.driver.switch_to.default_content()

    def quit_driver(self):
        """
        Method to quit the driver
        """
        self.driver.quit()

    def select_option_from_drop_down(self, selection_xpath, option_text, comment):
        with allure.step('Find the selection ' + comment):
            log.info('Find the selection ' + comment)
            selection = Select(self.find_element('visible', 'xpath', selection_xpath, ''))

        with allure.step('Find option to select'):
            log.info('Find option to select')
            OptionToSelect = self.find_element('visible', 'xpath',
                                               selection_xpath + "//option[contains(text(), '" + str(
                                                   option_text) + "')]", '')

        with allure.step('Select option'):
            log.info('Select option')
            selection.select_by_visible_text(OptionToSelect.text)

    def click_element(self, element_xpath, comment):
        with allure.step('Find element ' + comment):
            log.info('Find element ' + comment)
            element = self.find_element('visible', 'xpath', element_xpath, '')

        with allure.step('Click on element '):
            log.info('Click on element ')
            self.click(element)

    def click_element_and_catch_stale_element_reference_exception(self, element_xpath, comment):
        with allure.step('Find element ' + comment):
            log.info('Find element ' + comment)
            element = self.find_element('visible', 'xpath', element_xpath, '')

        try:
            with allure.step('Click on element '):
                log.info('Click on element ')
                self.click(element)
        except exceptions.StaleElementReferenceException:
            element = self.find_element('visible', 'xpath', element_xpath, '')
            self.click(element)

    def compare_element_text_with_value(self, element_xpath, val):
        with allure.step('Find element '):
            log.info('Find element ')
            element = self.find_element('visible', 'xpath', element_xpath, '')

        with allure.step('Compare element text with ' + str(val)):
            log.info('Compare element text with ' + str(val))
            assert element.text == val

    def click_element_and_accept_alert(self, element_xpath, comment):
        with allure.step('Click on element and accept alert'):
            log.info('try_accept_alert(): Click on element')
            self.click_element(element_xpath, comment)
            time.sleep(2)
            try:
                self.accept_system_alert()
            except:
                log.info('no popup, skip it as expected\n')

    def check_checkbox_enabled(self, element_xpath, comment):
        with allure.step(comment):
            log.info(comment)
            self.find_element('visible', 'xpath', element_xpath, '')
            return self.check_is_selected(element_xpath)

    def assert_checkbox_enabled(self, element_xpath, comment):
        with allure.step(comment):
            log.info(comment)
            self.find_element('visible', 'xpath', element_xpath, '')

            assert self.check_is_selected(element_xpath)

    def enter_text(self, element_xpath, txt, comment):
        with allure.step('Find element: ' + comment):
            log.info('Find element: ' + comment)
            element = self.find_element('visible', 'xpath', element_xpath, '')

        with allure.step('Enter "' + txt + '" to element: ' + comment):
            log.info('Enter "' + txt + '" to element: ' + comment)
            element.clear()
            element.send_keys(txt)

    def assert_element_attribute(self, element_xpath, attribute, comment):
        with allure.step('Find element: ' + comment):
            log.info('Find element: ' + comment)
            assert self.find_element('visible', 'xpath', element_xpath, '').get_attribute(attribute)

    def get_element_attribute_value(self, element_xpath, comment):
        with allure.step('Find %s get attribute value.' % comment):
            log.info('Find %s get attribute value.' % comment)
            return self.find_element('visible', 'xpath', element_xpath, '').get_attribute("value")

