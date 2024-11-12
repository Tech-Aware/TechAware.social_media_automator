# Location: src/infrastructure/external/openai_api.py

"""
This module implements the OpenAIAPI class, which serves as a concrete
implementation of the OpenAIGateway interface. It handles the actual
communication with the OpenAI API, including authentication and content generation.

The class provides functionality for:
- Initializing OpenAI client with proper credentials
- Generating content using GPT models
- Processing and cleaning generated content
- Error handling and logging

Key features:
- Secure API key handling
- Robust error handling
- Detailed logging
- Content validation and cleanup
"""

import openai
import re
import random
import os
from openai import OpenAI
from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.logging.logger import logger, log_method
from src.infrastructure.config.environment import initialize_environment, get_openai_credentials
from src.domain.exceptions import OpenAIError, ConfigurationError, TweetGenerationError
from src.infrastructure.prompting.prompt_builder import PromptBuilder


class OpenAIAPI(OpenAIGateway):
    # Définir le modèle comme constante de classe
    GPT_MODEL = "gpt-4-turbo"

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

        This method sends a prompt to the OpenAI API and processes the response.
        It extracts the content from within social_media_post tags, performs
        cleanup operations, and handles any errors that occur during generation.

        Args:
            prompt (str): The generation prompt containing platform and context information

        Returns:
            str: The generated content, cleaned and formatted

        Raises:
            OpenAIError: If content generation fails, response is empty, or content
                        format is invalid
        """
        try:
            logger.debug(f"Generating content with prompt")
            response = self.client.chat.completions.create(
                model=self.GPT_MODEL,  # Utiliser la constante de classe
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