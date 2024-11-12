# Location: tests/presentation/test_post_command.py

"""
This module contains unit tests for the PostCommand class, which handles platform-specific
content generation and posting commands. It verifies the command's initialization,
execution, and error handling across different platforms.

Test coverage includes:
- Command initialization with dependencies
- Platform-specific execution paths
- Dry run functionality
- Topic filtering
- Error handling scenarios
- Integration with gateways
"""

import pytest
from unittest.mock import patch, MagicMock
from src.presentation.post_command import PostCommand
from src.domain.exceptions import (
    AutomatorError, ValidationError, TwitterError, FacebookError,
    LinkedInError, OpenAIError, ConfigurationError
)


@pytest.fixture
def mock_openai_gateway():
    """
    Provides a mock OpenAI gateway for testing.

    Returns:
        MagicMock: A configured mock OpenAI gateway
    """
    mock = MagicMock()
    mock.generate.return_value = "Generated content"
    return mock


@pytest.fixture
def mock_gateways():
    """
    Provides mock gateway instances for all platforms.

    Returns:
        tuple: Mock instances for Facebook, LinkedIn, and Twitter gateways
    """
    mock_facebook = MagicMock()
    mock_facebook.post.return_value = {"id": "fb_123"}

    mock_linkedin = MagicMock()
    mock_linkedin.post.return_value = {"id": "li_456"}

    mock_twitter = MagicMock()
    mock_twitter.post_tweet.return_value = {"data": {"id": "tw_789"}}

    return mock_facebook, mock_linkedin, mock_twitter


def test_initialization_success():
    """
    Test successful PostCommand initialization.
    """
    with patch('src.presentation.post_command.OpenAIAPI') as mock_openai:
        command = PostCommand()
        assert command.openai_gateway == mock_openai.return_value


