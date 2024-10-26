# Location: tests/use_cases/test_post_facebook.py

"""
This module contains unit tests for the PostFacebookUseCase class.
It tests the execution of the use case with various scenarios including
successful posting and error handling.
"""

import sys
import os
import pytest
from unittest.mock import Mock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.use_cases.post_facebook import PostFacebookUseCase
from src.domain.entities.facebook_publication import FacebookPublication
from src.domain.exceptions import AutomatorError, ValidationError

@pytest.fixture
def mock_facebook_gateway():
    """
    Fixture providing a mock Facebook gateway.
    """
    return Mock()

def test_post_facebook_success(mock_facebook_gateway):
    """
    Test successful Facebook post creation.
    """
    mock_facebook_gateway.post.return_value = {"id": "123_456"}
    use_case = PostFacebookUseCase(mock_facebook_gateway)

    result = use_case.execute("Test Facebook post", "PUBLIC")

    assert result == {"id": "123_456"}
    mock_facebook_gateway.post.assert_called_once()
    assert isinstance(mock_facebook_gateway.post.call_args[0][0], FacebookPublication)
    assert mock_facebook_gateway.post.call_args[0][0].get_text() == "Test Facebook post"
    assert mock_facebook_gateway.post.call_args[0][0].get_privacy() == "PUBLIC"

def test_post_facebook_custom_privacy(mock_facebook_gateway):
    """
    Test Facebook post creation with custom privacy setting.
    """
    mock_facebook_gateway.post.return_value = {"id": "123_456"}
    use_case = PostFacebookUseCase(mock_facebook_gateway)

    result = use_case.execute("Test Facebook post", "FRIENDS")

    assert result == {"id": "123_456"}
    publication = mock_facebook_gateway.post.call_args[0][0]
    assert publication.get_privacy() == "FRIENDS"

def test_post_facebook_validation_error(mock_facebook_gateway):
    """
    Test handling of validation errors during post creation.
    """
    use_case = PostFacebookUseCase(mock_facebook_gateway)

    with pytest.raises(AutomatorError) as exc_info:
        use_case.execute("")  # Empty text should trigger validation error

    assert "Failed to post to Facebook" in str(exc_info.value)
    mock_facebook_gateway.post.assert_not_called()

def test_post_facebook_gateway_error(mock_facebook_gateway):
    """
    Test handling of gateway errors during post creation.
    """
    mock_facebook_gateway.post.side_effect = Exception("Gateway error")
    use_case = PostFacebookUseCase(mock_facebook_gateway)

    with pytest.raises(AutomatorError) as exc_info:
        use_case.execute("Test Facebook post")

    assert "Failed to post to Facebook" in str(exc_info.value)
    assert "Gateway error" in str(exc_info.value)

if __name__ == "__main__":
    pytest.main(["-v", __file__])