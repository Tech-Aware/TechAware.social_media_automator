# tests/infrastructure/external/test_openai_api.py

"""
Ce module contient les tests unitaires pour la classe OpenAIAPI
définie dans src.infrastructure.external.openai_api.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.external.openai_api import OpenAIAPI
from src.domain.exceptions import ConfigurationError, OpenAIError


@patch('src.infrastructure.external.openai_api.get_openai_credentials')
def test_openai_api_initialization(mock_get_credentials):
    """Test successful initialization of OpenAI API."""
    mock_get_credentials.return_value = {'api_key': 'fake_api_key'}
    api = OpenAIAPI()
    assert api.client.api_key == 'fake_api_key'


@patch('src.infrastructure.external.openai_api.get_openai_credentials')
def test_openai_api_initialization_error(mock_get_credentials):
    """Test error handling during initialization."""
    mock_get_credentials.side_effect = ConfigurationError("API key not found")
    with pytest.raises(ConfigurationError):
        OpenAIAPI()


@patch('src.infrastructure.external.openai_api.OpenAI')
@patch('os.path.exists')
@patch('os.listdir')
@patch('src.infrastructure.external.openai_api.OpenAIAPI.read_pdf')
@patch('random.choices')
def test_generate_tweet(mock_random_choices, mock_read_pdf, mock_listdir, mock_exists, mock_openai):
    """Test successful generation of content."""
    # Mock filesystem operations
    mock_exists.return_value = True
    mock_listdir.return_value = ['UPPERguideline.pdf', 'pageEntreprise.pdf']
    mock_read_pdf.return_value = "mock content"

    # Mock random choice
    mock_random_choices.return_value = ["https://www.techaware.net/pour-les-entreprises"]

    # Mock OpenAI response
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = """
    <social_media_post>Generated tweet content</social_media_post>
    """
    mock_client.chat.completions.create.return_value = mock_response

    api = OpenAIAPI()
    result = api.generate("Test prompt")

    assert result == "Generated tweet content"
    mock_client.chat.completions.create.assert_called_once()


@patch('src.infrastructure.external.openai_api.OpenAI')
@patch('os.path.exists')
@patch('os.listdir')
@patch('src.infrastructure.external.openai_api.OpenAIAPI.read_pdf')
@patch('random.choices')
def test_generate_tweet_error(mock_random_choices, mock_read_pdf, mock_listdir, mock_exists, mock_openai):
    """Test error handling during content generation."""
    # Mock filesystem operations
    mock_exists.return_value = True
    mock_listdir.return_value = ['UPPERguideline.pdf', 'pageEntreprise.pdf']
    mock_read_pdf.return_value = "mock content"

    # Mock random choice
    mock_random_choices.return_value = ["https://www.techaware.net/pour-les-entreprises"]

    # Mock API error
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.side_effect = Exception("API Error")

    api = OpenAIAPI()
    with pytest.raises(OpenAIError) as exc_info:
        api.generate("Test prompt")
    assert "API Error" in str(exc_info.value)


@patch('src.infrastructure.external.openai_api.OpenAI')
@patch('os.path.exists')
@patch('os.listdir')
@patch('src.infrastructure.external.openai_api.OpenAIAPI.read_pdf')
@patch('random.choices')
def test_generate_invalid_response_format(mock_random_choices, mock_read_pdf, mock_listdir, mock_exists, mock_openai):
    """Test handling of invalid response format."""
    # Mock filesystem operations
    mock_exists.return_value = True
    mock_listdir.return_value = ['UPPERguideline.pdf', 'pageEntreprise.pdf']
    mock_read_pdf.return_value = "mock content"

    # Mock random choice
    mock_random_choices.return_value = ["https://www.techaware.net/pour-les-entreprises"]

    # Mock response without social_media_post tags
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Invalid response format"
    mock_client.chat.completions.create.return_value = mock_response

    api = OpenAIAPI()
    with pytest.raises(OpenAIError) as exc_info:
        api.generate("Test prompt")
    assert "Le contenu généré ne contient pas les balises" in str(exc_info.value)


@patch('src.infrastructure.external.openai_api.OpenAI')
@patch('os.path.exists')
@patch('os.listdir')
@patch('src.infrastructure.external.openai_api.OpenAIAPI.read_pdf')
@patch('random.choices')
def test_generate_empty_response(mock_random_choices, mock_read_pdf, mock_listdir, mock_exists, mock_openai):
    """Test handling of empty response."""
    # Mock filesystem operations
    mock_exists.return_value = True
    mock_listdir.return_value = ['UPPERguideline.pdf', 'pageEntreprise.pdf']
    mock_read_pdf.return_value = "mock content"

    # Mock random choice
    mock_random_choices.return_value = ["https://www.techaware.net/pour-les-entreprises"]

    # Mock empty response
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = ""
    mock_client.chat.completions.create.return_value = mock_response

    api = OpenAIAPI()
    with pytest.raises(OpenAIError) as exc_info:
        api.generate("Test prompt")
    assert "Le contenu généré est vide" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", __file__])