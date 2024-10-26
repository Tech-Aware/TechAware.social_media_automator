# Location: src/use_cases/post_facebook.py

"""
This module implements the PostFacebookUseCase class, which encapsulates
the business logic for posting to Facebook. It coordinates between the domain entities
and the Facebook gateway to execute the posting process.
"""

from src.domain.entities.facebook_publication import FacebookPublication
from src.interfaces.facebook_gateway import FacebookGateway
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError

class PostFacebookUseCase:
    @log_method(logger)
    def __init__(self, facebook_gateway: FacebookGateway):
        """
        Initialize the use case with a Facebook gateway.

        Args:
            facebook_gateway (FacebookGateway): The gateway to interact with Facebook
        """
        self.facebook_gateway = facebook_gateway
        logger.debug(f"PostFacebookUseCase initialized with {facebook_gateway.__class__.__name__}")

    @log_method(logger)
    def execute(self, publication_text: str, privacy: str = "PUBLIC"):
        """
        Execute the use case to post content to Facebook.

        Args:
            publication_text (str): The text content to post
            privacy (str): Privacy setting for the post ("PUBLIC", "FRIENDS", "ONLY_ME")

        Returns:
            dict: Response from the Facebook API containing the post data

        Raises:
            AutomatorError: If there's an error during execution
        """
        try:
            logger.debug(f"Creating FacebookPublication entity with text: {publication_text[:20]}...")
            publication = FacebookPublication(publication_text, privacy)
            logger.debug("FacebookPublication entity created")

            logger.debug("Posting to Facebook via FacebookGateway")
            result = self.facebook_gateway.post(publication)
            logger.debug(f"Facebook post created, result: {result}")

            return result
        except Exception as e:
            logger.error(f"Error in PostFacebookUseCase: {str(e)}")
            raise AutomatorError(f"Failed to post to Facebook: {str(e)}")