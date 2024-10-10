# tests/infrastructure/config/test_environment.py

"""
Ce module contient les tests unitaires pour les fonctions de gestion
des variables d'environnement définies dans src.infrastructure.config.environment.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock


# Ajoute le répertoire racine du projet au sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.config.environment import load_environment_variables, get_twitter_credentials, get_openai_credentials


@patch('src.infrastructure.config.environment.load_environment_variables')
def test_load_environment_variables(mock_load_env):
    from src.infrastructure.config.environment import load_environment_variables
    load_environment_variables()
    mock_load_env.assert_called_once()


@patch('src.infrastructure.config.environment.get_twitter_credentials')
def test_get_twitter_credentials(mock_get_twitter):
    expected_credentials = {
        'consumer_key': 'fake_consumer_key',
        'consumer_secret': 'fake_consumer_secret',
        'access_token': 'fake_access_token',
        'access_token_secret': 'fake_access_token_secret'
    }
    mock_get_twitter.return_value = expected_credentials
    from src.infrastructure.config.environment import get_twitter_credentials
    credentials = get_twitter_credentials()
    assert credentials == expected_credentials


@patch('src.infrastructure.config.environment.get_openai_credentials')
def test_get_openai_credentials(mock_get_openai):
    expected_credentials = {
        'api_key': 'fake_api_key'
    }
    mock_get_openai.return_value = expected_credentials
    from src.infrastructure.config.environment import get_openai_credentials
    credentials = get_openai_credentials()
    assert credentials == expected_credentials


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
