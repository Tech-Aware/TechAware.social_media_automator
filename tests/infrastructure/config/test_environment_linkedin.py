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


@patch.dict(os.environ, {
    'LINKEDIN_CLIENT_ID': 'fake_client_id',
    'LINKEDIN_CLIENT_SECRET': 'fake_client_secret',
    'LINKEDIN_ACCESS_TOKEN': 'fake_access_token',
    'LINKEDIN_USER_ID': 'fake_user_id'
}, clear=True)
def test_get_linkedin_credentials():
    """
    Test the retrieval of LinkedIn credentials when all environment variables are set.
    """
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
def test_get_linkedin_credentials_missing_env(missing_var):
    """
    Test the behavior when a required LinkedIn environment variable is missing.
    """
    env_vars = {
        'LINKEDIN_CLIENT_ID': 'fake_client_id',
        'LINKEDIN_CLIENT_SECRET': 'fake_client_secret',
        'LINKEDIN_ACCESS_TOKEN': 'fake_access_token',
        'LINKEDIN_USER_ID': 'fake_user_id'
    }
    del env_vars[missing_var]

    with patch.dict(os.environ, env_vars, clear=True):
        with pytest.raises(ConfigurationError) as exc_info:
            get_linkedin_credentials()

        assert str(exc_info.value) == f"Missing environment variable: {missing_var}"


@patch('src.infrastructure.config.environment_linkedin.load_dotenv')
def test_load_dotenv_called(mock_load_dotenv):
    """
    Test that load_dotenv is called when getting LinkedIn credentials.
    """
    with patch.dict(os.environ, {
        'LINKEDIN_CLIENT_ID': 'fake_client_id',
        'LINKEDIN_CLIENT_SECRET': 'fake_client_secret',
        'LINKEDIN_ACCESS_TOKEN': 'fake_access_token',
        'LINKEDIN_USER_ID': 'fake_user_id'
    }, clear=True):
        get_linkedin_credentials()
        mock_load_dotenv.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v", __file__])