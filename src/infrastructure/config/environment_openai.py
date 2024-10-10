# src/infrastructure/config/environment_openai.py

import os
from dotenv import load_dotenv
from src.infrastructure.logging.logger import logger
from src.domain.exceptions import ConfigurationError


def get_openai_credentials():
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("Environment variable OPENAI_API_KEY is not set")
        raise ConfigurationError("Missing environment variable: OPENAI_API_KEY")

    logger.success("OpenAI API key loaded successfully")
    return {"api_key": api_key}