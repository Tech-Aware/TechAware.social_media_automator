# Location: tests/infrastructure/external/test_facebook_api.py

"""
This module contains unit tests for the FacebookAPI class.
It tests the initialization of the API client and the posting functionality,
including error handling and successful post scenarios.
"""

import sys
import os
import pytest
import requests  # Add this import
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.external.facebook_api import FacebookAPI
from src.domain.entities.facebook_publication import FacebookPublication
from src.domain.exceptions import ConfigurationError, FacebookError


@patch('src.infrastructure.external.facebook_api.get_facebook_credentials')
def test_facebook_api_initialization(mock_get_credentials):
    """
    Test successful initialization of the FacebookAPI class.
    """
    mock_get_credentials.return_value = {
        'app_id': 'fake_app_id',
        'app_secret': 'fake_app_secret',
        'access_token': 'fake_access_token',
        'page_id': 'fake_page_id'
    }
    api = FacebookAPI()
    assert api.credentials == mock_get_credentials.return_value
    assert api.base_url == "https://graph.facebook.com/v19.0"


@patch('src.infrastructure.external.facebook_api.get_facebook_credentials')
def test_facebook_api_initialization_error(mock_get_credentials):
    """
    Test handling of initialization errors in the FacebookAPI class.
    """
    mock_get_credentials.side_effect = ConfigurationError("Credentials not found")
    with pytest.raises(ConfigurationError):
        FacebookAPI()


@patch('src.infrastructure.external.facebook_api.get_facebook_credentials')
@patch('src.infrastructure.external.facebook_api.requests.post')
def test_post_facebook_publication_success(mock_post, mock_get_credentials):
    """
    Test successful posting of a Facebook publication.
    """
    mock_get_credentials.return_value = {
        'app_id': 'fake_app_id',
        'app_secret': 'fake_app_secret',
        'access_token': 'fake_access_token',
        'page_id': 'fake_page_id'
    }

    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "123_456"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    api = FacebookAPI()
    publication = FacebookPublication("Test Facebook post", privacy="PUBLIC")
    result = api.post(publication)

    assert result == {"id": "123_456"}
    mock_post.assert_called_once()

    # Verify API call details
    call_args = mock_post.call_args
    assert call_args is not None
    args, kwargs = call_args

    assert kwargs['headers']['Authorization'] == 'Bearer fake_access_token'
    assert kwargs['json']['message'] == "Test Facebook post"
    assert kwargs['json']['privacy']['value'] == "public"


@patch('src.infrastructure.external.facebook_api.get_facebook_credentials')
@patch('src.infrastructure.external.facebook_api.requests.post')
def test_post_facebook_publication_request_error(mock_post, mock_get_credentials):
    """
    Test handling of request errors when posting to Facebook.
    """
    mock_get_credentials.return_value = {
        'app_id': 'fake_app_id',
        'app_secret': 'fake_app_secret',
        'access_token': 'fake_access_token',
        'page_id': 'fake_page_id'
    }

    mock_post.side_effect = requests.exceptions.RequestException("Network error")

    api = FacebookAPI()
    publication = FacebookPublication("Test Facebook post")

    with pytest.raises(FacebookError) as exc_info:
        api.post(publication)
    assert "Failed to post to Facebook" in str(exc_info.value)


@patch('src.infrastructure.external.facebook_api.get_facebook_credentials')
@patch('src.infrastructure.external.facebook_api.requests.post')
def test_post_facebook_publication_validation_error(mock_post, mock_get_credentials):
    """
    Test that validation errors are caught when posting invalid content.
    """
    mock_get_credentials.return_value = {
        'app_id': 'fake_app_id',
        'app_secret': 'fake_app_secret',
        'access_token': 'fake_access_token',
        'page_id': 'fake_page_id'
    }

    api = FacebookAPI()
    publication = FacebookPublication("Valid content")

    # Simulate validation failure
    with patch.object(publication, 'validate', side_effect=Exception("Validation failed")):
        with pytest.raises(FacebookError) as exc_info:
            api.post(publication)
        assert "Unexpected error posting to Facebook" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", __file__])