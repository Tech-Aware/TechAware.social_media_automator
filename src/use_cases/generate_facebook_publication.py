# Location: src/use_cases/generate_facebook_publication.py

"""
This module implements the GenerateFacebookPublicationUseCase class, which encapsulates
the business logic for generating Facebook publications using OpenAI. It handles
the coordination between the OpenAI gateway and publication generation process.
"""
import random

from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.prompting.prompt_builder import PromptBuilder
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError, OpenAIError, FacebookGenerationError


class GenerateFacebookPublicationUseCase:
    @log_method(logger)
    def __init__(self, openai_gateway: OpenAIGateway):
        """
        Initialize the use case with OpenAI gateway and PromptBuilder.

        Args:
            openai_gateway (OpenAIGateway): The gateway to interact with OpenAI
        """
        try:
            self.openai_gateway = openai_gateway
            self.prompt_builder = PromptBuilder()
            logger.debug(f"GenerateFacebookPublicationUseCase initialized with {openai_gateway.__class__.__name__}")
        except Exception as e:
            logger.error(f"Failed to initialize Facebook publication generator: {str(e)}")
            raise FacebookGenerationError(f"Initialization failed: {str(e)}")

    @log_method(logger)
    def execute(self) -> str:
        """
        Execute the use case to generate Facebook publication content.

        Returns:
            str: The generated Facebook publication content

        Raises:
            FacebookGenerationError: If publication generation fails
        """
        try:
            # define topics to choice
            topic_category = ['business', 'developer', 'slides']
            random_topic = random.choice(topic_category)
            # Reset any previous configuration
            self.prompt_builder.reset()

            # Configure and build the prompt
            prompt = (self.prompt_builder
                      .set_platform_and_topic_category('facebook', random_topic)
                      .add_custom_instructions(
                "Ensure the content is engaging and suited for Facebook's algorithm. "
                "Include a mix of storytelling and business value."
            )
                      .build())

            logger.debug("Prompt built successfully, generating Facebook publication")

            # Generate the publication using OpenAI
            generated_publication = self.openai_gateway.generate(prompt)
            logger.debug(f"Facebook publication generated successfully: {generated_publication[:100]}...")

            return generated_publication

        except OpenAIError as e:
            logger.error(f"OpenAI error in GenerateFacebookPublicationUseCase: {str(e)}")
            raise FacebookGenerationError(f"Error generating Facebook publication: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in GenerateFacebookPublicationUseCase: {str(e)}")
            raise FacebookGenerationError(f"Unexpected error generating Facebook publication: {str(e)}")