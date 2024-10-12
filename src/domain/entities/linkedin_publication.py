# src/domain/entities/linkedin_publication.py

"""
This module defines the LinkedInPublication entity, representing a LinkedIn publication in the application.
It encapsulates the publication's content and provides validation logic to ensure
the publication conforms to LinkedIn's requirements.
"""

from src.domain.exceptions import ValidationError
from src.infrastructure.logging.logger import logger, log_method


class LinkedInPublication:
    @log_method(logger)
    def __init__(self, text):
        self.text = text
        self.validate()

    @log_method(logger)
    def validate(self):
        if not self.text:
            logger.warning("LinkedIn publication validation failed: Empty text")
            raise ValidationError("LinkedIn publication text cannot be empty")

        if len(self.text) > 3000:
            logger.warning(f"LinkedIn publication validation failed: Text too long ({len(self.text)} characters)")
            raise ValidationError(f"LinkedIn publication text must be 3000 characters or less (current: {len(self.text)})")

    @log_method(logger)
    def get_text(self):
        return self.text