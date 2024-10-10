# tests/infrastructure/config/test_environment_openai.py

"""
Ce module contient les tests unitaires pour les fonctions de gestion
des variables d'environnement OpenAI définies dans src.infrastructure.config.environment_openai.
"""

import sys
import os
import pytest
from unittest.mock import patch


# Ajoute le répertoire racine du projet au sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.config.environment_openai import get_openai_credentials
from src.domain.exceptions import ConfigurationError


@patch('os.getenv')
def test_get_openai_credentials(mock_getenv):
    mock_getenv.return_value = 'fake_api_key'

    credentials = get_openai_credentials()

    assert credentials == {'api_key': 'fake_api_key'}


@patch('os.getenv')
def test_get_openai_credentials_missing_env(mock_getenv):
    mock_getenv.return_value = None

    with pytest.raises(ConfigurationError):
        get_openai_credentials()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
