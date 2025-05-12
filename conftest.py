import json
import os
import allure
import pytest
import logging
import datetime

from Pages.Fusionpackages import Pages
from selenium import webdriver
from webdriver.LaunchBrowserNew import LaunchBrowser

# Logging variable
log = logging

# Default test configuration (change values here)
default_env = "dev"
default_browser = "chrome"
default_headless = False

# Determine project root (2 levels up from this file)
project_root = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(project_root, 'config')):
    project_root = os.path.dirname(project_root)

# Create logs directory at project root
log_dir = os.path.join(project_root, "TestResults", "PytestLogs")
os.makedirs(log_dir, exist_ok=True)

# Generate unique log file per run
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f"pytest_log_{timestamp}.log")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def pytest_configure(config):
    """Force logs and reports to always write to the root-level testResults folder (case-sensitive)."""
    html_report = os.path.abspath(os.path.join(project_root, 'testResults', 'PytestHTMLReport', 'ViewSMCTestAutomationReport.htm'))
    allure_dir = os.path.abspath(os.path.join(project_root, 'testResults', 'AllureReports'))
    log_file = os.path.abspath(os.path.join(project_root, 'testResults', 'PytestLogs', 'PytestLog.txt'))

    config.option.htmlpath = html_report
    config.option.allure_report_dir = allure_dir
    config.option.log_file = log_file


# Load env config from JSON file
def load_env_config(env):
    config_path = os.path.join(project_root, "config", "env.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ Environment config file not found: {config_path}")

    with open(config_path) as f:
        env_data = json.load(f)

    if env not in env_data:
        raise ValueError(f"❌ Environment '{env}' not found in env.json.")

    return env_data[env]


def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="Environment to run tests against (dev, qa, stage)")
    parser.addoption("--host", action="store", default="local", help="host machine option")
    parser.addoption("--browser", action="store", help="Browser to run tests (chrome, firefox, edge)")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")
    parser.addoption("--role", action="store", default="Supervisor", help="role of the cep")
    parser.addoption("--name", action="store", default="akashk", help="input username")
    parser.addoption("--password", action="store", default="spanidea", help="input password")


@pytest.fixture(scope='function')
def browser(request):
    env = request.config.getoption("--env") or default_env
    host = request.config.getoption("--host")
    browser_type = request.config.getoption("--browser") or default_browser
    headless = request.config.getoption("--headless") or default_headless

    env_config = load_env_config(env)
    url = env_config.get("url")

    print(f"Launching test with URL: {url} (Host: {host}, ENV: {env}, Browser: {browser_type}, Headless: {headless})")

    lb = LaunchBrowser()
    driver = lb.launch_browser(host=host, browser=browser_type, headless=headless)
    driver.get(url)

    request.node.driver = driver

    yield driver

    with allure.step('Close Browser'):
        log.info('\n' + '\n' + 'Close Browser' + '\n' + '\n')
        driver.quit()


@pytest.fixture(scope='session')
def base_url():
    return "https://companydev.jobeze.com/backend"


@pytest.fixture(scope='session')
def api_url(base_url):
    return f"{base_url}/user-info"


@pytest.fixture(scope='session')
def auth_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InByaXlhbnNodTAwMUBnbWFpbC5jb20iLCJyb2xlX2lkIjoxLCJpYXQiOjE3NDY0MTk3NzcsImV4cCI6MTc0NjU5MjU3N30.Oz8NS1fXZdj3yhvDBRUuLwBjKtWdeD8jPBYUagdASdw"


@pytest.fixture(scope='function')
def test_env_url(url):
    yield url


@pytest.fixture(scope='function')
def test_env_role(role):
    yield role


@pytest.fixture(scope='function')
def test_env_name(name):
    yield name


@pytest.fixture(scope='function')
def test_env_password(password):
    yield password


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    summary = []
    extra = getattr(report, 'extra', [])
    driver = getattr(item, 'driver', None)
    xfail = hasattr(report, 'wasxfail')
    report.TestCaseDescription = str(item.function.__doc__)

    if report.when == 'call' or report.when == "setup":
        extra.append(pytest_html.extras.html("<p>" + str(item.function.__doc__) + "</p>"))
        if (report.skipped and xfail) or (report.failed and not xfail):
            if driver is not None:
                _gather_url(item, report, driver, summary, extra)
                _gather_screenshot(item, report, driver, summary, extra)
                try:
                    allure.attach(driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)
                except Exception as ex:
                    print("something wrong with screenshot in conftest: ", ex)
            else:
                extra.append(pytest_html.extras.html('<p>' + 'This test case does not require screenshot on failure. '
                                                     'Please see logs for details.' + '<p>'))

        if summary:
            report.sections.append(('\n' + 'Test Execution Log Summary' + '\n', '\n'.join(summary)))

        report.extra = extra


def _gather_url(item, report, driver, summary, extra):
    try:
        url = driver.current_url
    except Exception as e:
        summary.append('WARNING: Failed to gather URL: {0}'.format(e))
        return
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is not None:
        extra.append(pytest_html.extras.url(url))
    summary.append('URL: {0}'.format(url))


def _gather_screenshot(item, report, driver, summary, extra):
    try:
        screenshot = driver.get_screenshot_as_base64()
    except Exception as e:
        summary.append('WARNING: Failed to gather screenshot: {0}'.format(e))
        return
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is not None:
        extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))


@pytest.fixture(scope='function')
def test_case_template(
        browser,
        test_env_url,
        test_env_role,
        test_env_name,
        test_env_password
):
    class WebEnvironmentSetup(Pages):

        def __init__(self):
            import logging
            import time

            self.driver = browser
            self.log = logging
            self.time = time
            self.url = test_env_url
            self.role = test_env_role
            self.name = test_env_name
            self.password = test_env_password

    test_case_template_init = WebEnvironmentSetup()
    yield test_case_template_init
