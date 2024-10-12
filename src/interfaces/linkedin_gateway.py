# src/interfaces/linkedin_gateway.py

"""
This module defines the LinkedInGateway abstract base class, which serves as
an interface for interacting with the LinkedIn API. It provides a contract
for implementing concrete LinkedIn API interaction classes.
"""

from abc import ABC, abstractmethod
from src.domain.entities.linkedin_publication import LinkedInPublication


class LinkedInGateway(ABC):
    @abstractmethod
    def post(self, publication: LinkedInPublication):
        """
        Post a publication to LinkedIn.

        Args:
            publication (LinkedInPublication): The LinkedIn publication entity to be posted.

        Returns:
            dict: The response from the LinkedIn API containing the posted publication's data.

        Raises:
            LinkedInError: If there's an error posting the publication to LinkedIn.
        """
        pass