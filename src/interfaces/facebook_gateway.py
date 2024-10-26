# Location: src/interfaces/facebook_gateway.py

"""
This module defines the FacebookGateway abstract base class, which serves as
an interface for interacting with the Facebook API. It provides a contract
for implementing concrete Facebook API interaction classes.

The interface defines the required methods for Facebook operations,
ensuring consistency across different implementations.
"""

from abc import ABC, abstractmethod
from src.domain.entities.facebook_publication import FacebookPublication


class FacebookGateway(ABC):
    """
    Abstract base class defining the interface for Facebook API interactions.
    This interface ensures that any concrete implementation provides the
    necessary methods for posting content to Facebook.
    """

    @abstractmethod
    def post(self, publication: FacebookPublication):
        """
        Post a publication to Facebook.

        Args:
            publication (FacebookPublication): The Facebook publication entity to be posted

        Returns:
            dict: The response from the Facebook API containing the posted publication's data

        Raises:
            FacebookError: If there's an error posting the publication to Facebook
        """
        pass