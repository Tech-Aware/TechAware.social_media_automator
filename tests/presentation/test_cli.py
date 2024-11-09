# tests/presentation/test_cli.py

"""
This module contains unit tests for the CLI class. It tests the actual implementation
of the CLI including menu selection, content generation and posting capabilities,
and comprehensive error handling scenarios.
"""

import pytest
from unittest.mock import patch, MagicMock, call
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


@pytest.mark.parametrize("user_input,expected_call", [
    ("y", None),  # blog article option
    ("n", "run"),  # social media option
])
def test_menu_selection(mock_gateways, user_input, expected_call):
    """
    Test menu selection handling based on user input.

    Args:
        mock_gateways: Fixture providing mock gateway instances
        user_input: The simulated user input
        expected_call: The expected method to be called
    """
    mock_twitter, mock_facebook, mock_linkedin, mock_openai = mock_gateways

    with patch('src.presentation.cli.TwitterAPI', return_value=mock_twitter), \
            patch('src.presentation.cli.FacebookAPI', return_value=mock_facebook), \
            patch('src.presentation.cli.LinkedInAPI', return_value=mock_linkedin), \
            patch('src.presentation.cli.OpenAIAPI', return_value=mock_openai), \
            patch('builtins.input', return_value=user_input), \
            patch('builtins.print') as mock_print, \
            patch.object(CLI, 'run') as mock_run:

        cli = CLI()
        cli.menu()

        if user_input.lower() == "y":
            mock_print.assert_called_with("You want to create a blog article first !")  # Fixed space before !
            mock_run.assert_not_called()
        else:
            mock_run.assert_called_once()


def test_cli_run_success(mock_gateways):
    """
    Test successful execution of the run method with all content generation and posting.
    """
    mock_twitter, mock_facebook, mock_linkedin, mock_openai = mock_gateways

    # Configure mock responses
    mock_facebook_content = "Generated Facebook content"
    mock_linkedin_content = "Generated LinkedIn content"
    mock_tweet_content = "Generated tweet content"

    with patch('src.presentation.cli.TwitterAPI', return_value=mock_twitter), \
            patch('src.presentation.cli.FacebookAPI', return_value=mock_facebook), \
            patch('src.presentation.cli.LinkedInAPI', return_value=mock_linkedin), \
            patch('src.presentation.cli.OpenAIAPI', return_value=mock_openai), \
            patch('builtins.print') as mock_print, \
            patch('time.sleep'):  # Mock sleep to speed up tests

        # Create CLI instance and configure mocks
        cli = CLI()

        # Mock generation use cases
        cli.generate_facebook_use_case.execute = MagicMock(return_value=mock_facebook_content)
        cli.generate_linkedin_use_case.execute = MagicMock(return_value=mock_linkedin_content)
        cli.generate_tweet_use_case.execute = MagicMock(return_value=mock_tweet_content)

        # Mock posting use cases
        cli.post_facebook_use_case.execute = MagicMock(return_value={"id": "123456"})
        cli.post_linkedin_use_case.execute = MagicMock(return_value={"id": "789012"})
        cli.post_tweet_use_case.execute = MagicMock(return_value={"id": "345678"})

        # Run the CLI
        cli.run()

        # Verify content generation calls
        cli.generate_facebook_use_case.execute.assert_called_once()
        cli.generate_linkedin_use_case.execute.assert_called_once()
        cli.generate_tweet_use_case.execute.assert_called_once()

        # Verify posting calls
        cli.post_facebook_use_case.execute.assert_called_once_with(mock_facebook_content)
        cli.post_linkedin_use_case.execute.assert_called_once_with(mock_linkedin_content)
        cli.post_tweet_use_case.execute.assert_called_once_with(mock_tweet_content)

        # Verify progress messages
        assert any("Waiting for facebook generation" in str(call) for call in mock_print.call_args_list)
        assert any("Waiting for linkedin generation" in str(call) for call in mock_print.call_args_list)
        assert any("Waiting for X tweet generation" in str(call) for call in mock_print.call_args_list)


@pytest.mark.parametrize("exception,expected_message", [
    (ValidationError("Invalid content"), "Invalid content"),
    (FacebookError("Facebook API error"), "Facebook error"),
    (LinkedInError("LinkedIn API error"), "LinkedIn error"),
    (TwitterError("Twitter API error"), "Twitter error"),
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
            patch('builtins.print') as mock_print, \
            patch('time.sleep'):
        cli = CLI()
        cli.generate_facebook_use_case.execute = MagicMock(side_effect=exception)

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
            patch('builtins.print') as mock_print, \
            patch('time.sleep'):
        cli = CLI()
        cli.generate_facebook_use_case.execute = MagicMock(side_effect=original_error)

        with pytest.raises(AutomatorError) as exc_info:
            cli.run()

        assert exc_info.value is original_error
        mock_print.assert_any_call("An error occurred: Original error")


if __name__ == "__main__":
    pytest.main(["-v", __file__])