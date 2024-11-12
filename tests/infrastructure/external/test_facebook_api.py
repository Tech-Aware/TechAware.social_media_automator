# Location: tests/infrastructure/external/test_facebook_api.py

"""
This module contains unit tests for the FacebookAPI class.
It tests the initialization of the API client and the posting functionality,
including error handling and successful post scenarios.
"""

import sys
import os
import pytest
import requests
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.external.facebook_api import FacebookAPI
from src.domain.entities.facebook_publication import FacebookPublication
from src.domain.exceptions import ConfigurationError, FacebookError, ValidationError


@patch('src.infrastructure.external.facebook_api.get_facebook_credentials')
def test_facebook_api_initialization(mock_get_credentials):
    """
    Test successful initialization of the FacebookAPI class.
    """
    # Setup mock credentials
    mock_credentials = {
        'app_id': 'fake_app_id',
        'app_secret': 'fake_app_secret',
        'access_token': 'fake_access_token',
        'page_id': 'fake_page_id'
    }
    mock_get_credentials.return_value = mock_credentials

    # Create API instance and test
    api = FacebookAPI()
    assert api.access_token == 'fake_access_token'
    assert api.page_id == 'fake_page_id'
    assert api.BASE_URL == "https://graph.facebook.com/v19.0"



@patch('src.infrastructure.external.facebook_api.get_facebook_credentials')
def test_facebook_api_initialization_error(mock_get_credentials):
    """
    Test handling of initialization errors in the FacebookAPI class.
    """
    mock_get_credentials.side_effect = FacebookError("Missing environment variable: FACEBOOK_APP_ID")

    with pytest.raises(FacebookError) as exc_info:
        FacebookAPI()
    assert "Missing environment variable: FACEBOOK_APP_ID" in str(exc_info.value)


@patch('src.infrastructure.external.facebook_api.os.getenv')
def test_post_facebook_publication_success(mock_getenv):
    """
    Test successful posting of a Facebook publication.
    """
    # Setup mocks
    mock_getenv.return_value = 'fake_access_token'

    # Mock the page token verification response
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {'access_token': 'page_access_token'}
    mock_get = MagicMock(return_value=mock_get_response)

    # Mock the post response
    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.json.return_value = {"id": "123_456"}
    mock_post = MagicMock(return_value=mock_post_response)

    with patch('requests.get', mock_get), \
            patch('requests.post', mock_post), \
            patch('src.infrastructure.external.facebook_api.get_facebook_credentials',
                  return_value={'access_token': 'fake_access_token', 'page_id': 'fake_page_id'}):
        # Create API instance and test
        api = FacebookAPI()
        publication = FacebookPublication("Test Facebook post", privacy="PUBLIC")
        result = api.post(publication)

        assert result == {"id": "123_456"}


@patch('src.infrastructure.external.facebook_api.get_facebook_credentials')
@patch('requests.post')
def test_post_facebook_publication_request_error(mock_post, mock_get_credentials):
    """
    Test handling of request errors when posting to Facebook.
    """
    mock_get_credentials.return_value = {
        'access_token': 'fake_access_token',
        'page_id': 'fake_page_id'
    }
    mock_post.side_effect = Exception("Network error")

    api = FacebookAPI()
    publication = FacebookPublication("Test Facebook post")

    with pytest.raises(FacebookError) as exc_info:
        api.post(publication)
    assert "Error posting to Facebook" in str(exc_info.value)



def test_post_facebook_publication_validation_error():
    """
    Test that validation errors are caught when posting invalid content.
    """
    with pytest.raises(ValidationError) as exc_info:
        FacebookPublication("")
    assert "Facebook publication text cannot be empty" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
