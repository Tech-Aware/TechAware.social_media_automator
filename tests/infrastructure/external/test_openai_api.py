# tests/infrastructure/external/test_openai_api.py

"""
Ce module contient les tests unitaires pour la classe OpenAIAPI
définie dans src.infrastructure.external.openai_api.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock


# Ajoute le répertoire racine du projet au sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.external.openai_api import OpenAIAPI
from src.domain.exceptions import ConfigurationError, TweetGenerationError


@patch('src.infrastructure.external.openai_api.get_openai_credentials')
def test_openai_api_initialization(mock_get_credentials):
    mock_get_credentials.return_value = {'api_key': 'fake_api_key'}
    api = OpenAIAPI()
    assert api.client.api_key == 'fake_api_key'


@patch('src.infrastructure.external.openai_api.get_openai_credentials')
def test_openai_api_initialization_error(mock_get_credentials):
    mock_get_credentials.side_effect = ConfigurationError("API key not found")
    with pytest.raises(ConfigurationError):
        OpenAIAPI()


@patch('src.infrastructure.external.openai_api.OpenAI')
def test_generate_tweet(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "\"Generated tweet\""
    mock_client.chat.completions.create.return_value = mock_response

    api = OpenAIAPI()
    result = api.generate("Test prompt")

    assert result == "Generated tweet"
    mock_client.chat.completions.create.assert_called_once()


@patch('src.infrastructure.external.openai_api.OpenAI')
def test_generate_tweet_error(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.side_effect = Exception("API Error")

    api = OpenAIAPI()
    with pytest.raises(TweetGenerationError):
        api.generate("Test prompt")


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
