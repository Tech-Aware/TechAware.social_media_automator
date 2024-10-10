# src/domain/entities/tweet.py

"""
This module defines the Tweet entity, representing a tweet in the application.
It encapsulates the tweet's text and provides validation logic to ensure
the tweet conforms to Twitter's character limit requirements.
"""


from src.domain.exceptions import ValidationError
from src.infrastructure.logging.logger import logger, log_method


class Tweet:
    @log_method(logger)
    def __init__(self, text):
        logger.debug(f"Creating Tweet object with text: {text[:20]}...")
        self.text = text
        logger.debug("Tweet object created successfully")

    @log_method(logger)
    def validate(self):
        logger.debug(f"Validating tweet: {self.text[:20]}...")
        if not self.text:
            logger.warning("Tweet validation failed: Empty tweet")
            raise ValidationError("Tweet cannot be empty")

        if len(self.text) > 280:
            logger.warning(f"Tweet validation failed: Tweet too long ({len(self.text)} characters)")
            raise ValidationError(f"Tweet must be 280 characters or less (current: {len(self.text)})")

        logger.debug("Tweet validation passed")

    @log_method(logger)
    def get_text(self):
        logger.debug("Retrieving tweet text")
        return self.text

    @log_method(logger)
    def set_text(self, new_text):
        logger.debug(f"Setting new tweet text: {new_text[:20]}...")
        self.text = new_text
        logger.debug("New tweet text set successfully")
        try:
            self.validate()
            logger.success("New tweet text is valid")
        except ValidationError as e:
            logger.warning(f"New tweet text is invalid: {str(e)}")
            raise ValidationError(f"Invalid tweet text: {str(e)}") from e

    @staticmethod
    @log_method(logger)
    def create_tweet(text):
        logger.debug(f"Creating and validating new tweet: {text[:20]}...")
        tweet = Tweet(text)
        try:
            tweet.validate()
            logger.success("Tweet created and validated successfully")
            return tweet
        except ValidationError as e:
            logger.error(f"Failed to create valid tweet: {str(e)}")
            raise ValidationError(f"Failed to create valid tweet: {str(e)}") from e