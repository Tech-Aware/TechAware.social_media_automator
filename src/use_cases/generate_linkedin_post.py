import random

from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.prompting.prompt_builder import PromptBuilder
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError, OpenAIError, LinkedInGenerationError


class GenerateLinkedInPostUseCase:
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
            logger.debug(f"GenerateLinkedInPostUseCase initialized with {openai_gateway.__class__.__name__}")
        except Exception as e:
            logger.error(f"Failed to initialize LinkedIn post generator: {str(e)}")
            raise LinkedInGenerationError(f"Initialization failed: {str(e)}")

    @log_method(logger)
    def execute(self) -> str:
        """
        Execute the use case to generate LinkedIn post content.

        Returns:
            str: The generated LinkedIn post content

        Raises:
            LinkedInGenerationError: If post generation fails
        """
        try:
            topic_category = ['business', 'developer', 'slides']
            random_topic = random.choice(topic_category)
            self.prompt_builder.reset()

            # Configure and build the prompt
            prompt = (self.prompt_builder
                      .set_platform_and_topic_category('linkedin', random_topic)
                      .add_custom_instructions(
                "Focus on professional insights and industry expertise. "
                "Include specific achievements or metrics when possible. "
                "Maintain a thought leadership tone suitable for LinkedIn's professional audience."
            )
                      .build())

            # Log the prompt for debugging
            logger.debug(f"Generated prompt: {prompt}")

            # Generate the post using the OpenAI gateway
            post_content = self.openai_gateway.generate(prompt)
            return post_content
        except OpenAIError as e:
            raise LinkedInGenerationError(f"Error generating LinkedIn post: {str(e)}")
        except Exception as e:
            raise LinkedInGenerationError(f"Unexpected error generating LinkedIn post: {str(e)}")