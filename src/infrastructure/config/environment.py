#src/infrastructure/config/environment.py
"""
This module serves as a central point for managing environment variables
across different services in the application. It imports and re-exports
functions for retrieving credentials for various services.
"""

from .environment_twitter import load_environment_variables, get_twitter_credentials
from .environment_openai import get_openai_credentials
from .environment_linkedin import get_linkedin_credentials
from src.infrastructure.logging.logger import logger


def initialize_environment():
    """
    Initialize and load all environment variables.
    This should be called at application startup.
    """
    try:
        logger.debug("Loading environment variables")
        load_environment_variables()
        logger.debug("Environment variables loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load environment variables: {str(e)}")
        return False

# Export the initialization function along with the credential getters
__all__ = [
    'initialize_environment',
    'load_environment_variables',
    'get_twitter_credentials',
    'get_openai_credentials',
    'get_linkedin_credentials'
]