def test_initialization_failure():
    """
    Test PostCommand initialization failure.
    """
    with patch('src.presentation.post_command.OpenAIAPI', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            PostCommand()
        assert "API Error" in str(exc_info.value)


@pytest.mark.parametrize("platform,topic", [
    ("facebook", "business"),
    ("linkedin", "developer"),
    ("twitter", "slides")
])
def test_execute_with_topic(mock_openai_gateway, mock_gateways, platform, topic):
    """
    Test command execution with specified platform and topic.

    Args:
        platform (str): Target platform
        topic (str): Content topic category
    """
    mock_facebook, mock_linkedin, mock_twitter = mock_gateways

    with patch('src.presentation.post_command.OpenAIAPI', return_value=mock_openai_gateway), \
            patch('src.presentation.post_command.FacebookAPI', return_value=mock_facebook), \
            patch('src.presentation.post_command.LinkedInAPI', return_value=mock_linkedin), \
            patch('src.presentation.post_command.TwitterAPI', return_value=mock_twitter):

        command = PostCommand()
        result = command.execute(platform=platform, topic=topic)

        if platform == "facebook":
            assert result == {"id": "fb_123"}
            mock_facebook.post.assert_called_once()
        elif platform == "linkedin":
            assert result == {"id": "li_456"}
            mock_linkedin.post.assert_called_once()
        else:  # twitter
            assert result == {"data": {"id": "tw_789"}}
            mock_twitter.post_tweet.assert_called_once()


def test_execute_dry_run(mock_openai_gateway):
    """
    Test dry run execution that only generates content without posting.
    """
    with patch('src.presentation.post_command.OpenAIAPI', return_value=mock_openai_gateway):
        command = PostCommand()
        result = command.execute(platform="facebook", dry_run=True)

        assert result == "Generated content"
        mock_openai_gateway.generate.assert_called_once()


@pytest.mark.parametrize("platform,api_name,error_class,error_message", [
    ("facebook", "FacebookAPI", AutomatorError, "Failed to post to Facebook: Facebook API error"),
    ("linkedin", "LinkedInAPI", LinkedInError, "LinkedIn API error"),  # LinkedInError n'est pas encapsulé
    ("twitter", "TwitterAPI", TwitterError, "Twitter API error")
])
def test_execute_platform_errors(mock_openai_gateway, platform, api_name, error_class, error_message):
    """
    Test handling of platform-specific API errors.

    Args:
        platform (str): Target platform
        api_name (str): Exact API class name to mock
        error_class (Exception): Expected error class
        error_message (str): Expected error message
    """
    mock_api = MagicMock()

    # Configuration des erreurs spécifiques à chaque plateforme
    if platform == "facebook":
        mock_api.post.side_effect = FacebookError("Facebook API error")
    elif platform == "linkedin":
        mock_api.post.side_effect = LinkedInError("LinkedIn API error")
    else:  # twitter
        mock_api.post_tweet.side_effect = TwitterError("Twitter API error")

    with patch('src.presentation.post_command.OpenAIAPI', return_value=mock_openai_gateway), \
            patch(f'src.presentation.post_command.{api_name}', return_value=mock_api):

        command = PostCommand()
        with pytest.raises(error_class) as exc_info:
            command.execute(platform=platform)

        # Vérifie que le message d'erreur correspond exactement
        assert str(exc_info.value) == error_message


def test_execute_invalid_platform():
    """
    Test handling of invalid platform specification.
    """
    command = PostCommand()
    with pytest.raises(ValueError) as exc_info:
        command.execute(platform="invalid_platform")
    assert "Unsupported platform" in str(exc_info.value)


def test_content_generation_error(mock_openai_gateway):
    """
    Test handling of content generation errors.
    """
    mock_openai_gateway.generate.side_effect = OpenAIError("Generation failed")

    with patch('src.presentation.post_command.OpenAIAPI', return_value=mock_openai_gateway):
        command = PostCommand()
        with pytest.raises(OpenAIError) as exc_info:
            command.execute(platform="facebook")
        assert "Generation failed" in str(exc_info.value)


@patch('src.presentation.post_command.OpenAIAPI')
def test_handle_facebook_publishing(mock_openai_api):
    """
    Test detailed Facebook content generation and publishing flow.
    """
    mock_openai = MagicMock()
    mock_openai_api.return_value = mock_openai
    mock_openai.generate.return_value = "Facebook content"

    mock_facebook = MagicMock()
    mock_facebook.post.return_value = {"id": "123", "link": "facebook.com/post/123"}

    with patch('src.presentation.post_command.FacebookAPI', return_value=mock_facebook):
        command = PostCommand()
        result = command._handle_facebook(dry_run=False, topic="business")

        mock_openai.generate.assert_called_once()
        mock_facebook.post.assert_called_once()
        assert result == {"id": "123", "link": "facebook.com/post/123"}


@patch('src.presentation.post_command.OpenAIAPI')
def test_handle_linkedin_publishing(mock_openai_api):
    """
    Test detailed LinkedIn content generation and publishing flow.
    """
    mock_openai = MagicMock()
    mock_openai_api.return_value = mock_openai
    mock_openai.generate.return_value = "LinkedIn content"

    mock_linkedin = MagicMock()
    mock_linkedin.post.return_value = {"id": "456", "link": "linkedin.com/post/456"}

    with patch('src.presentation.post_command.LinkedInAPI', return_value=mock_linkedin):
        command = PostCommand()
        result = command._handle_linkedin(dry_run=False, topic="business")

        mock_openai.generate.assert_called_once()
        mock_linkedin.post.assert_called_once()
        assert result == {"id": "456", "link": "linkedin.com/post/456"}


@patch('src.presentation.post_command.OpenAIAPI')
def test_handle_twitter_publishing(mock_openai_api):
    """
    Test detailed Twitter content generation and publishing flow.
    """
    mock_openai = MagicMock()
    mock_openai_api.return_value = mock_openai
    mock_openai.generate.return_value = "Tweet content"

    mock_twitter = MagicMock()
    mock_twitter.post_tweet.return_value = {"data": {"id": "789"}}

    with patch('src.presentation.post_command.TwitterAPI', return_value=mock_twitter):
        command = PostCommand()
        result = command._handle_twitter(dry_run=False, topic="business")

        mock_openai.generate.assert_called_once()
        mock_twitter.post_tweet.assert_called_once()
        assert result == {"data": {"id": "789"}}


if __name__ == "__main__":
    pytest.main(["-v", __file__])