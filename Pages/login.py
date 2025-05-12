import time

import pytest

from webdriver.WebDriverHelper import WebDriverHelper
import logging

log = logging


class Login(WebDriverHelper):

    def __int__(self):
        WebDriverHelper.__init__(self)

'''   
    def login_CEP(self, role, username, password):
        role_id = "//Select[@id='exampleFormControlSelect1']/option[text()='" + role + "']"
        user_name_xpath = "#exampleInputEmail1"
        password_id = "//input[@id='exampleInputPassword1']"
        login_button_xpath = "//button[contains(text(),'Submit')]"

        self.role = self.find_element('visible', 'xpath', role_id, 40)
        self.role.click()

        self.uname = self.find_element('visible', 'css', user_name_xpath, 10)
        self.uname.send_keys(username)

        self.password = self.find_element('visible', 'xpath', password_id, 10)
        self.password.send_keys(password)

        time.sleep(2)
        self.login_button = self.find_element('visible', 'xpath', login_button_xpath, 10)
        self.login_button.click()

    def logout_cep(self):
        button_xpath = "//a[@id='navbarDropdownMenuLink']"
        signout_xpath = "//a[text()='Sign out']"

        self.button = self.find_element('visible', 'xpath', button_xpath, 20)
        self.button.click()
        time.sleep(5)
        self.signout = self.find_element('visible', 'xpath', signout_xpath, 20)
        self.signout.click()
'''
