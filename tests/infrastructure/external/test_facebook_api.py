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


@patch('src.infrastructure.external.facebook_api.os.getenv')
def test_facebook_api_initialization(mock_getenv):
    """
    Test successful initialization of the FacebookAPI class.
    """
    mock_getenv.return_value = 'fake_access_token'

    api = FacebookAPI()
    assert api.access_token == 'fake_access_token'
    assert api.BASE_URL == "https://graph.facebook.com/v19.0"

    mock_getenv.assert_called_with('FACEBOOK_ACCESS_TOKEN')


@patch('src.infrastructure.external.facebook_api.os.getenv')
def test_facebook_api_initialization_error(mock_getenv):
    """
    Test handling of initialization errors in the FacebookAPI class.
    """
    mock_getenv.return_value = None

    with pytest.raises(FacebookError) as exc_info:
        FacebookAPI()
    assert "Facebook access token not found" in str(exc_info.value)


@patch('src.infrastructure.external.facebook_api.os.getenv')
@patch('requests.post')
@patch('requests.get')
def test_post_facebook_publication_success(mock_get, mock_post, mock_getenv):
    """
    Test successful posting of a Facebook publication.
    """
    # Setup mocks
    mock_getenv.return_value = 'fake_access_token'

    # Mock the page token verification response
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {'access_token': 'page_access_token'}
    mock_get.return_value = mock_get_response

    # Mock the post response
    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.json.return_value = {"id": "123_456"}
    mock_post.return_value = mock_post_response

    # Create API instance and test
    api = FacebookAPI()
    publication = FacebookPublication("Test Facebook post", privacy="PUBLIC")
    result = api.post(publication)

    assert result == {"id": "123_456"}

    # Verify the post call
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args is not None
    args, kwargs = call_args

    # Verify the data being sent
    assert kwargs['data']['message'] == "Test Facebook post"
    assert kwargs['data']['access_token'] == 'page_access_token'


@patch('src.infrastructure.external.facebook_api.os.getenv')
@patch('requests.post')
def test_post_facebook_publication_request_error(mock_post, mock_getenv):
    """
    Test handling of request errors when posting to Facebook.
    """
    mock_getenv.return_value = 'fake_access_token'
    mock_post.side_effect = requests.exceptions.RequestException("Network error")

    api = FacebookAPI()
    publication = FacebookPublication("Test Facebook post")

    with pytest.raises(FacebookError) as exc_info:
        api.post(publication)
    assert "Network error posting to Facebook" in str(exc_info.value)


@patch('src.infrastructure.external.facebook_api.os.getenv')
def test_post_facebook_publication_validation_error(mock_getenv):
    """
    Test that validation errors are caught when posting invalid content.
    """
    mock_getenv.return_value = 'fake_access_token'
    api = FacebookAPI()

    # Test avec une publication invalide
    with pytest.raises(ValidationError) as exc_info:
        FacebookPublication("")  # Cela devrait lever une ValidationError directement
    assert "Facebook publication text cannot be empty" in str(exc_info.value)

    # Test supplémentaire avec une publication valide mais qui devient invalide
    publication = FacebookPublication("Valid text")  # Création valide
    publication.text = ""  # Rend la publication invalide

    with pytest.raises(FacebookError) as exc_info:
        api.post(publication)
    assert "Error posting to Facebook" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", __file__])