#location: tests/infrastructure/config/test_environment.py

"""
This module contains unit tests for the environment configuration module.
It tests the loading of environment variables and the retrieval of credentials
for various services (Twitter, OpenAI, LinkedIn).
"""

import os
import sys
import pytest
from unittest.mock import patch

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.config.environment import (
    load_environment_variables,
    get_twitter_credentials,
    get_openai_credentials,
    get_linkedin_credentials
)

@patch('src.infrastructure.config.environment_twitter.dotenv.load_dotenv')
def test_load_environment_variables(mock_load_dotenv):
    load_environment_variables()
    mock_load_dotenv.assert_called_once()

@patch.dict(os.environ, {
    'CONSUMER_KEY': 'fake_consumer_key',
    'CONSUMER_SECRET': 'fake_consumer_secret',
    'ACCESS_TOKEN': 'fake_access_token',
    'ACCESS_TOKEN_SECRET': 'fake_access_token_secret'
}, clear=True)
def test_get_twitter_credentials():
    credentials = get_twitter_credentials()
    assert credentials == {
        'consumer_key': 'fake_consumer_key',
        'consumer_secret': 'fake_consumer_secret',
        'access_token': 'fake_access_token',
        'access_token_secret': 'fake_access_token_secret'
    }

@patch.dict(os.environ, {'OPENAI_API_KEY': 'fake_api_key'}, clear=True)
def test_get_openai_credentials():
    credentials = get_openai_credentials()
    assert credentials == {'api_key': 'fake_api_key'}


@patch.dict(os.environ, {
    'LINKEDIN_CLIENT_ID': 'fake_client_id',
    'LINKEDIN_CLIENT_SECRET': 'fake_client_secret',
    'LINKEDIN_ACCESS_TOKEN': 'fake_access_token',
    'LINKEDIN_USER_ID': 'fake_user_id'
}, clear=True)
def test_get_linkedin_credentials():
    credentials = get_linkedin_credentials()
    assert credentials == {
        'client_id': 'fake_client_id',
        'client_secret': 'fake_client_secret',
        'access_token': 'fake_access_token',
        'user_id': 'fake_user_id'
    }

if __name__ == "__main__":
    pytest.main(["-v", __file__])