# tests/presentation/test_cli.py

"""
This module contains unit tests for the CLI (Command Line Interface) class.
It tests the initialization of the CLI and its run method, including various
scenarios such as successful tweet posting and error handling.
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from unittest.mock import patch, MagicMock
from src.presentation.cli import CLI
from src.domain.exceptions import ValidationError, TwitterError, OpenAIError, TweetGenerationError


@pytest.fixture
def mock_use_cases():
    """
    Fixture to create mock use cases for testing.
    """
    mock_post_tweet = MagicMock()
    mock_generate_tweet = MagicMock()
    return mock_post_tweet, mock_generate_tweet


def test_cli_initialization():
    """
    Test that the CLI can be initialized without errors.
    """
    with patch('src.presentation.cli.TwitterAPI'), \
         patch('src.presentation.cli.OpenAIAPI'), \
         patch('src.presentation.cli.PostTweetUseCase'), \
         patch('src.presentation.cli.GenerateTweetUseCase'):
        cli = CLI()
        assert cli is not None


@pytest.mark.parametrize("prompt,generated_tweet,user_input,expected_output", [
    ("", "", "Hello, world!", "Tweet posté avec succès. ID du tweet : 12345"),
    ("Test prompt", "Generated tweet", "", "Tweet posté avec succès. ID du tweet : 12345"),
    ("Test prompt", "Generated tweet", "Custom tweet", "Tweet posté avec succès. ID du tweet : 12345"),
])
def test_cli_run_success(mock_use_cases, prompt, generated_tweet, user_input, expected_output):
    """
    Test the CLI's run method for successful scenarios.
    """
    mock_post_tweet, mock_generate_tweet = mock_use_cases
    mock_post_tweet.execute.return_value = {"data": {"id": "12345"}}
    mock_generate_tweet.execute.return_value = generated_tweet

    with patch('src.presentation.cli.TwitterAPI'), \
         patch('src.presentation.cli.OpenAIAPI'), \
         patch('src.presentation.cli.PostTweetUseCase', return_value=mock_post_tweet), \
         patch('src.presentation.cli.GenerateTweetUseCase', return_value=mock_generate_tweet), \
         patch('builtins.input', side_effect=[prompt, user_input]), \
         patch('builtins.print') as mock_print:
        cli = CLI()
        cli.run()

        if prompt:
            mock_generate_tweet.execute.assert_called_once_with(prompt)
        mock_post_tweet.execute.assert_called_once()
        mock_print.assert_called_with(expected_output)


@pytest.mark.parametrize("exception,expected_output", [
    (ValidationError("Invalid tweet"), "Tweet invalide : Invalid tweet"),
    (TwitterError("Twitter API error"), "Erreur lors de la publication sur Twitter : Twitter API error"),
    (OpenAIError("OpenAI API error"), "Erreur avec OpenAI : OpenAI API error"),
    (TweetGenerationError("Generation failed"), "Erreur lors de la génération du tweet : Generation failed"),
    (Exception("Unexpected error"), "Une erreur inattendue s'est produite : Unexpected error"),
])
def test_cli_run_errors(mock_use_cases, exception, expected_output):
    """
    Test the CLI's run method for error scenarios.
    """
    mock_post_tweet, mock_generate_tweet = mock_use_cases
    mock_post_tweet.execute.side_effect = exception

    with patch('src.presentation.cli.TwitterAPI'), \
         patch('src.presentation.cli.OpenAIAPI'), \
         patch('src.presentation.cli.PostTweetUseCase', return_value=mock_post_tweet), \
         patch('src.presentation.cli.GenerateTweetUseCase', return_value=mock_generate_tweet), \
         patch('builtins.input', return_value=""), \
         patch('builtins.print') as mock_print:
        cli = CLI()
        cli.run()

        mock_print.assert_called_with(expected_output)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
