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
    with pytest.raises(TypeError) as exc_info:
        OpenAIGateway()
    assert "Can't instantiate abstract class" in str(exc_info.value)


def test_openai_gateway_generate_method():
    """
    Test that OpenAIGateway has a generate method and that it can be implemented
    in a concrete subclass.
    """
    assert hasattr(OpenAIGateway, 'generate')

    class ConcreteOpenAIGateway(OpenAIGateway):
        def generate(self, prompt: str) -> str:
            """Example implementation of generate method"""
            return "Generated content"

    gateway = ConcreteOpenAIGateway()
    assert callable(gateway.generate)
    assert isinstance(gateway.generate("test prompt"), str)
    assert gateway.generate("test prompt") == "Generated content"


def test_openai_gateway_generate_raises_error():
    """
    Test that a concrete implementation of OpenAIGateway can raise an OpenAIError
    when generate encounters an error.
    """

    class ErrorOpenAIGateway(OpenAIGateway):
        def generate(self, prompt: str) -> str:
            """Example implementation that raises an error"""
            raise OpenAIError("Test error")

    gateway = ErrorOpenAIGateway()
    with pytest.raises(OpenAIError) as exc_info:
        gateway.generate("test prompt")
    assert "Test error" in str(exc_info.value)


def test_openai_gateway_generate_input_validation():
    """
    Test that generate method properly handles input validation.
    """

    class ValidatingOpenAIGateway(OpenAIGateway):
        def generate(self, prompt: str) -> str:
            """Example implementation with input validation"""
            if not isinstance(prompt, str):
                raise ValueError("Prompt must be a string")
            if not prompt.strip():
                raise ValueError("Prompt cannot be empty")
            return "Valid content"

    gateway = ValidatingOpenAIGateway()

    # Test with invalid input types
    with pytest.raises(ValueError) as exc_info:
        gateway.generate(123)  # type: ignore
    assert "Prompt must be a string" in str(exc_info.value)

    # Test with empty prompt
    with pytest.raises(ValueError) as exc_info:
        gateway.generate("   ")
    assert "Prompt cannot be empty" in str(exc_info.value)

    # Test with valid prompt
    assert gateway.generate("valid prompt") == "Valid content"


if __name__ == "__main__":
    pytest.main(["-v", __file__])