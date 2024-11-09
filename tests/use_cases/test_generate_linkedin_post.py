# tests/use_cases/test_generate_linkedin_post.py

"""
This module contains unit tests for the GenerateLinkedInPostUseCase class.
It tests the execution of the use case with various scenarios including
successful post generation and error handling.
"""

import sys
import os
import pytest
from unittest.mock import Mock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.use_cases.generate_linkedin_post import GenerateLinkedInPostUseCase
from src.domain.exceptions import OpenAIError, LinkedInGenerationError


@pytest.fixture
def mock_openai_gateway():
    """
    Fixture providing a mock OpenAI gateway.
    """
    return Mock()


def test_generate_linkedin_post_success(mock_openai_gateway):
    """
    Test successful LinkedIn post generation.
    """
    # Configure the mock
    mock_openai_gateway.generate.return_value = "Generated LinkedIn post content"
    use_case = GenerateLinkedInPostUseCase(mock_openai_gateway)

    # Execute the use case
    result = use_case.execute()

    # Verify the result
    assert result == "Generated LinkedIn post content"
    mock_openai_gateway.generate.assert_called_once()

    # Verify that the prompt was properly configured
    call_args = mock_openai_gateway.generate.call_args[0][0]
    assert "linkedin" in call_args.lower()


def test_generate_linkedin_post_openai_error(mock_openai_gateway):
    """
    Test handling of OpenAIError during LinkedIn post generation.
    """
    # Configure the mock to raise an OpenAIError
    mock_openai_gateway.generate.side_effect = OpenAIError("API error")
    use_case = GenerateLinkedInPostUseCase(mock_openai_gateway)

    # Verify that the appropriate error is raised
    with pytest.raises(LinkedInGenerationError) as exc_info:
        use_case.execute()

    assert "Error generating LinkedIn post" in str(exc_info.value)
    assert "API error" in str(exc_info.value)


def test_generate_linkedin_post_unexpected_error(mock_openai_gateway):
    """
    Test handling of unexpected errors during LinkedIn post generation.
    """
    # Configure the mock to raise an unexpected error
    mock_openai_gateway.generate.side_effect = Exception("Unexpected error")
    use_case = GenerateLinkedInPostUseCase(mock_openai_gateway)

    # Verify that the appropriate error is raised
    with pytest.raises(LinkedInGenerationError) as exc_info:
        use_case.execute()

    assert "Unexpected error generating LinkedIn post" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", __file__])