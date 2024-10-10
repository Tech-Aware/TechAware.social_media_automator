# tests/infrastructure/external/test_twitter_api.py

"""
Ce module contient les tests unitaires pour la classe TwitterAPI
définie dans src.infrastructure.external.twitter_api.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Ajoute le répertoire racine du projet au sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.external.twitter_api import TwitterAPI
from src.domain.entities.tweet import Tweet
from src.domain.exceptions import ConfigurationError, TwitterError


@patch('src.infrastructure.external.twitter_api.get_twitter_credentials')
@patch('src.infrastructure.external.twitter_api.OAuth1Session')
def test_twitter_api_initialization(mock_oauth, mock_get_credentials):
    mock_get_credentials.return_value = {
        'consumer_key': 'fake_key',
        'consumer_secret': 'fake_secret',
        'access_token': 'fake_token',
        'access_token_secret': 'fake_token_secret'
    }
    TwitterAPI()
    mock_oauth.assert_called_once_with(
        'fake_key',
        client_secret='fake_secret',
        resource_owner_key='fake_token',
        resource_owner_secret='fake_token_secret'
    )

@patch('src.infrastructure.external.twitter_api.get_twitter_credentials')
def test_twitter_api_initialization_error(mock_get_credentials):
    mock_get_credentials.side_effect = ConfigurationError("Credentials not found")
    with pytest.raises(ConfigurationError):
        TwitterAPI()

@patch('src.infrastructure.external.twitter_api.get_twitter_credentials')
@patch('src.infrastructure.external.twitter_api.OAuth1Session')
def test_post_tweet(mock_oauth, mock_get_credentials):
    mock_get_credentials.return_value = {
        'consumer_key': 'fake_key',
        'consumer_secret': 'fake_secret',
        'access_token': 'fake_token',
        'access_token_secret': 'fake_token_secret'
    }
    mock_session = MagicMock()
    mock_oauth.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": {"id": "12345"}}
    mock_session.post.return_value = mock_response

    api = TwitterAPI()
    tweet = Tweet("Test tweet")
    result = api.post_tweet(tweet)

    assert result == {"data": {"id": "12345"}}
    mock_session.post.assert_called_once_with(
        "https://api.twitter.com/2/tweets",
        json={"text": "Test tweet"}
    )

@patch('src.infrastructure.external.twitter_api.get_twitter_credentials')
@patch('src.infrastructure.external.twitter_api.OAuth1Session')
def test_post_tweet_error(mock_oauth, mock_get_credentials):
    mock_get_credentials.return_value = {
        'consumer_key': 'fake_key',
        'consumer_secret': 'fake_secret',
        'access_token': 'fake_token',
        'access_token_secret': 'fake_token_secret'
    }
    mock_session = MagicMock()
    mock_oauth.return_value = mock_session
    mock_session.post.side_effect = Exception("API Error")

    api = TwitterAPI()
    tweet = Tweet("Test tweet")
    with pytest.raises(TwitterError):
        api.post_tweet(tweet)

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
