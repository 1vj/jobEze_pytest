# import logging
# from selenium.webdriver.common.by import By
# from webdriver.WebDriverHelperNew import WebDriverHelper
#
# log = logging.getLogger(__name__)
#
#
# class HomePage:
#     def __init__(self, driver):
#         self.driver = driver
#         self.helper = WebDriverHelper(driver)
#
#     def click_home_link(self):
#         log.info("Clicking Home link on navbar")
#         self.helper.click_element("//a[text()='Home']", "Clicking Home link")
#
#     def click_jobs_menu(self):
#         log.info("Clicking Jobs menu on navbar")
#         self.helper.click_element("//*[contains(@class,'nav-jobs')]", "Clicking Jobs Menu")
#
#     def is_login_button_visible(self):
#         log.info("Checking if LOGIN button is visible")
#         return self.helper.is_element_displayed("//button[contains(text(), 'LOGIN')]")
#
#     def is_sign_up_button_visible(self):
#         log.info("Checking if SIGN UP button is visible")
#         return self.helper.is_element_displayed("//button[contains(text(), 'SIGN UP')]")
#
#     def is_submenu_visible(self):
#         log.info("Checking if 'Management' submenu is visible")
#         return self.helper.is_element_displayed("//b[normalize-space()='Management']")


import logging
from selenium.webdriver.common.by import By
from webdriver.WebDriverHelperNew import WebDriverHelper

log = logging.getLogger(__name__)


class HomePage:
    # Centralized locators
    HOME_LINK = (By.XPATH, "//a[text()='Home']")
    JOBS_MENU = (By.XPATH, "//*[contains(@class,'nav-jobs')]")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'LOGIN')]")
    SIGN_UP_BUTTON = (By.XPATH, "//button[contains(text(), 'SIGN UP')]")
    MANAGEMENT_SUBMENU = (By.XPATH, "//b[normalize-space()='Management']")

    def __init__(self, driver):
        self.driver = driver
        self.helper = WebDriverHelper(driver)

    def click_home_link(self):
        log.info("Clicking Home link on navbar")
        self.helper.click_element(self.HOME_LINK, "Clicking Home link")

    def click_jobs_menu(self):
        log.info("Clicking Jobs menu on navbar")
        self.helper.click_element(self.JOBS_MENU, "Clicking Jobs Menu")

    def is_login_button_visible(self):
        log.info("Checking if LOGIN button is visible")
        return self.helper.is_element_displayed(self.LOGIN_BUTTON)

    def is_sign_up_button_visible(self):
        log.info("Checking if SIGN UP button is visible")
        return self.helper.is_element_displayed(self.SIGN_UP_BUTTON)

    def is_submenu_visible(self):
        log.info("Checking if 'Management' submenu is visible")
        return self.helper.is_element_displayed(self.MANAGEMENT_SUBMENU)
