# tests/use_cases/test_generate_tweet.py

"""
This module contains unit tests for the GenerateTweetUseCase class.
It tests the execution of the use case with various scenarios including
successful tweet generation and error handling.
"""

import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from unittest.mock import Mock
from src.use_cases.generate_tweet import GenerateTweetUseCase
from src.domain.exceptions import OpenAIError, TweetGenerationError


@pytest.fixture
def mock_openai_gateway():
    return Mock()


def test_generate_tweet_success(mock_openai_gateway):
    """
    Test successful tweet generation.
    """
    mock_openai_gateway.generate_tweet.return_value = "Generated tweet"
    use_case = GenerateTweetUseCase(mock_openai_gateway)

    result = use_case.execute("Test prompt")

    assert result == "Generated tweet"
    mock_openai_gateway.generate_tweet.assert_called_once_with("Test prompt")


def test_generate_tweet_openai_error(mock_openai_gateway):
    """
    Test handling of OpenAIError during tweet generation.
    """
    mock_openai_gateway.generate_tweet.side_effect = OpenAIError("API error")
    use_case = GenerateTweetUseCase(mock_openai_gateway)

    with pytest.raises(TweetGenerationError) as exc_info:
        use_case.execute("Test prompt")

    assert str(exc_info.value) == "Erreur lors de la génération du tweet : API error"


def test_generate_tweet_unexpected_error(mock_openai_gateway):
    """
    Test handling of unexpected errors during tweet generation.
    """
    mock_openai_gateway.generate_tweet.side_effect = Exception("Unexpected error")
    use_case = GenerateTweetUseCase(mock_openai_gateway)

    with pytest.raises(TweetGenerationError) as exc_info:
        use_case.execute("Test prompt")

    assert str(exc_info.value) == "Erreur inattendue lors de la génération du tweet : Unexpected error"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
