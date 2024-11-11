# Location: tests/infrastructure/config/test_environment_linkedin.py

"""
This module contains unit tests for the LinkedIn environment configuration.
It tests the loading of LinkedIn-specific environment variables and the
retrieval of LinkedIn API credentials.
"""

import os
import sys
import pytest
from unittest.mock import patch

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.config.environment_linkedin import get_linkedin_credentials
from src.domain.exceptions import ConfigurationError


@patch('os.getenv')
def test_get_linkedin_credentials(mock_getenv):
    """
    Test the retrieval of LinkedIn credentials when all environment variables are set.
    """
    mock_getenv.side_effect = lambda x: {
        'LINKEDIN_CLIENT_ID': 'fake_client_id',
        'LINKEDIN_CLIENT_SECRET': 'fake_client_secret',
        'LINKEDIN_ACCESS_TOKEN': 'fake_access_token',
        'LINKEDIN_USER_ID': 'fake_user_id'
    }.get(x)

    credentials = get_linkedin_credentials()
    assert credentials == {
        'client_id': 'fake_client_id',
        'client_secret': 'fake_client_secret',
        'access_token': 'fake_access_token',
        'user_id': 'fake_user_id'
    }


@pytest.mark.parametrize("missing_var", [
    'LINKEDIN_CLIENT_ID',
    'LINKEDIN_CLIENT_SECRET',
    'LINKEDIN_ACCESS_TOKEN',
    'LINKEDIN_USER_ID'
])
@patch('os.getenv')
def test_get_linkedin_credentials_missing_env(mock_getenv, missing_var):
    """
    Test the behavior when a required LinkedIn environment variable is missing.
    """
    def mock_getenv_with_missing(var_name):
        if var_name == missing_var:
            return None
        return {
            'LINKEDIN_CLIENT_ID': 'fake_client_id',
            'LINKEDIN_CLIENT_SECRET': 'fake_client_secret',
            'LINKEDIN_ACCESS_TOKEN': 'fake_access_token',
            'LINKEDIN_USER_ID': 'fake_user_id'
        }.get(var_name)

    mock_getenv.side_effect = mock_getenv_with_missing

    with pytest.raises(ConfigurationError) as exc_info:
        get_linkedin_credentials()
    assert f"Missing environment variable: {missing_var}" in str(exc_info.value)


@patch('src.infrastructure.config.environment_linkedin.load_dotenv')
@patch('os.getenv')
def test_load_dotenv_called(mock_getenv, mock_load_dotenv):
    """
    Test that load_dotenv is called when getting LinkedIn credentials.
    """
    mock_getenv.side_effect = lambda x: {
        'LINKEDIN_CLIENT_ID': 'fake_client_id',
        'LINKEDIN_CLIENT_SECRET': 'fake_client_secret',
        'LINKEDIN_ACCESS_TOKEN': 'fake_access_token',
        'LINKEDIN_USER_ID': 'fake_user_id'
    }.get(x)

    get_linkedin_credentials()
    mock_load_dotenv.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v", __file__])