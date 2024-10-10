# tests/interfaces/test_twitter_gateway.py

"""
This module contains unit tests for the TwitterGateway interface.
It verifies that the interface is correctly defined and that concrete implementations
can be created and used as expected.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from src.interfaces.twitter_gateway import TwitterGateway
from src.domain.entities.tweet import Tweet
from src.domain.exceptions import TwitterError


def test_twitter_gateway_is_abstract():
    """
    Test that TwitterGateway cannot be instantiated directly as it is an abstract base class.
    """
    with pytest.raises(TypeError):
        TwitterGateway()


def test_twitter_gateway_post_tweet_method():
    """
    Test that TwitterGateway has a post_tweet method and that it can be implemented
    in a concrete subclass.
    """
    assert hasattr(TwitterGateway, 'post_tweet')

    class ConcreteTwitterGateway(TwitterGateway):
        def post_tweet(self, tweet: Tweet):
            return {"id": "123456", "text": tweet.get_text()}

    gateway = ConcreteTwitterGateway()
    assert callable(gateway.post_tweet)
    tweet = Tweet("Test tweet")
    result = gateway.post_tweet(tweet)
    assert isinstance(result, dict)
    assert "id" in result
    assert "text" in result


def test_twitter_gateway_post_tweet_raises_error():
    """
    Test that a concrete implementation of TwitterGateway can raise a TwitterError
    when post_tweet encounters an error.
    """

    class ErrorTwitterGateway(TwitterGateway):
        def post_tweet(self, tweet: Tweet):
            raise TwitterError("Test error")

    gateway = ErrorTwitterGateway()
    tweet = Tweet("Test tweet")
    with pytest.raises(TwitterError):
        gateway.post_tweet(tweet)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
    