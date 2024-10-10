# tests/infrastructure/config/test_environment_twitter.py

"""
Ce module contient les tests unitaires pour les fonctions de gestion
des variables d'environnement Twitter définies dans src.infrastructure.config.environment_twitter.
"""

import sys
import os
import pytest
from unittest.mock import patch


# Ajoute le répertoire racine du projet au sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.config.environment_twitter import load_environment_variables, get_twitter_credentials
from src.domain.exceptions import ConfigurationError


@patch('src.infrastructure.config.environment_twitter.dotenv.load_dotenv')
def test_load_environment_variables(mock_load_dotenv):
    load_environment_variables()
    mock_load_dotenv.assert_called_once()


@patch('os.getenv')
def test_get_twitter_credentials(mock_getenv):
    mock_getenv.side_effect = lambda key: {
        'CONSUMER_KEY': 'fake_consumer_key',
        'CONSUMER_SECRET': 'fake_consumer_secret',
        'ACCESS_TOKEN': 'fake_access_token',
        'ACCESS_TOKEN_SECRET': 'fake_access_token_secret'
    }.get(key)

    credentials = get_twitter_credentials()

    assert credentials == {
        'consumer_key': 'fake_consumer_key',
        'consumer_secret': 'fake_consumer_secret',
        'access_token': 'fake_access_token',
        'access_token_secret': 'fake_access_token_secret'
    }


@patch('os.getenv')
def test_get_twitter_credentials_missing_env(mock_getenv):
    mock_getenv.return_value = None

    with pytest.raises(ConfigurationError):
        get_twitter_credentials()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])