# Location: tests/infrastructure/external/test_linkedin_api.py

"""
This module contains unit tests for the LinkedInAPI class.
It tests the initialization of the API client and the posting functionality,
including error handling and successful post scenarios.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.external.linkedin_api import LinkedInAPI
from src.domain.entities.linkedin_publication import LinkedInPublication
from src.domain.exceptions import ConfigurationError, LinkedInError


@patch('src.infrastructure.external.linkedin_api.get_linkedin_credentials')
def test_linkedin_api_initialization(mock_get_credentials):
    """
    Test the initialization of the LinkedInAPI class.
    """
    mock_get_credentials.return_value = {
        'client_id': 'fake_client_id',
        'client_secret': 'fake_client_secret',
        'access_token': 'fake_access_token',
        'user_id': 'fake_user_id'
    }
    api = LinkedInAPI()
    assert api.credentials == mock_get_credentials.return_value


@patch('src.infrastructure.external.linkedin_api.get_linkedin_credentials')
def test_linkedin_api_initialization_error(mock_get_credentials):
    """
    Test the handling of initialization errors in the LinkedInAPI class.
    """
    mock_get_credentials.side_effect = ConfigurationError("Credentials not found")
    with pytest.raises(ConfigurationError):
        LinkedInAPI()


@patch('src.infrastructure.external.linkedin_api.get_linkedin_credentials')
@patch('src.infrastructure.external.linkedin_api.requests.post')
def test_post_linkedin_publication(mock_post, mock_get_credentials):
    """
    Test the successful posting of a LinkedIn publication.
    """
    # Configure mock credentials
    mock_get_credentials.return_value = {
        'client_id': 'fake_client_id',
        'client_secret': 'fake_client_secret',
        'access_token': 'fake_access_token',
        'user_id': 'fake_user_id'
    }

    # Configure mock response
    mock_response = MagicMock()
    mock_response.status_code = 201  # Important: Set correct status code
    mock_response.json.return_value = {"id": "fake_post_id"}
    mock_post.return_value = mock_response

    # Create API instance and test publication
    api = LinkedInAPI()
    publication = LinkedInPublication("Test LinkedIn post")
    result = api.post(publication)

    # Verify results
    assert result == {"id": "fake_post_id"}

    # Verify API call
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args

    # Verify endpoint
    assert args[0] == 'https://api.linkedin.com/v2/ugcPosts'

    # Verify headers
    assert kwargs['headers']['Authorization'] == 'Bearer fake_access_token'
    assert kwargs['headers']['Content-Type'] == 'application/json'
    assert kwargs['headers']['X-Restli-Protocol-Version'] == '2.0.0'

    # Verify payload
    expected_payload = {
        'author': 'urn:li:organization:fake_user_id',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': 'Test LinkedIn post'
                },
                'shareMediaCategory': 'NONE'
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
        }
    }
    assert kwargs['json'] == expected_payload


@patch('src.infrastructure.external.linkedin_api.get_linkedin_credentials')
@patch('src.infrastructure.external.linkedin_api.requests.post')
def test_post_linkedin_publication_error(mock_post, mock_get_credentials):
    """
    Test the handling of errors when posting a LinkedIn publication.
    """
    mock_get_credentials.return_value = {
        'client_id': 'fake_client_id',
        'client_secret': 'fake_client_secret',
        'access_token': 'fake_access_token',
        'user_id': 'fake_user_id'
    }

    # Configure mock to simulate API error
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_post.return_value = mock_response

    api = LinkedInAPI()
    publication = LinkedInPublication("Test LinkedIn post")

    with pytest.raises(LinkedInError) as exc_info:
        api.post(publication)
    assert "LinkedIn API error: 400 - Bad Request" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", __file__])