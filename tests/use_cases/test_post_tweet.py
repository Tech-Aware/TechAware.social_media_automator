# tests/use_cases/test_post_tweet.py

"""
This module contains unit tests for the PostTweetUseCase class.
It tests the execution of the use case with various scenarios including
successful tweet posting and error handling.
"""

import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from unittest.mock import Mock
from src.use_cases.post_tweet import PostTweetUseCase
from src.domain.entities.tweet import Tweet
from src.domain.exceptions import TwitterError, ValidationError


@pytest.fixture
def mock_twitter_gateway():
    return Mock()


def test_post_tweet_success(mock_twitter_gateway):
    """
    Test successful tweet posting.
    """
    mock_twitter_gateway.post_tweet.return_value = {"data": {"id": "123456"}}
    use_case = PostTweetUseCase(mock_twitter_gateway)

    result = use_case.execute("Test tweet")

    assert result == {"data": {"id": "123456"}}
    mock_twitter_gateway.post_tweet.assert_called_once()
    assert isinstance(mock_twitter_gateway.post_tweet.call_args[0][0], Tweet)
    assert mock_twitter_gateway.post_tweet.call_args[0][0].get_text() == "Test tweet"


def test_post_tweet_validation_error():
    """
    Test handling of ValidationError during tweet creation.
    """
    use_case = PostTweetUseCase(Mock())

    with pytest.raises(ValidationError) as exc_info:
        use_case.execute("     " * 50)  # Tweet too long

        assert "Tweet must be 280 characters or less" in str(exc_info.value)


def test_post_tweet_twitter_error(mock_twitter_gateway):
    """
    Test handling of TwitterError during tweet posting.
    """
    mock_twitter_gateway.post_tweet.side_effect = TwitterError("API error")
    use_case = PostTweetUseCase(mock_twitter_gateway)

    with pytest.raises(TwitterError) as exc_info:
        use_case.execute("Test tweet")

    assert str(exc_info.value) == "API error"
    mock_twitter_gateway.post_tweet.assert_called_once()


def test_post_tweet_unexpected_error(mock_twitter_gateway):
    """
    Test handling of unexpected errors during tweet posting.
    """
    mock_twitter_gateway.post_tweet.side_effect = Exception("Unexpected error")
    use_case = PostTweetUseCase(mock_twitter_gateway)

    with pytest.raises(Exception) as exc_info:
        use_case.execute("Test tweet")

    assert str(exc_info.value) == "Unexpected error"
    mock_twitter_gateway.post_tweet.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])