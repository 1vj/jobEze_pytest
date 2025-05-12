import os
import platform
import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService


class LaunchBrowser:
    driver_path = os.getcwd()
    this_platform = platform.system()
    driver = None

    if this_platform == 'Darwin':
        ChromeDriverPath = os.path.join(driver_path, "drivers/mac_chromedriver/chromedriver")
    elif "linux" in this_platform.lower():
        ChromeDriverPath = os.path.join(driver_path, "drivers/linux_chromedriver/chromedriver")
    else:
        ChromeDriverPath = os.path.join(driver_path, "drivers/windows_chromedriver/chromedriver")

    log = logging

    def __init__(self):
        pass

    def launch_browser(self, host, browser="chrome", headless=False):
        browser = browser.lower()

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            driver_manager = ChromeDriverManager().install()
            service = ChromeService(executable_path=driver_manager)
            driver_class = webdriver.Chrome

        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            driver_manager = GeckoDriverManager().install()
            service = FirefoxService(executable_path=driver_manager)
            driver_class = webdriver.Firefox

        elif browser == "edge":
            options = webdriver.EdgeOptions()
            driver_manager = EdgeChromiumDriverManager().install()
            service = EdgeService(executable_path=driver_manager)
            driver_class = webdriver.Edge

        else:
            raise ValueError(f"Unsupported browser: {browser}")

        files_downloaded_dir = os.path.join(os.getcwd(), 'file_downloaded')
        if browser == "chrome":
            prefs = {
                'download.default_directory': files_downloaded_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option('prefs', prefs)

        if headless:
            if browser == "chrome":
                options.add_argument('--headless=new')
            else:
                options.add_argument('--headless')
            options.add_argument("window-size=1920,1080")
        else:
            if browser == "chrome":
                options.add_argument("--start-maximized")

        # Common arguments
        options.add_argument('--verbose')
        options.add_argument("--test-type")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        options.add_argument("--enable-automation")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")

        self.log.info(f'Launching {browser.capitalize()} browser')
        driver = driver_class(service=service, options=options)
        driver.implicitly_wait(5)
        return driver
