# src/use_cases/post_tweet.py

"""
This module implements the PostTweetUseCase class, which encapsulates the
business logic for posting a tweet. It coordinates between the domain entities
and the Twitter gateway to execute the tweet posting process.
"""

from src.domain.entities.tweet import Tweet
from src.interfaces.twitter_gateway import TwitterGateway
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError


class PostTweetUseCase:
    @log_method(logger)
    def __init__(self, twitter_gateway: TwitterGateway):
        self.twitter_gateway = twitter_gateway
        logger.debug(f"PostTweetUseCase initialized with {twitter_gateway.__class__.__name__}")

    @log_method(logger)
    def execute(self, tweet_text: str):
        try:
            logger.debug(f"Creating Tweet entity with text: {tweet_text[:20]}...")
            tweet = Tweet(tweet_text)
            logger.debug("Tweet entity created")

            logger.debug("Posting tweet via TwitterGateway")
            result = self.twitter_gateway.post_tweet(tweet)
            logger.debug(f"Tweet posted, result: {result}")

            return result
        except AutomatorError as e:
            logger.error(f"Error in PostTweetUseCase: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in PostTweetUseCase: {str(e)}")
            raise AutomatorError(f"Unexpected error: {str(e)}")