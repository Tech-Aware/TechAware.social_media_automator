# Location: tests/infrastructure/config/test_environment_facebook.py

"""
This module contains unit tests for the Facebook environment configuration.
It tests the loading of Facebook-specific environment variables and the
retrieval of Facebook API credentials.
"""

import os
import sys
import pytest
from unittest.mock import patch

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.config.environment_facebook import get_facebook_credentials
from src.domain.exceptions import ConfigurationError


@patch.dict(os.environ, {
    'FACEBOOK_APP_ID': 'fake_app_id',
    'FACEBOOK_APP_SECRET': 'fake_app_secret',
    'FACEBOOK_ACCESS_TOKEN': 'fake_access_token',
    'FACEBOOK_PAGE_ID': 'fake_page_id'
}, clear=True)
def test_get_facebook_credentials_success():
    """
    Test successful retrieval of Facebook credentials when all environment variables are set.
    """
    credentials = get_facebook_credentials()
    assert credentials == {
        'app_id': 'fake_app_id',
        'app_secret': 'fake_app_secret',
        'access_token': 'fake_access_token',
        'page_id': 'fake_page_id'
    }


@pytest.mark.parametrize("missing_var", [
    'FACEBOOK_APP_ID',
    'FACEBOOK_APP_SECRET',
    'FACEBOOK_ACCESS_TOKEN',
    'FACEBOOK_PAGE_ID'
])
def test_get_facebook_credentials_missing_env(missing_var):
    """
    Test the behavior when a required Facebook environment variable is missing.

    Args:
        missing_var: The environment variable to omit
    """
    env_vars = {
        'FACEBOOK_APP_ID': 'fake_app_id',
        'FACEBOOK_APP_SECRET': 'fake_app_secret',
        'FACEBOOK_ACCESS_TOKEN': 'fake_access_token',
        'FACEBOOK_PAGE_ID': 'fake_page_id'
    }
    del env_vars[missing_var]

    with patch.dict(os.environ, env_vars, clear=True):
        with pytest.raises(ConfigurationError) as exc_info:
            get_facebook_credentials()
        assert str(exc_info.value) == f"Missing environment variable: {missing_var}"


if __name__ == "__main__":
    pytest.main(["-v", __file__])