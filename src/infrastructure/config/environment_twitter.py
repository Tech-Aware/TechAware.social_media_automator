# src/infrastructure/config/environment_twitter.py

"""
This module handles the loading and management of Twitter-specific environment variables
for the application. It provides functions to load variables from a .env file
and retrieve Twitter API credentials, ensuring secure and centralized
configuration management for Twitter-related settings.
"""

import os
import dotenv
from src.infrastructure.logging.logger import logger
from src.domain.exceptions import ConfigurationError

def load_environment_variables():
    """
    Load environment variables from a .env file if it exists.
    """
    if not dotenv.load_dotenv():
        logger.warning(".env file not found or empty")

def get_twitter_credentials():
    """
    Retrieve the Twitter API credentials from environment variables.

    Returns:
        dict: A dictionary containing the Twitter API credentials.

    Raises:
        ConfigurationError: If any of the required environment variables are not set.
    """
    load_environment_variables()
    variables = ["CONSUMER_KEY", "CONSUMER_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]
    credentials = {}

    for var in variables:
        value = os.getenv(var)
        if not value:
            logger.error(f"Environment variable {var} is not set")
            raise ConfigurationError(f"Missing environment variable: {var}")
        credentials[var.lower()] = value

    logger.success("All Twitter credentials loaded successfully")
    return credentials