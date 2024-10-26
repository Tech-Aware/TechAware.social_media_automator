# Location: src/domain/entities/facebook_publication.py

"""
This module defines the FacebookPublication entity, which represents a publication
on Facebook. It encapsulates the publication's content and provides validation
logic to ensure the publication conforms to Facebook's requirements.

The entity handles:
- Text content validation
- Length restrictions
- Required fields validation
- Privacy settings
"""

from typing import Optional
from src.domain.exceptions import ValidationError
from src.infrastructure.logging.logger import logger, log_method


class FacebookPublication:
    @log_method(logger)
    def __init__(self, text: str, privacy: str = "PUBLIC"):
        """
        Initialize a new FacebookPublication instance.

        Args:
            text (str): The content of the Facebook publication
            privacy (str): Privacy setting for the post ("PUBLIC", "FRIENDS", "ONLY_ME")

        Raises:
            ValidationError: If the initial text or privacy setting is invalid
            TypeError: If arguments are of incorrect type
        """
        try:
            if not isinstance(text, str):
                error_msg = "Publication text must be a string"
                logger.error(error_msg)
                raise TypeError(error_msg)
            if not isinstance(privacy, str):
                error_msg = "Privacy setting must be a string"
                logger.error(error_msg)
                raise TypeError(error_msg)

            logger.debug(f"Creating FacebookPublication with text: {text[:20]}...")
            self.text = text
            self.privacy = privacy.upper()
            self.validate()
            logger.debug("FacebookPublication created successfully")
        except (TypeError, ValidationError) as e:
            raise type(e)(f"Failed to create Facebook publication: {str(e)}") from e
        except Exception as e:
            raise ValidationError(f"Unexpected error creating Facebook publication: {str(e)}") from e

    @log_method(logger)
    def get_text(self) -> str:
        """
        Get the publication text content.

        Returns:
            str: The text content of the publication

        Raises:
            AttributeError: If text attribute is not set
            ValidationError: If text content is invalid
        """
        try:
            logger.debug("Retrieving Facebook publication text")
            if not hasattr(self, 'text'):
                error_msg = "Publication text has not been set"
                logger.error(error_msg)
                raise AttributeError(error_msg)
            return self.text
        except AttributeError as e:
            raise AttributeError(f"Failed to retrieve publication text: {str(e)}") from e
        except Exception as e:
            raise ValidationError(f"Unexpected error retrieving publication text: {str(e)}") from e

    @log_method(logger)
    def get_privacy(self) -> str:
        """
        Get the publication privacy setting.

        Returns:
            str: The privacy setting of the publication

        Raises:
            AttributeError: If privacy attribute is not set
            ValidationError: If privacy setting is invalid
        """
        try:
            logger.debug("Retrieving Facebook publication privacy setting")
            if not hasattr(self, 'privacy'):
                error_msg = "Publication privacy setting has not been set"
                logger.error(error_msg)
                raise AttributeError(error_msg)
            return self.privacy
        except AttributeError as e:
            raise AttributeError(f"Failed to retrieve privacy setting: {str(e)}") from e
        except Exception as e:
            raise ValidationError(f"Unexpected error retrieving privacy setting: {str(e)}") from e

    @log_method(logger)
    def set_text(self, new_text: str) -> None:
        """
        Update the publication text content.

        Args:
            new_text (str): The new text content

        Raises:
            TypeError: If new_text is not a string
            ValidationError: If the new text is invalid
        """
        try:
            if not isinstance(new_text, str):
                error_msg = "New text must be a string"
                logger.error(error_msg)
                raise TypeError(error_msg)

            logger.debug(f"Setting new Facebook publication text: {new_text[:20]}...")
            self.text = new_text
            self.validate()
            logger.debug("New Facebook publication text set successfully")
        except TypeError as e:
            raise TypeError(f"Invalid text type: {str(e)}") from e
        except ValidationError as e:
            raise ValidationError(f"Text validation failed: {str(e)}") from e
        except Exception as e:
            raise ValidationError(f"Unexpected error setting text: {str(e)}") from e

    @log_method(logger)
    def set_privacy(self, new_privacy: str) -> None:
        """
        Update the publication privacy setting.

        Args:
            new_privacy (str): The new privacy setting

        Raises:
            TypeError: If new_privacy is not a string
            ValidationError: If the new privacy setting is invalid
        """
        try:
            if not isinstance(new_privacy, str):
                error_msg = "New privacy setting must be a string"
                logger.error(error_msg)
                raise TypeError(error_msg)

            logger.debug(f"Setting new Facebook publication privacy: {new_privacy}")
            self.privacy = new_privacy.upper()
            self.validate()
            logger.debug("New Facebook publication privacy set successfully")
        except TypeError as e:
            raise TypeError(f"Invalid privacy type: {str(e)}") from e
        except ValidationError as e:
            raise ValidationError(f"Privacy validation failed: {str(e)}") from e
        except Exception as e:
            raise ValidationError(f"Unexpected error setting privacy: {str(e)}") from e

    @log_method(logger)
    def validate(self) -> None:
        """
        Validate the Facebook publication content.

        Checks:
        - Text is not empty or whitespace
        - Text length is within Facebook's limits (63,206 characters)
        - Privacy setting is valid ("PUBLIC", "FRIENDS", "ONLY_ME")

        Raises:
            AttributeError: If required attributes are missing
            ValidationError: If any validation check fails
            Exception: For any other unexpected validation errors
        """
        try:
            # Check if required attributes exist
            if not hasattr(self, 'text'):
                error_msg = "Publication text is missing"
                logger.error(error_msg)
                raise AttributeError(error_msg)
            if not hasattr(self, 'privacy'):
                error_msg = "Publication privacy setting is missing"
                logger.error(error_msg)
                raise AttributeError(error_msg)

            # Check if text is empty
            if not self.text or self.text.isspace():
                error_msg = "Facebook publication text cannot be empty"
                logger.warning(error_msg)
                raise ValidationError(error_msg)

            # Check text length
            if len(self.text) > 63206:
                error_msg = f"Facebook publication text must be 63,206 characters or less (current: {len(self.text)})"
                logger.warning(error_msg)
                raise ValidationError(error_msg)

            # Validate privacy setting
            valid_privacy_settings = ["PUBLIC", "FRIENDS", "ONLY_ME"]
            if self.privacy not in valid_privacy_settings:
                error_msg = f"Invalid privacy setting. Must be one of: {', '.join(valid_privacy_settings)}"
                logger.warning(error_msg)
                raise ValidationError(error_msg)

            logger.debug("Facebook publication validation passed")
        except (AttributeError, ValidationError) as e:
            raise type(e)(str(e)) from e
        except Exception as e:
            raise ValidationError(f"Unexpected validation error: {str(e)}") from e