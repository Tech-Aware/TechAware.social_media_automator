# src/use_cases/post_linkedin.py

"""
This module implements the PostLinkedInUseCase class, which encapsulates the
business logic for posting on LinkedIn. It coordinates between the domain entities
and the LinkedIn gateway to execute the posting process.
"""

from src.domain.entities.linkedin_publication import LinkedInPublication
from src.interfaces.linkedin_gateway import LinkedInGateway
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError


class PostLinkedInUseCase:
    @log_method(logger)
    def __init__(self, linkedin_gateway: LinkedInGateway):
        self.linkedin_gateway = linkedin_gateway
        logger.debug(f"PostLinkedInUseCase initialized with {linkedin_gateway.__class__.__name__}")

    @log_method(logger)
    def execute(self, post_text: str):
        try:
            logger.debug(f"Creating LinkedInPost entity with text: {post_text[:20]}...")
            linkedin_post = LinkedInPublication(post_text)
            logger.debug("LinkedInPost entity created")

            logger.debug("Posting to LinkedIn via LinkedInGateway")
            result = self.linkedin_gateway.post(linkedin_post)
            logger.debug(f"LinkedIn post created, result: {result}")

            return result
        except AutomatorError as e:
            logger.error(f"Error in PostLinkedInUseCase: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in PostLinkedInUseCase: {str(e)}")
            raise AutomatorError(f"Unexpected error: {str(e)}")