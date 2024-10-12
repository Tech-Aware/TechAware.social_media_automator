# Location: tests/use_cases/test_post_linkedin.py

"""
This module contains unit tests for the PostLinkedInUseCase class.
It tests the execution of the use case with various scenarios including
successful publication posting and error handling.
"""

import pytest
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from unittest.mock import Mock
from src.use_cases.post_linkedin import PostLinkedInUseCase
from src.domain.entities.linkedin_publication import LinkedInPublication
from src.domain.exceptions import LinkedInError, ValidationError, AutomatorError


@pytest.fixture
def mock_linkedin_gateway():
    return Mock()


def test_post_linkedin_success(mock_linkedin_gateway):
    """
    Test successful LinkedIn publication posting.
    """
    mock_linkedin_gateway.post.return_value = {"id": "123456"}
    use_case = PostLinkedInUseCase(mock_linkedin_gateway)

    result = use_case.execute("Test LinkedIn publication")

    assert result == {"id": "123456"}
    mock_linkedin_gateway.post.assert_called_once()
    assert isinstance(mock_linkedin_gateway.post.call_args[0][0], LinkedInPublication)
    assert mock_linkedin_gateway.post.call_args[0][0].get_text() == "Test LinkedIn publication"


def test_post_linkedin_validation_error():
    """
    Test handling of ValidationError during LinkedIn publication creation.
    """
    use_case = PostLinkedInUseCase(Mock())

    with pytest.raises(ValidationError) as exc_info:
        use_case.execute("      " * 1000)  # Publication too long

    assert "LinkedIn publication text must be 3000 characters or less" in str(exc_info.value)


def test_post_linkedin_linkedin_error(mock_linkedin_gateway):
    """
    Test handling of LinkedInError during publication posting.
    """
    mock_linkedin_gateway.post.side_effect = LinkedInError("API error")
    use_case = PostLinkedInUseCase(mock_linkedin_gateway)

    with pytest.raises(LinkedInError) as exc_info:
        use_case.execute("Test LinkedIn publication")

    assert str(exc_info.value) == "API error"
    mock_linkedin_gateway.post.assert_called_once()


def test_post_linkedin_unexpected_error(mock_linkedin_gateway):
    """
    Test handling of unexpected errors during publication posting.
    """
    mock_linkedin_gateway.post.side_effect = Exception("Unexpected error")
    use_case = PostLinkedInUseCase(mock_linkedin_gateway)

    with pytest.raises(AutomatorError) as exc_info:
        use_case.execute("Test LinkedIn publication")

    assert "Unexpected error" in str(exc_info.value)
    mock_linkedin_gateway.post.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
