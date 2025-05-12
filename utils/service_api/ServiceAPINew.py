import time
import logging
import allure
import requests
import pytest
from jsonschema import validate, ValidationError

log = logging.getLogger(__name__)  # Configure logging


class ServiceAPI:
    def __init__(self, token=None):
        """Initialize the API client with an optional authorization token."""
        self.token = token

    def get_headers(self):
        """Construct the headers, including the authorization token if provided."""
        headers = {
            'Content-Type': 'application/json',
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'  # Include token in the Authorization header
        return headers

    @allure.step("Sending GET request to API")
    def get_service_response(self, api_url):
        """Send GET request to the given API URL with optional authorization and return the response."""
        log.info(f'Sending GET request to {api_url}')
        try:
            headers = self.get_headers()
            response = requests.get(api_url, headers=headers)
            log.info(f'Response received: {response.status_code}')
            # Log the response content
            log.info(f'Response Content:, {response.text}')
            return response
        except requests.exceptions.RequestException as e:
            log.error(f'Error while sending GET request to {api_url}: {str(e)}')
            pytest.fail(f"API GET request failed: {e}")

    @allure.step("Sending POST request to API")
    def post_service_response(self, api_url, payload):
        """Send POST request to the given API URL with payload and optional authorization."""
        log.info(f'Sending POST request to {api_url} with payload: {payload}')
        try:
            headers = self.get_headers()
            response = requests.post(api_url, json=payload, headers=headers)
            log.info(f'Response received: {response.status_code}')
            # Log the response content
            log.info(f'Response Content:, {response.text}')
            return response
        except requests.exceptions.RequestException as e:
            log.error(f'Error while sending POST request to {api_url}: {str(e)}')
            pytest.fail(f"API POST request failed: {e}")

    @allure.step("Sending PATCH request to API")
    def patch_service_response(self, api_url, payload):
        """Send PATCH request to the given API URL with payload and optional authorization."""
        log.info(f'Sending PATCH request to {api_url} with payload: {payload}')
        try:
            headers = self.get_headers()
            response = requests.patch(api_url, json=payload, headers=headers)
            log.info(f'Response received: {response.status_code}')
            # Log the response content
            log.info(f'Response Content:, {response.text}')
            return response
        except requests.exceptions.RequestException as e:
            log.error(f'Error while sending PATCH request to {api_url}: {str(e)}')
            pytest.fail(f"API PATCH request failed: {e}")

    @allure.step("Sending DELETE request to API")
    def delete_service_response(self, api_url):
        """Send DELETE request to the given API URL with optional authorization."""
        log.info(f'Sending DELETE request to {api_url}')
        try:
            headers = self.get_headers()
            response = requests.delete(api_url, headers=headers)
            log.info(f'Response received: {response.status_code}')
            # Log the response content
            log.info(f'Response Content:, {response.text}')
            return response
        except requests.exceptions.RequestException as e:
            log.error(f'Error while sending DELETE request to {api_url}: {str(e)}')
            pytest.fail(f"API DELETE request failed: {e}")

    @allure.step("Validating API response")
    def validate_response(self, response, expected_status=200):
        """Validate the API response with the expected status."""
        assert response is not None, "No response received from the API"
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}, but got {response.status_code}"
        log.info(f'API response validation successful, status code: {response.status_code}')

    @allure.step("Sending PUT request to API")
    def put_service_response(self, api_url, payload):
        """Send PUT request to the given API URL with payload and optional authorization."""
        log.info(f'Sending PUT request to {api_url} with payload: {payload}')
        try:
            headers = self.get_headers()
            response = requests.put(api_url, json=payload, headers=headers)
            log.info(f'Response received: {response.status_code}')
            log.info(f'Response Content: {response.text}')
            return response
        except requests.exceptions.RequestException as e:
            log.error(f'Error while sending PUT request to {api_url}: {str(e)}')
            pytest.fail(f"API PUT request failed: {e}")

    @allure.step("Fetching JSON from API response")
    def get_json_response(self, response):
        """Parse and return the JSON content of a response."""
        try:
            json_data = response.json()
            log.info("JSON data retrieved successfully")
            return json_data
        except ValueError as e:
            log.error("Error parsing JSON response")
            pytest.fail(f"Failed to parse JSON response: {e}")

    @allure.step("Validating JSON response data")
    def validate_json_key(self, response, key, expected_value):
        """Validate that a specific key in the JSON response matches the expected value."""
        json_data = self.get_json_response(response)
        assert key in json_data, f"Key '{key}' not found in the response"
        assert json_data[key] == expected_value, f"Expected '{key}' to be '{expected_value}', but got '{json_data[key]}'"
        log.info(f"Validated {key} = {expected_value}")

    @allure.step("Checking API response time")
    def check_response_time(self, response, max_time=2000):
        """Validate that the API response time is within an acceptable limit (in milliseconds)."""
        response_time = response.elapsed.total_seconds() * 1000
        assert response_time <= max_time, f"Response time exceeded: {response_time} ms"
        log.info(f"Response time is within limit: {response_time} ms")

    @allure.step("Sending request with custom headers")
    def custom_headers_request(self, api_url, payload=None, headers=None, method="GET"):
        """Send a request with custom headers and optional payload."""
        try:
            if headers is None:
                headers = self.get_headers()
            log.info(f'Sending {method} request to {api_url} with headers: {headers} and payload: {payload}')
            response = requests.request(method, api_url, json=payload, headers=headers)
            log.info(f'Response received: {response.status_code}')
            log.info(f'Response Content: {response.text}')
            return response
        except requests.exceptions.RequestException as e:
            log.error(f'Error while sending {method} request to {api_url}: {str(e)}')
            pytest.fail(f"{method} request failed: {e}")

    @allure.step("Logging full API request and response details")
    def log_full_response(self, response):
        """Logs the complete details of the request and response."""
        log.info(f"Request Method: {response.request.method}")
        log.info(f"Request URL: {response.request.url}")
        log.info(f"Request Headers: {response.request.headers}")
        if response.request.body:
            log.info(f"Request Body: {response.request.body}")
        log.info(f"Response Status Code: {response.status_code}")
        log.info(f"Response Headers: {response.headers}")
        log.info(f"Response Text: {response.text}")

    @allure.step("Validating content type in response header")
    def validate_content_type(self, response, expected_content_type="application/json"):
        """Validates that the response has the expected content type."""
        content_type = response.headers.get("Content-Type", "")
        assert expected_content_type in content_type, \
            f"Expected content type {expected_content_type}, but got {content_type}"
        log.info(f"Content type validation successful: {content_type}")

    @allure.step("Extracting header from response")
    def get_response_header(self, response, header_name):
        """Extracts a specific header from the response."""
        header_value = response.headers.get(header_name)
        if header_value:
            log.info(f"Header '{header_name}': {header_value}")
        else:
            log.warning(f"Header '{header_name}' not found in the response")
        return header_value

    @allure.step("Checking if JSON key exists in response")
    def does_json_key_exist(self, response, key):
        """Checks if a specific JSON key exists in the response data."""
        json_data = self.get_json_response(response)
        exists = key in json_data
        log.info(f"Key '{key}' exists in JSON response: {exists}")
        return exists

    @allure.step("Retrying request on failure")
    def retry_request(self, api_url, payload=None, method="GET", retries=3, delay=2):
        """Retries the request on failure for a specified number of times with a delay."""
        for attempt in range(retries):
            try:
                log.info(f"Attempt {attempt + 1} for {method} request to {api_url}")
                response = self.custom_headers_request(api_url, payload=payload, method=method)
                if response.status_code == 200:
                    return response
            except requests.exceptions.RequestException as e:
                log.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
        pytest.fail(f"{method} request failed after {retries} retries")

    @allure.step("Validating response schema")
    def validate_json_schema(self, response, schema):
        """Validates the response JSON against a provided schema."""
        try:
            json_data = self.get_json_response(response)
            validate(instance=json_data, schema=schema)
            log.info("JSON schema validation successful")
        except ValidationError as e:
            log.error(f"JSON schema validation failed: {e}")
            pytest.fail(f"JSON schema validation failed: {e}")

    @allure.step("Calculating response size in bytes")
    def get_response_size(self, response):
        """Calculates and logs the size of the response in bytes."""
        size = len(response.content)
        log.info(f"Response size: {size} bytes")
        return size
