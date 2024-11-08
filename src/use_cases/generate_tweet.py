# src/use_cases/generate_tweet.py

import random

from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.prompting.prompt_builder import PromptBuilder
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError, OpenAIError, TweetGenerationError


class GenerateTweetUseCase:
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
            logger.debug(f"GenerateTweetUseCase initialized with {openai_gateway.__class__.__name__}")
        except Exception as e:
            logger.error(f"Failed to initialize tweet generator: {str(e)}")
            raise TweetGenerationError(f"Initialization failed: {str(e)}")

    @log_method(logger)
    def execute(self) -> str:
        """
        Execute the use case to generate tweet content.

        Returns:
            str: The generated tweet content

        Raises:
            TweetGenerationError: If tweet generation fails
        """
        try:
            topic_category = ['business', 'developer', 'slides']
            random_topic = random.choice(topic_category)
            # Reset any previous configuration
            self.prompt_builder.reset()

            # Configure and build the prompt
            prompt = (self.prompt_builder
                      .set_platform_and_topic_category('twitter', random_topic)
                      .add_custom_instructions(
                "Ensure the tweet is attention-grabbing and concise. "
                "Maximum 250 characters including hashtags. "
                "Include 2-3 relevant hashtags and make every word count. "
                "Focus on immediate value and shareability."
            )
                      .build())

            logger.debug("Prompt built successfully, generating tweet")

            # Generate the tweet using OpenAI
            generated_tweet = self.openai_gateway.generate(prompt)
            logger.debug(f"Tweet generated successfully: {generated_tweet}")

            # Vérifier la longueur du tweet
            if len(generated_tweet) > 280:
                logger.warning(f"Generated tweet exceeds 250 characters ({len(generated_tweet)}), retrying...")
                return self.execute()  # Recursive retry

            return generated_tweet

        except OpenAIError as e:
            logger.error(f"OpenAI error in GenerateTweetUseCase: {str(e)}")
            raise TweetGenerationError(f"Error generating tweet: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in GenerateTweetUseCase: {str(e)}")
            raise TweetGenerationError(f"Unexpected error generating tweet: {str(e)}")
