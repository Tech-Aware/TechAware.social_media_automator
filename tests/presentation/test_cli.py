# Location: tests/presentation/test_cli.py

"""
This module contains unit tests for the CLI class, including platform-specific
prompt handling, content generation, posting capabilities, and comprehensive
error handling scenarios. It verifies the correct behavior of the CLI under
both normal and error conditions.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.presentation.cli import CLI
from src.domain.exceptions import (
    ValidationError, TwitterError, FacebookError, LinkedInError,
    OpenAIError, TweetGenerationError, AutomatorError, ConfigurationError
)


@pytest.fixture
def mock_gateways():
    """
    Fixture providing mock gateway instances for all platforms.

    Returns:
        tuple: Mock instances for Twitter, Facebook, LinkedIn, and OpenAI gateways
    """
    mock_twitter = MagicMock()
    mock_facebook = MagicMock()
    mock_linkedin = MagicMock()
    mock_openai = MagicMock()
    return mock_twitter, mock_facebook, mock_linkedin, mock_openai


def test_cli_initialization_success():
    """
    Test successful CLI initialization with all components.
    """
    with patch('src.presentation.cli.TwitterAPI'), \
            patch('src.presentation.cli.FacebookAPI'), \
            patch('src.presentation.cli.LinkedInAPI'), \
            patch('src.presentation.cli.OpenAIAPI'):
        cli = CLI()
        assert isinstance(cli, CLI)


def test_cli_initialization_error():
    """
    Test CLI initialization failure due to configuration error.
    """
    with patch('src.presentation.cli.TwitterAPI', side_effect=ConfigurationError("Config error")), \
            patch('src.presentation.cli.FacebookAPI'), \
            patch('src.presentation.cli.LinkedInAPI'), \
            patch('src.presentation.cli.OpenAIAPI'):
        with pytest.raises(AutomatorError) as exc_info:
            CLI()
        assert "Failed to initialize CLI due to configuration error" in str(exc_info.value)


@pytest.mark.parametrize("platform", ["twitter", "facebook", "linkedin"])
def test_read_platform_prompt_success(platform):
    """
    Test successful prompt reading for each platform.

    Args:
        platform: The social media platform to test
    """
    expected_content = f"Test prompt for {platform}"
    with patch('src.presentation.cli.TwitterAPI'), \
            patch('src.presentation.cli.FacebookAPI'), \
            patch('src.presentation.cli.LinkedInAPI'), \
            patch('src.presentation.cli.OpenAIAPI'), \
            patch('src.presentation.cli.read_prompt_file', return_value=expected_content) as mock_read:
        cli = CLI()
        result = cli.read_platform_prompt(platform)
        assert result == expected_content
        mock_read.assert_called_once_with(platform)


@pytest.mark.parametrize("platform", ["twitter", "facebook", "linkedin"])
def test_read_platform_prompt_file_not_found(platform):
    """
    Test prompt reading with missing files for each platform.

    Args:
        platform: The social media platform to test
    """
    with patch('src.presentation.cli.TwitterAPI'), \
            patch('src.presentation.cli.FacebookAPI'), \
            patch('src.presentation.cli.LinkedInAPI'), \
            patch('src.presentation.cli.OpenAIAPI'), \
            patch('src.presentation.cli.read_prompt_file', side_effect=FileNotFoundError()):
        cli = CLI()
        result = cli.read_platform_prompt(platform)
        assert result == f"Generate an engaging {platform} post about technology."


def test_read_platform_prompt_unexpected_error():
    """
    Test handling of unexpected errors during prompt reading.
    """
    with patch('src.presentation.cli.TwitterAPI'), \
            patch('src.presentation.cli.FacebookAPI'), \
            patch('src.presentation.cli.LinkedInAPI'), \
            patch('src.presentation.cli.OpenAIAPI'), \
            patch('src.presentation.cli.read_prompt_file', side_effect=Exception("Unexpected error")):
        cli = CLI()
        with pytest.raises(AutomatorError) as exc_info:
            cli.read_platform_prompt("facebook")
        assert "Unexpected error reading prompt file" in str(exc_info.value)


def test_cli_run_success(mock_gateways):
    """
    Test successful content generation and posting to Facebook.
    """
    mock_twitter, mock_facebook, mock_linkedin, mock_openai = mock_gateways

    with patch('src.presentation.cli.TwitterAPI', return_value=mock_twitter), \
            patch('src.presentation.cli.FacebookAPI', return_value=mock_facebook), \
            patch('src.presentation.cli.LinkedInAPI', return_value=mock_linkedin), \
            patch('src.presentation.cli.OpenAIAPI', return_value=mock_openai), \
            patch.object(CLI, 'read_platform_prompt', return_value="Test prompt"), \
            patch('builtins.print') as mock_print, \
            patch('time.sleep'):
        # Create CLI instance
        cli = CLI()

        # Configure mock responses properly
        mock_generate_facebook = MagicMock(return_value="Generated Facebook content")
        mock_post_facebook = MagicMock(return_value={"id": "123456"})

        # Replace the real methods with mocks
        cli.generate_facebook_use_case.execute = mock_generate_facebook
        cli.post_facebook_use_case.execute = mock_post_facebook

        # Run the CLI
        cli.run()

        # Verify content generation
        mock_generate_facebook.assert_called_once_with("Test prompt")
        mock_post_facebook.assert_called_once_with("Generated Facebook content")

        # Verify output messages
        mock_print.assert_any_call("Generated Facebook post: Generated Facebook content")
        mock_print.assert_any_call("Facebook post created successfully. Post ID: 123456")


@pytest.mark.parametrize("exception,expected_message", [
    (ValidationError("Invalid content"), "Invalid content"),
    (FacebookError("Facebook API error"), "Facebook error"),
    (OpenAIError("OpenAI API error"), "OpenAI error"),
    (TweetGenerationError("Generation failed"), "Content generation error"),
    (Exception("Unexpected error"), "An unexpected error occurred")
])
def test_cli_run_errors(mock_gateways, exception, expected_message):
    """
    Test error handling for various failure scenarios.

    Args:
        mock_gateways: Fixture providing mock gateway instances
        exception: The exception to simulate
        expected_message: Expected error message
    """
    mock_twitter, mock_facebook, mock_linkedin, mock_openai = mock_gateways

    with patch('src.presentation.cli.TwitterAPI', return_value=mock_twitter), \
            patch('src.presentation.cli.FacebookAPI', return_value=mock_facebook), \
            patch('src.presentation.cli.LinkedInAPI', return_value=mock_linkedin), \
            patch('src.presentation.cli.OpenAIAPI', return_value=mock_openai), \
            patch.object(CLI, 'read_platform_prompt', side_effect=exception), \
            patch('builtins.print') as mock_print:
        cli = CLI()

        with pytest.raises(AutomatorError) as exc_info:
            cli.run()

        assert expected_message in str(exc_info.value)
        assert any(expected_message in str(call) for call in mock_print.call_args_list)


def test_cli_reraising_automator_error(mock_gateways):
    """
    Test that AutomatorError is re-raised without modification.
    """
    mock_twitter, mock_facebook, mock_linkedin, mock_openai = mock_gateways
    original_error = AutomatorError("Original error")

    with patch('src.presentation.cli.TwitterAPI', return_value=mock_twitter), \
            patch('src.presentation.cli.FacebookAPI', return_value=mock_facebook), \
            patch('src.presentation.cli.LinkedInAPI', return_value=mock_linkedin), \
            patch('src.presentation.cli.OpenAIAPI', return_value=mock_openai), \
            patch.object(CLI, 'read_platform_prompt', side_effect=original_error), \
            patch('builtins.print') as mock_print:
        cli = CLI()

        with pytest.raises(AutomatorError) as exc_info:
            cli.run()

        assert exc_info.value is original_error
        mock_print.assert_called_with("An error occurred: Original error")


if __name__ == "__main__":
    pytest.main(["-v", __file__])