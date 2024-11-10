# Location: tests/infrastructure/config/test_environment_facebook.py

"""
This module contains unit tests for the Facebook environment configuration.
It tests the loading of Facebook-specific environment variables and the
retrieval of Facebook API credentials with enhanced error handling and validation.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.config.environment_facebook import get_facebook_credentials
from src.domain.exceptions import ConfigurationError


@pytest.fixture
def mock_env_vars():
    """
    Fixture providing mock environment variables for testing.

    Returns:
        dict: Mock environment variables
    """
    return {
        'FACEBOOK_APP_ID': 'fake_app_id',
        'FACEBOOK_APP_SECRET': 'fake_app_secret',
        'FACEBOOK_ACCESS_TOKEN': 'fake_access_token',
        'FACEBOOK_PAGE_ID': 'fake_page_id'
    }


@patch('src.infrastructure.config.environment_facebook.load_dotenv')
def test_get_facebook_credentials_success(mock_load_dotenv, mock_env_vars):
    """
    Test successful retrieval of Facebook credentials when all environment variables are set.

    Args:
        mock_load_dotenv: Mock for dotenv.load_dotenv
        mock_env_vars: Fixture providing mock environment variables
    """
    mock_load_dotenv.return_value = True

    with patch.dict(os.environ, mock_env_vars, clear=True):
        credentials = get_facebook_credentials()

        assert credentials == {
            'app_id': 'fake_app_id',
            'app_secret': 'fake_app_secret',
            'access_token': 'fake_access_token',
            'page_id': 'fake_page_id'
        }

        mock_load_dotenv.assert_called_once()


@pytest.mark.parametrize("missing_var", [
    'FACEBOOK_APP_ID',
    'FACEBOOK_APP_SECRET',
    'FACEBOOK_ACCESS_TOKEN',
    'FACEBOOK_PAGE_ID'
])
@patch('src.infrastructure.config.environment_facebook.load_dotenv')
def test_get_facebook_credentials_missing_env(mock_load_dotenv, mock_env_vars, missing_var):
    """
    Test the behavior when a required Facebook environment variable is missing.

    Args:
        mock_load_dotenv: Mock for dotenv.load_dotenv
        mock_env_vars: Fixture providing mock environment variables
        missing_var: The environment variable to omit
    """
    mock_load_dotenv.return_value = True
    env_vars = mock_env_vars.copy()
    del env_vars[missing_var]

    with patch.dict(os.environ, env_vars, clear=True):
        with pytest.raises(ConfigurationError) as exc_info:
            get_facebook_credentials()
        assert str(exc_info.value) == f"Missing environment variable: {missing_var}"

        mock_load_dotenv.assert_called_once()


@patch('src.infrastructure.config.environment_facebook.load_dotenv')
def test_get_facebook_credentials_dotenv_failure(mock_load_dotenv, mock_env_vars):
    """
    Test handling of dotenv loading failure.

    Args:
        mock_load_dotenv: Mock for dotenv.load_dotenv
        mock_env_vars: Fixture providing mock environment variables
    """
    mock_load_dotenv.return_value = False

    with patch.dict(os.environ, mock_env_vars, clear=True):
        credentials = get_facebook_credentials()

        assert credentials == {
            'app_id': 'fake_app_id',
            'app_secret': 'fake_app_secret',
            'access_token': 'fake_access_token',
            'page_id': 'fake_page_id'
        }

        mock_load_dotenv.assert_called_once()


@patch('src.infrastructure.config.environment_facebook.load_dotenv')
def test_get_facebook_credentials_empty_values(mock_load_dotenv, mock_env_vars):
    """
    Test handling of empty environment variable values.

    Args:
        mock_load_dotenv: Mock for dotenv.load_dotenv
        mock_env_vars: Fixture providing mock environment variables
    """
    mock_load_dotenv.return_value = True
    env_vars = {k: '' for k in mock_env_vars.keys()}

    with patch.dict(os.environ, env_vars, clear=True):
        with pytest.raises(ConfigurationError) as exc_info:
            get_facebook_credentials()
        assert "Missing environment variable: FACEBOOK_APP_ID" in str(exc_info.value)

        mock_load_dotenv.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v", __file__])