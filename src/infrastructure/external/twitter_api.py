# src/infrastructure/external/twitter_api.py

"""
This module implements the TwitterAPI class, which serves as a concrete
implementation of the TwitterGateway interface. It handles the actual
communication with the Twitter API, including authentication and tweet posting.
"""


from requests_oauthlib import OAuth1Session
from src.interfaces.twitter_gateway import TwitterGateway
from src.domain.entities.tweet import Tweet
from src.infrastructure.logging.logger import logger, log_method
from src.infrastructure.config.environment import get_twitter_credentials
from src.domain.exceptions import TwitterError, ConfigurationError


class TwitterAPI(TwitterGateway):
    """
    A concrete implementation of the TwitterGateway interface.

    This class handles the authentication and communication with the Twitter API,
    allowing the application to post tweets and perform other Twitter-related operations.
    """

    @log_method(logger)
    def __init__(self):
        """
        Initialize the TwitterAPI with the necessary credentials.

        Raises:
            ConfigurationError: If there's an error loading the Twitter credentials.
        """
        try:
            logger.debug("Loading Twitter credentials")
            credentials = get_twitter_credentials()
            logger.debug(f"Credentials loaded: {', '.join(credentials.keys())}")
            self.oauth_session = OAuth1Session(
                credentials['consumer_key'],
                client_secret=credentials['consumer_secret'],
                resource_owner_key=credentials['access_token'],
                resource_owner_secret=credentials['access_token_secret'],
            )
            logger.debug("OAuth session created successfully")
        except ConfigurationError as e:
            logger.error(f"Failed to initialize Twitter API: {str(e)}")
            raise

    @log_method(logger)
    def post_tweet(self, tweet: Tweet):
        """
        Post a tweet to Twitter.

        Args:
            tweet (Tweet): The Tweet entity to be posted.

        Returns:
            dict: The response from the Twitter API containing the posted tweet's data.

        Raises:
            TwitterError: If there's an error posting the tweet to Twitter.
        """
        try:
            logger.debug(f"Validating tweet: {tweet.text[:20]}...")
            tweet.validate()
            logger.debug("Tweet validation passed")

            payload = {"text": tweet.text}
            logger.debug(f"Prepared payload: {payload}")

            logger.debug("Sending request to Twitter API")
            response = self.oauth_session.post(
                "https://api.twitter.com/2/tweets",
                json=payload,
            )
            logger.debug(f"API response status code: {response.status_code}")

            response.raise_for_status()
            response_json = response.json()
            logger.debug(f"API response content: {response_json}")

            return response_json
        except Exception as e:
            logger.error(f"Failed to post tweet: {str(e)}")
            raise TwitterError(f"Failed to post tweet: {str(e)}")