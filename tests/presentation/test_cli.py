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
from src.domain.exceptions import ValidationError, TwitterError, OpenAIError, TweetGenerationError, AutomatorError


@pytest.fixture
def mock_use_cases():
    mock_post_tweet = MagicMock()
    mock_generate_tweet = MagicMock()
    return mock_post_tweet, mock_generate_tweet


def test_cli_initialization():
    with patch('src.presentation.cli.TwitterAPI'), \
            patch('src.presentation.cli.OpenAIAPI'), \
            patch('src.presentation.cli.PostTweetUseCase'), \
            patch('src.presentation.cli.GenerateTweetUseCase'):
        cli = CLI()
        assert isinstance(cli, CLI)


@pytest.mark.parametrize("prompt,generated_tweet,expected_output", [
    ("Test prompt", "Generated tweet", "Tweet posté avec succès. ID du tweet : 12345"),
    ("", "Hello World !", "Tweet posté avec succès. ID du tweet : 12345"),
])
def test_cli_run_success(mock_use_cases, prompt, generated_tweet, expected_output):
    mock_post_tweet, mock_generate_tweet = mock_use_cases
    mock_post_tweet.execute.return_value = {"data": {"id": "12345"}}
    mock_generate_tweet.execute.return_value = generated_tweet

    with patch('src.presentation.cli.TwitterAPI'), \
            patch('src.presentation.cli.OpenAIAPI'), \
            patch('src.presentation.cli.PostTweetUseCase', return_value=mock_post_tweet), \
            patch('src.presentation.cli.GenerateTweetUseCase', return_value=mock_generate_tweet), \
            patch('src.presentation.cli.read_prompt_file', return_value=prompt), \
            patch('builtins.print') as mock_print, \
            patch('time.sleep'):  # Mock sleep to speed up the test
        cli = CLI()
        cli.run()

        if prompt:
            mock_generate_tweet.execute.assert_called_once_with(prompt)
            mock_post_tweet.execute.assert_called_once_with(generated_tweet)
        else:
            mock_post_tweet.execute.assert_called_once_with("Hello World !")

        mock_print.assert_any_call(expected_output)


@pytest.mark.parametrize("exception,expected_output", [
    (FileNotFoundError("File not found"), "Le fichier prompt n'a pas été trouvé. Utilisation d'un prompt par défaut."),
    (IOError("IO Error"), "Erreur lors de la lecture du fichier prompt. Utilisation d'un prompt par défaut."),
    (ValidationError("Invalid tweet"), "Tweet invalide : Invalid tweet"),
    (TwitterError("Twitter API error"), "Erreur lors de la publication sur Twitter : Twitter API error"),
    (OpenAIError("OpenAI API error"), "Erreur avec OpenAI : OpenAI API error"),
    (TweetGenerationError("Generation failed"), "Erreur lors de la génération du tweet : Generation failed"),
    (AutomatorError("Automator error"), "Une erreur s'est produite : Automator error"),
    (Exception("Unexpected error"), "Une erreur inattendue s'est produite : Unexpected error"),
])
def test_cli_run_errors(mock_use_cases, exception, expected_output):
    mock_post_tweet, mock_generate_tweet = mock_use_cases
    default_prompt = "Générez un tweet intéressant sur la technologie."

    with patch('src.presentation.cli.TwitterAPI'), \
         patch('src.presentation.cli.OpenAIAPI'), \
         patch('src.presentation.cli.PostTweetUseCase', return_value=mock_post_tweet), \
         patch('src.presentation.cli.GenerateTweetUseCase', return_value=mock_generate_tweet), \
         patch('src.presentation.cli.read_prompt_file', side_effect=exception if isinstance(exception, (FileNotFoundError, IOError)) else None), \
         patch('builtins.print') as mock_print, \
         patch('time.sleep'):  # Mock sleep to speed up the test

        if isinstance(exception, (FileNotFoundError, IOError)):
            mock_generate_tweet.execute.return_value = "Generated tweet"
        else:
            mock_generate_tweet.execute.side_effect = exception
            mock_post_tweet.execute.side_effect = exception

        cli = CLI()
        cli.run()

        mock_print.assert_any_call(expected_output)

        if isinstance(exception, (FileNotFoundError, IOError)):
            mock_generate_tweet.execute.assert_called_once_with(default_prompt)
            mock_post_tweet.execute.assert_called_once_with("Generated tweet")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
