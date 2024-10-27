# Location: src/infrastructure/external/facebook_api.py

"""
This module implements the FacebookAPI class with extensive debugging
and token type verification.
"""

import requests
from src.interfaces.facebook_gateway import FacebookGateway
from src.domain.entities.facebook_publication import FacebookPublication
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import FacebookError
import os


class FacebookAPI(FacebookGateway):
    BASE_URL = "https://graph.facebook.com/v19.0"
    PAGE_ID = "276164198921949"

    @log_method(logger)
    def __init__(self):
        """
        Initialize the FacebookAPI with token verification.
        """
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if not self.access_token:
            raise FacebookError("Facebook access token not found in environment variables (FACEBOOK_ACCESS_TOKEN)")

        # Verify the token and get page access token
        self.access_token = self._get_page_access_token()
        logger.debug("Facebook credentials loaded and verified successfully")

    def _get_page_access_token(self):
        """
        Get a page access token from the user access token.
        """
        try:
            logger.debug("Attempting to get page access token")
            url = f"{self.BASE_URL}/{self.PAGE_ID}"
            params = {
                'fields': 'access_token',
                'access_token': self.access_token
            }

            logger.debug(f"Making request to: {url}")
            response = requests.get(url, params=params)
            logger.debug(f"Token exchange response status: {response.status_code}")
            logger.debug(f"Token exchange response: {response.text}")

            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    logger.debug("Successfully retrieved page access token")
                    return data['access_token']
                else:
                    logger.warning("No access_token in response, using user token")
                    return self.access_token
            else:
                logger.warning(f"Failed to get page token: {response.text}. Using user token.")
                return self.access_token

        except Exception as e:
            logger.warning(f"Error getting page token: {e}. Using user token.")
            return self.access_token

    @log_method(logger)
    def post(self, publication: FacebookPublication):
        """
        Post a publication to Facebook with enhanced debugging.
        """
        try:
            logger.debug(f"Validating publication: {publication.get_text()[:20]}...")
            publication.validate()
            logger.debug("Publication validation passed")

            # First, verify page access
            verify_url = f"{self.BASE_URL}/{self.PAGE_ID}/feed"
            logger.debug(f"Verifying page access with URL: {verify_url}")

            # Complete payload
            payload = {
                'message': publication.get_text(),
                'access_token': self.access_token
            }

            logger.debug("Payload prepared (excluding access_token):")
            logger.debug(f"message: {payload['message'][:50]}...")

            # Attempt to post
            logger.debug("Sending POST request to Facebook")
            response = requests.post(verify_url, data=payload)
            logger.debug(f"Response Status Code: {response.status_code}")
            logger.debug(f"Response Headers: {dict(response.headers)}")
            logger.debug(f"Response Content: {response.text}")

            response_json = response.json()

            if 'error' in response_json:
                error_detail = response_json['error']
                error_msg = (
                    f"Facebook API error:\n"
                    f"Code: {error_detail.get('code', 'N/A')}\n"
                    f"Type: {error_detail.get('type', 'N/A')}\n"
                    f"Message: {error_detail.get('message', 'N/A')}"
                )
                logger.error(error_msg)
                raise FacebookError(error_msg)

            logger.success(f"Successfully posted to Facebook. Post ID: {response_json.get('id')}")
            return response_json

        except requests.exceptions.RequestException as e:
            error_msg = f"Network error posting to Facebook: {str(e)}"
            logger.error(error_msg)
            raise FacebookError(error_msg)
        except Exception as e:
            error_msg = f"Error posting to Facebook: {str(e)}"
            logger.error(error_msg)
            raise FacebookError(error_msg) from e