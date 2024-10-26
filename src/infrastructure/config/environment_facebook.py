# Location: src/infrastructure/config/environment_facebook.py

"""
This module handles the loading and management of Facebook-specific environment variables
for the application. It provides functions to load variables from a .env file
and retrieve Facebook API credentials, ensuring secure and centralized
configuration management for Facebook-related settings.
"""

import os
from dotenv import load_dotenv
from src.infrastructure.logging.logger import logger
from src.domain.exceptions import ConfigurationError

def get_facebook_credentials():
    """
    Retrieve the Facebook API credentials from environment variables.

    Returns:
        dict: A dictionary containing the Facebook API credentials

    Raises:
        ConfigurationError: If any required environment variable is missing
    """
    load_dotenv()

    required_vars = {
        'FACEBOOK_APP_ID': 'app_id',
        'FACEBOOK_APP_SECRET': 'app_secret',
        'FACEBOOK_ACCESS_TOKEN': 'access_token',
        'FACEBOOK_PAGE_ID': 'page_id'
    }

    credentials = {}

    for env_var, cred_key in required_vars.items():
        value = os.getenv(env_var)
        if not value:
            logger.error(f"Environment variable {env_var} is not set")
            raise ConfigurationError(f"Missing environment variable: {env_var}")
        credentials[cred_key] = value

    logger.success("Facebook credentials loaded successfully")
    return credentials