import openai
import re
import random
import PyPDF2
import os
from openai import OpenAI
from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.logging.logger import logger, log_method
from src.infrastructure.config.environment import initialize_environment, get_openai_credentials
from src.domain.exceptions import OpenAIError, ConfigurationError, TweetGenerationError
from src.infrastructure.prompting.prompt_builder import PromptBuilder


class OpenAIAPI(OpenAIGateway):
    @log_method(logger)
    def __init__(self):
        try:
            logger.debug("Initializing environment")
            if not initialize_environment():
                raise ConfigurationError("Failed to initialize environment")

            logger.debug("Loading OpenAI credentials")
            credentials = get_openai_credentials()

            # Debug pour voir la clé récupérée
            api_key = credentials['api_key']
            logger.debug(f"Received API key starting with: {api_key[:10]}...")

            self.client = OpenAI(api_key=api_key)
            self.prompt_builder = PromptBuilder()
            logger.debug("OpenAI client initialized successfully")
        except ConfigurationError as e:
            logger.error(f"Failed to initialize OpenAI API: {str(e)}")
            raise

    @log_method(logger)
    def generate(self, prompt: str) -> str:
        """
        Generate content using OpenAI's API.

        Args:
            prompt (str): The generation prompt containing platform and context information

        Returns:
            str: The generated content

        Raises:
            OpenAIError: If generation fails
        """
        try:
            logger.debug(f"Generating content with prompt")
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": prompt}
                ]
            )
            generated_content = response.choices[0].message.content.strip()

            # Verify if content was generated
            if not generated_content:
                logger.error("Generated content is empty")
                raise OpenAIError("Generated content is empty")

            # Extract content from social_media_post tags
            match = re.search(r"<social_media_post>(.*?)</social_media_post>",
                            generated_content, re.DOTALL)
            if not match:
                logger.error("Could not find social_media_post tags in generated content")
                raise OpenAIError("Generated content does not contain social_media_post tags")

            # Clean up the content
            final_content = match.group(1).strip()
            final_content = re.sub(r"\*\*", "", final_content)
            final_content = final_content.strip('.')

            logger.debug(f"Content generated successfully: {final_content[:100]}...")
            return final_content

        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise OpenAIError(f"Content generation failed: {str(e)}")
