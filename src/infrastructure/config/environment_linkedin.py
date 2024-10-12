# src/infrastructure/config/environment_linkedin.py

"""
This module handles the loading and management of LinkedIn-specific environment variables
for the application. It provides functions to load variables from a .env file
and retrieve LinkedIn API credentials, ensuring secure and centralized
configuration management for LinkedIn-related settings.
"""

import os
from dotenv import load_dotenv
from src.infrastructure.logging.logger import logger
from src.domain.exceptions import ConfigurationError


def get_linkedin_credentials():
    load_dotenv()

    credentials = {
        "client_id": os.getenv('LINKEDIN_CLIENT_ID'),
        "client_secret": os.getenv('LINKEDIN_CLIENT_SECRET'),
        "access_token": os.getenv('LINKEDIN_ACCESS_TOKEN'),
        "user_id": os.getenv('LINKEDIN_USER_ID')
    }

    for key, value in credentials.items():
        if not value:
            logger.error(f"Environment variable LINKEDIN_{key.upper()} is not set")
            raise ConfigurationError(f"Missing environment variable: LINKEDIN_{key.upper()}")

    logger.success("LinkedIn credentials loaded successfully")
    return credentials