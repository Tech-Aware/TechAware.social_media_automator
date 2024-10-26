# Location: src/infrastructure/external/facebook_api.py

"""
This module implements the FacebookAPI class, which serves as a concrete
implementation of the FacebookGateway interface. It handles the actual
communication with the Facebook API, including authentication and post creation.
"""

import requests
from src.interfaces.facebook_gateway import FacebookGateway
from src.domain.entities.facebook_publication import FacebookPublication
from src.infrastructure.logging.logger import logger, log_method
from src.infrastructure.config.environment_facebook import get_facebook_credentials
from src.domain.exceptions import FacebookError, ConfigurationError


class FacebookAPI(FacebookGateway):
    """
    A concrete implementation of the FacebookGateway interface.
    This class handles authentication and communication with the Facebook API,
    allowing the application to create posts and perform other Facebook-related operations.
    """

    @log_method(logger)
    def __init__(self):
        """
        Initialize the FacebookAPI with the necessary credentials.

        Raises:
            ConfigurationError: If there's an error loading the Facebook credentials
        """
        try:
            logger.debug("Loading Facebook credentials")
            self.credentials = get_facebook_credentials()
            self.base_url = "https://graph.facebook.com/v19.0"
            logger.debug("Facebook credentials loaded successfully")
        except ConfigurationError as e:
            logger.error(f"Failed to initialize Facebook API: {str(e)}")
            raise

    @log_method(logger)
    def post(self, publication: FacebookPublication):
        """
        Post a publication to Facebook.

        Args:
            publication (FacebookPublication): The Facebook publication entity to be posted

        Returns:
            dict: The response from the Facebook API containing the posted publication's data

        Raises:
            FacebookError: If there's an error posting to Facebook
        """
        try:
            logger.debug(f"Validating publication: {publication.get_text()[:20]}...")
            publication.validate()
            logger.debug("Publication validation passed")

            endpoint = f"{self.base_url}/{self.credentials['page_id']}/feed"

            headers = {
                "Authorization": f"Bearer {self.credentials['access_token']}",
                "Content-Type": "application/json"
            }

            payload = {
                "message": publication.get_text(),
                "privacy": {"value": publication.get_privacy().lower()}
            }

            logger.debug(f"Sending request to Facebook API endpoint: {endpoint}")
            response = requests.post(endpoint, json=payload, headers=headers)
            logger.debug(f"API response status code: {response.status_code}")

            response.raise_for_status()
            response_json = response.json()
            logger.debug(f"API response content: {response_json}")

            return response_json
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to post to Facebook: {str(e)}"
            logger.error(error_msg)
            raise FacebookError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error posting to Facebook: {str(e)}"
            logger.error(error_msg)
            raise FacebookError(error_msg)