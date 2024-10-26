# Location: tests/use_cases/test_generate_facebook_publication.py

"""
This module contains unit tests for the GenerateFacebookPublicationUseCase class.
It tests the execution of the use case with various scenarios including
successful publication generation and error handling.
"""

import sys
import os
import pytest
from unittest.mock import Mock

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.use_cases.generate_facebook_publication import GenerateFacebookPublicationUseCase
from src.domain.exceptions import OpenAIError, TweetGenerationError


@pytest.fixture
def mock_openai_gateway():
    """
    Fixture providing a mock OpenAI gateway.
    """
    return Mock()


def test_generate_facebook_publication_success(mock_openai_gateway):
    """
    Test successful Facebook publication generation.
    """
    mock_openai_gateway.generate_tweet.return_value = "Generated Facebook publication content"
    use_case = GenerateFacebookPublicationUseCase(mock_openai_gateway)

    result = use_case.execute("Test prompt")

    assert result == "Generated Facebook publication content"
    mock_openai_gateway.generate_tweet.assert_called_once()

    # Verify that the prompt was enhanced with Facebook-specific context
    call_args = mock_openai_gateway.generate_tweet.call_args[0][0]
    assert "Facebook publication" in call_args
    assert "general audience" in call_args
    assert "emojis" in call_args
    assert "Test prompt" in call_args


def test_generate_facebook_publication_openai_error(mock_openai_gateway):
    """
    Test handling of OpenAIError during Facebook publication generation.
    """
    mock_openai_gateway.generate_tweet.side_effect = OpenAIError("API error")
    use_case = GenerateFacebookPublicationUseCase(mock_openai_gateway)

    with pytest.raises(TweetGenerationError) as exc_info:
        use_case.execute("Test prompt")

    assert "Error generating Facebook publication" in str(exc_info.value)
    assert "API error" in str(exc_info.value)


def test_generate_facebook_publication_unexpected_error(mock_openai_gateway):
    """
    Test handling of unexpected errors during Facebook publication generation.
    """
    mock_openai_gateway.generate_tweet.side_effect = Exception("Unexpected error")
    use_case = GenerateFacebookPublicationUseCase(mock_openai_gateway)

    with pytest.raises(TweetGenerationError) as exc_info:
        use_case.execute("Test prompt")

    assert "Unexpected error generating Facebook publication" in str(exc_info.value)


def test_generate_facebook_publication_with_empty_prompt(mock_openai_gateway):
    """
    Test generation with an empty prompt.
    """
    mock_openai_gateway.generate_tweet.return_value = "Generated content for empty prompt"
    use_case = GenerateFacebookPublicationUseCase(mock_openai_gateway)

    result = use_case.execute("")

    assert result == "Generated content for empty prompt"
    mock_openai_gateway.generate_tweet.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v", __file__])