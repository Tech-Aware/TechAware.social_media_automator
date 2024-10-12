# Location: src/infrastructure/external/linkedin_api.py

"""
This module implements the LinkedInAPI class, which serves as a concrete
implementation of the LinkedInGateway interface. It handles the actual
communication with the LinkedIn API, including authentication and publication creation.
"""

import requests
from src.interfaces.linkedin_gateway import LinkedInGateway
from src.domain.entities.linkedin_publication import LinkedInPublication
from src.infrastructure.logging.logger import logger, log_method
from src.infrastructure.config.environment import get_linkedin_credentials
from src.domain.exceptions import LinkedInError, ConfigurationError

class LinkedInAPI(LinkedInGateway):
    @log_method(logger)
    def __init__(self):
        try:
            logger.debug("Loading LinkedIn credentials")
            self.credentials = get_linkedin_credentials()
            logger.debug("LinkedIn credentials loaded successfully")
        except ConfigurationError as e:
            logger.error(f"Failed to initialize LinkedIn API: {str(e)}")
            raise

    @log_method(logger)
    def post(self, publication: LinkedInPublication):
        try:
            logger.debug(f"Validating LinkedIn publication: {publication.get_text()[:20]}...")
            publication.validate()
            logger.debug("LinkedIn publication validation passed")

            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'Authorization': f'Bearer {self.credentials["access_token"]}',
                'Content-Type': 'application/json',
            }

            payload = self._create_payload(publication)
            logger.debug(f"Prepared payload: {payload}")

            logger.debug("Sending request to LinkedIn API")
            response = requests.post(
                'https://api.linkedin.com/v2/ugcPosts',
                headers=headers,
                json=payload
            )
            logger.debug(f"API response status code: {response.status_code}")

            if response.status_code != 201:
                logger.error(f"LinkedIn API error: {response.status_code} - {response.text}")
                raise LinkedInError(f"LinkedIn API error: {response.status_code} - {response.text}")

            response_json = response.json()
            logger.debug(f"API response content: {response_json}")

            return response_json
        except requests.RequestException as e:
            logger.error(f"Network error when posting to LinkedIn: {str(e)}")
            raise LinkedInError(f"Network error when posting to LinkedIn: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when posting to LinkedIn: {str(e)}")
            raise LinkedInError(f"Unexpected error when posting to LinkedIn: {str(e)}")

    def _create_payload(self, publication: LinkedInPublication):

        payload = {
            "author": f"urn:li:organization:{self.credentials['user_id']}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": publication.get_text()
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        return payload