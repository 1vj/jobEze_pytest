import json
import os
import uuid

import pytest
from utils.service_api.ServiceAPINew import ServiceAPI


@pytest.fixture(scope="module")
def api_setup(api_url, auth_token):
    """Fixture to set up the ServiceAPI client."""
    return ServiceAPI(token=auth_token)


@pytest.fixture(scope="module")
def load_api_config():
    """Fixture to load the API config from JSON once per module."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(project_root, 'config', 'api_config.json')
    with open(config_path) as config_file:
        return json.load(config_file)


@pytest.fixture(scope="module")
def created_user_id(api_setup, base_url, load_api_config):
    """Creates a user via POST and returns the ID for reuse in other tests."""
    payload = dict(load_api_config['api_payload']['user'])  # Clone to prevent mutation
    payload['email'] = f"testuser_{uuid.uuid4().hex[:6]}@example.com"  # Unique email

    create_user_url = f"{base_url}/create-user"
    response = api_setup.post_service_response(create_user_url, payload)
    api_setup.validate_response(response, expected_status=200)

    response_data = response.json()
    user_id = response_data.get("message", {}).get("user_id")
    assert user_id is not None, "User ID not found in POST response"
    return user_id


def test_get_user(api_setup, base_url, created_user_id):
    """Test the GET request for a specific user ID."""
    get_user_url = f"{base_url}/user-info/{created_user_id}"
    response_get = api_setup.get_service_response(get_user_url)
    api_setup.validate_response(response_get, expected_status=200)


def test_post_resource(api_setup, base_url, load_api_config):
    """Test the POST request to create a new user with a unique email."""
    payload = dict(load_api_config['api_payload']['user'])  # Clone to avoid mutation
    payload['email'] = f"testuser_{uuid.uuid4().hex[:6]}@example.com"

    create_user_url = f"{base_url}/create-user"
    response_post = api_setup.post_service_response(create_user_url, payload)
    api_setup.validate_response(response_post, expected_status=200)

    response_data = response_post.json()
    user_id = response_data.get("message", {}).get("user_id")
    assert user_id is not None, "User ID not returned in POST response"


def x_patch_user(api_setup, base_url, created_user_id):
    """Test the PATCH request for a specific user ID."""
    patch_url = f"{base_url}/users/{created_user_id}"
    payload_patch = {"firstName": "UpdatedFirstName"}
    response_patch = api_setup.patch_service_response(patch_url, payload_patch)
    api_setup.validate_response(response_patch, expected_status=200)


def xtest_delete_user(api_setup, base_url, created_user_id):
    """Test the DELETE request for a specific user ID."""
    delete_url = f"{base_url}/users/{created_user_id}"
    response_delete = api_setup.delete_service_response(delete_url)
    api_setup.validate_response(response_delete, expected_status=204)


if __name__ == "__main__":
    pytest.main()
