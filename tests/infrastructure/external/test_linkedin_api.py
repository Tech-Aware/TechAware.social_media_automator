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
    mock_get_credentials.return_value = {
        'client_id': 'fake_client_id',
        'client_secret': 'fake_client_secret',
        'access_token': 'fake_access_token',
        'user_id': 'fake_user_id'
    }
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "fake_post_id"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    api = LinkedInAPI()
    publication = LinkedInPublication("Test LinkedIn post")
    result = api.post(publication)

    assert result == {"id": "fake_post_id"}
    mock_post.assert_called_once()
    _, kwargs = mock_post.call_args
    assert kwargs['headers']['Authorization'] == 'Bearer fake_access_token'
    assert 'Test LinkedIn post' in str(kwargs['json'])


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
    mock_post.side_effect = Exception("API Error")

    api = LinkedInAPI()
    publication = LinkedInPublication("Test LinkedIn post")
    with pytest.raises(LinkedInError):
        api.post(publication)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
