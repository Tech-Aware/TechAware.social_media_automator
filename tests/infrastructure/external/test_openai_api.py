# tests/infrastructure/external/test_openai_api.py

"""
This module contains unit tests for the OpenAIAPI class.
It tests the initialization of the API client and content generation
functionality, including error handling and response validation.
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
def test_generate_success(mock_openai):
    """Test successful content generation."""
    # Configure mock response
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = """
    <social_media_post>Generated content</social_media_post>
    """
    mock_client.chat.completions.create.return_value = mock_response

    api = OpenAIAPI()
    result = api.generate("Test prompt")

    assert result == "Generated content"
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Test prompt"}
        ]
    )


@patch('src.infrastructure.external.openai_api.OpenAI')
def test_generate_api_error(mock_openai):
    """Test handling of API errors during generation."""
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.side_effect = Exception("API Error")

    api = OpenAIAPI()
    with pytest.raises(OpenAIError) as exc_info:
        api.generate("Test prompt")
    assert "Content generation failed: API Error" in str(exc_info.value)


@patch('src.infrastructure.external.openai_api.OpenAI')
def test_generate_invalid_response_format(mock_openai):
    """Test handling of invalid response format."""
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Invalid response format"
    mock_client.chat.completions.create.return_value = mock_response

    api = OpenAIAPI()
    with pytest.raises(OpenAIError) as exc_info:
        api.generate("Test prompt")
    assert "Generated content does not contain social_media_post tags" in str(exc_info.value)


@patch('src.infrastructure.external.openai_api.OpenAI')
def test_generate_empty_response(mock_openai):
    """Test handling of empty response."""
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = ""
    mock_client.chat.completions.create.return_value = mock_response

    api = OpenAIAPI()
    with pytest.raises(OpenAIError) as exc_info:
        api.generate("Test prompt")
    assert "Generated content is empty" in str(exc_info.value)


@patch('src.infrastructure.external.openai_api.OpenAI')
def test_response_cleanup(mock_openai):
    """Test cleanup of generated content."""
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = """
    <social_media_post>**Bold Text**. </social_media_post>
    """
    mock_client.chat.completions.create.return_value = mock_response

    api = OpenAIAPI()
    result = api.generate("Test prompt")

    assert result == "Bold Text"
    assert "**" not in result
    assert not result.endswith(".")


if __name__ == "__main__":
    pytest.main(["-v", __file__])