# Location: src/use_cases/generate_linkedin_post.py

"""
This module implements the GenerateLinkedInPostUseCase class, which encapsulates
the business logic for generating LinkedIn posts using OpenAI. It handles
the coordination between the OpenAI gateway and post generation process.
"""

from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError, OpenAIError, TweetGenerationError


class GenerateLinkedInPostUseCase:
    @log_method(logger)
    def __init__(self, openai_gateway: OpenAIGateway):
        """
        Initialize the use case with an OpenAI gateway.

        Args:
            openai_gateway (OpenAIGateway): The gateway to interact with OpenAI
        """
        self.openai_gateway = openai_gateway
        logger.debug(f"GenerateLinkedInPostUseCase initialized with {openai_gateway.__class__.__name__}")

    @log_method(logger)
    def execute(self) -> str:
        """
        Execute the use case to generate LinkedIn post content.

        Args:
            prompt (str): The prompt for post generation

        Returns:
            str: The generated LinkedIn post content

        Raises:
            TweetGenerationError: If post generation fails
        """
        try:
            logger.debug(f"Generating Facebook publication")
            linkedin_prompt = (
                "Generate a LinkedIn publication. The publication should be engaging, "
                "conversational, and suitable for a professional audience. "
                "Include relevant emojis where appropriate."
                "output language in french"
                "Include link without any special format, writing it as https://www.webpage.net "
            )
            generated_publication = self.openai_gateway.generate(linkedin_prompt)
            logger.debug(f"Facebook publication generated: {generated_publication}")
            return generated_publication

        except OpenAIError as e:
            logger.error(f"OpenAI error in GenerateFacebookPublicationUseCase: {str(e)}")
            raise TweetGenerationError(f"Error generating Facebook publication: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in GenerateFacebookPublicationUseCase: {str(e)}")
            raise TweetGenerationError(f"Unexpected error generating Facebook publication: {str(e)}")