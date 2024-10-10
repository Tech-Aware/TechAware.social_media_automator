# tests/interfaces/test_openai_gateway.py

"""
This module contains unit tests for the OpenAIGateway interface.
It verifies that the interface is correctly defined and that concrete implementations
can be created and used as expected.
"""


import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from src.interfaces.openai_gateway import OpenAIGateway
from src.domain.exceptions import OpenAIError


def test_openai_gateway_is_abstract():
    """
    Test that OpenAIGateway cannot be instantiated directly as it is an abstract base class.
    """
    with pytest.raises(TypeError):
        OpenAIGateway()


def test_openai_gateway_generate_tweet_method():
    """
    Test that OpenAIGateway has a generate_tweet method and that it can be implemented
    in a concrete subclass.
    """
    assert hasattr(OpenAIGateway, 'generate_tweet')

    class ConcreteOpenAIGateway(OpenAIGateway):
        def generate_tweet(self, prompt: str) -> str:
            return "Test tweet"

    gateway = ConcreteOpenAIGateway()
    assert callable(gateway.generate_tweet)
    assert isinstance(gateway.generate_tweet("test prompt"), str)


def test_openai_gateway_generate_tweet_raises_error():
    """
    Test that a concrete implementation of OpenAIGateway can raise an OpenAIError
    when generate_tweet encounters an error.
    """

    class ErrorOpenAIGateway(OpenAIGateway):
        def generate_tweet(self, prompt: str) -> str:
            raise OpenAIError("Test error")

    gateway = ErrorOpenAIGateway()
    with pytest.raises(OpenAIError):
        gateway.generate_tweet("test prompt")


if __name__ == "__main__":
    pytest.main(["-v", __file__])