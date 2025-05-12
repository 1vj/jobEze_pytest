import os
import time
import allure
import logging
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


log = logging


class LaunchBrowser:
    driver_path = os.getcwd()
    this_platform = platform.system()
    driver = None
    if this_platform == 'Darwin':
        ChromeDriverPath = driver_path + "/drivers/mac_chromedriver/chromedriver"
    elif "linux" in this_platform.lower():  # validating the OS name with contains value
        ChromeDriverPath = driver_path + "/drivers/linux_chromedriver/chromedriver"
    else:
        ChromeDriverPath = driver_path + "/drivers/windows_chromedriver/chromedriver"
    # Logging variable
    log = logging

    def __init__(self):
        pass
        # InitialSystemSetupCheck.__init__(self)

    def launch_chrome_browser(self, host):
        chrome_options = webdriver.ChromeOptions()

        # Set default path of download location.
        files_downloaded_dir = os.path.join(os.getcwd(), 'file_downloaded')
        prefs = {'download.default_directory': files_downloaded_dir, "download.prompt_for_download": False,
                 "download.directory_upgrade": True, "safebrowsing.enabled": True}
        chrome_options.add_experimental_option('prefs', prefs)
        if host == 'local' and "linux" in self.this_platform.lower():  # validating the OS with contains value
            os.system('chmod 777 -R *')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("window-size=1920,1080")
        else:
            chrome_options.add_argument("--start-maximized")

        chrome_options.add_argument('--verbose')
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument('--perfLoggingPrefs')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-default-apps")
        # below options to skip the non-secure page error
        chrome_options.add_argument("--ignore-ssl-errors=yes")
        chrome_options.add_argument("--ignore-certificate-errors")
        capabilities = chrome_options.to_capabilities()
        capabilities['loggingPrefs'] = {'browser': 'ALL'}
        capabilities['loggingPrefs'] = {'performance': 'ALL'}

        if host == 'local':
            with allure.step('Launch Chrome browser'):
                log.info('\n' + '\n' + 'Launch Chrome browser' + '\n' + '\n')
                # self.driver = webdriver.Chrome(
                #     # executable_path=self.ChromeDriverPath,
                #     driver=webdriver.Chrome(service=service),
                #     desired_capabilities=capabilities
                # )
                # self.driver.implicitly_wait(5)

                os.makedirs(os.path.dirname(self.ChromeDriverPath), exist_ok=True)

                # Use webdriver-manager to download and set up ChromeDriver
                service = ChromeService(executable_path=ChromeDriverManager().install())

                # Initialize the Chrome WebDriver
                driver = webdriver.Chrome(service=service)
                self.driver.implicitly_wait(5)
                return driver

        elif host == 'remote' or None:
            with allure.step('Launch Chrome browser'):
                log.info('Launch Chrome browser')
                # self.driver = webdriver.Remote(
                #     command_executor='http://localhost:4444/wd/hub',
                #     desired_capabilities=capabilities)
                # self.driver.implicitly_wait(5)

                os.makedirs(os.path.dirname(self.ChromeDriverPath), exist_ok=True)

                # Use webdriver-manager to download and set up ChromeDriver
                service = ChromeService(executable_path=ChromeDriverManager().install())

                # Initialize the Chrome WebDriver
                driver = webdriver.Chrome(service=service)
                self.driver.implicitly_wait(5)
        else:
            print("either the 'host' and/or 'browsers' variables have not been set properly")

        yield driver  # This is where the testing happens
        return driver


# if __name__ == '__main__':
#     url = "https://appnot.viewglass.com/root/relaydata/55055/ncconfig.txt"
#     lb = LaunchBrowser()
#     dr = lb.launch_chrome_browser("local")
#     dr.get("https://www.google.com/?gws_rd=ssl")
#     time.sleep(30)
#     dr.quit()
