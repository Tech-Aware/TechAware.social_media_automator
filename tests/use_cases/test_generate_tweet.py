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
    """
    Fixture providing a mock OpenAI gateway.
    """
    mock = Mock()
    # Configure the generate method instead of generate_tweet
    mock.generate.return_value = "Short generated tweet content"
    return mock


def test_generate_tweet_success(mock_openai_gateway):
    """
    Test successful tweet generation.
    """
    use_case = GenerateTweetUseCase(mock_openai_gateway)

    result = use_case.execute()

    assert result == "Short generated tweet content"
    assert mock_openai_gateway.generate.call_count == 1

    # Verify the prompt argument contains expected elements
    call_args = mock_openai_gateway.generate.call_args[0][0]
    assert "twitter" in call_args.lower()
    assert "hashtags" in call_args.lower()


def test_generate_tweet_openai_error(mock_openai_gateway):
    """
    Test handling of OpenAIError during tweet generation.
    """
    mock_openai_gateway.generate.side_effect = OpenAIError("API error")
    use_case = GenerateTweetUseCase(mock_openai_gateway)

    with pytest.raises(TweetGenerationError) as exc_info:
        use_case.execute()

    assert "Error generating tweet: API error" in str(exc_info.value)


def test_generate_tweet_too_long(mock_openai_gateway):
    """
    Test automatic retry when tweet exceeds character limit.
    """
    # Configure mock to return a long tweet first, then a valid one
    mock_openai_gateway.generate.side_effect = [
        "x" * 281,  # First call returns too long tweet
        "Valid short tweet"  # Second call returns valid tweet
    ]

    use_case = GenerateTweetUseCase(mock_openai_gateway)
    result = use_case.execute()

    assert result == "Valid short tweet"
    assert mock_openai_gateway.generate.call_count == 2  # Should be called twice


def test_generate_tweet_unexpected_error(mock_openai_gateway):
    """
    Test handling of unexpected errors during tweet generation.
    """
    mock_openai_gateway.generate.side_effect = Exception("Unexpected error")
    use_case = GenerateTweetUseCase(mock_openai_gateway)

    with pytest.raises(TweetGenerationError) as exc_info:
        use_case.execute()

    assert "Unexpected error generating tweet: Unexpected error" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
