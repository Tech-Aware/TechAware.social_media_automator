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
from src.domain.exceptions import OpenAIError, FacebookGenerationError


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
    mock_openai_gateway.generate.return_value = "Generated Facebook publication content"
    use_case = GenerateFacebookPublicationUseCase(mock_openai_gateway)

    result = use_case.execute()

    assert result == "Generated Facebook publication content"
    mock_openai_gateway.generate.assert_called_once()

    # Verify that the prompt contains Facebook-specific context
    call_args = mock_openai_gateway.generate.call_args[0][0]
    assert "facebook" in call_args.lower()


def test_generate_facebook_publication_openai_error(mock_openai_gateway):
    """
    Test handling of OpenAIError during Facebook publication generation.
    """
    mock_openai_gateway.generate.side_effect = OpenAIError("API error")
    use_case = GenerateFacebookPublicationUseCase(mock_openai_gateway)

    with pytest.raises(FacebookGenerationError) as exc_info:
        use_case.execute()

    assert "Error generating Facebook publication" in str(exc_info.value)
    assert "API error" in str(exc_info.value)


def test_generate_facebook_publication_unexpected_error(mock_openai_gateway):
    """
    Test handling of unexpected errors during Facebook publication generation.
    """
    mock_openai_gateway.generate.side_effect = Exception("Unexpected error")
    use_case = GenerateFacebookPublicationUseCase(mock_openai_gateway)

    with pytest.raises(FacebookGenerationError) as exc_info:
        use_case.execute()

    assert "Unexpected error generating Facebook publication" in str(exc_info.value)


def test_generate_facebook_publication_prompt_building(mock_openai_gateway):
    """
    Test that the prompt is correctly built using the PromptBuilder.
    """
    mock_openai_gateway.generate.return_value = "Generated content"
    use_case = GenerateFacebookPublicationUseCase(mock_openai_gateway)

    result = use_case.execute()

    assert result == "Generated content"
    mock_openai_gateway.generate.assert_called_once()

    # Verify that the prompt includes expected Facebook-specific elements
    call_args = mock_openai_gateway.generate.call_args[0][0]
    assert "facebook" in call_args.lower()
    assert "engaging" in call_args.lower()
    assert "storytelling" in call_args.lower()


if __name__ == "__main__":
    pytest.main(["-v", __file__])