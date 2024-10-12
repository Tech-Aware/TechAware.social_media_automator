# Location: tests/interfaces/test_linkedin_gateway.py

"""
This module contains unit tests for the LinkedInGateway interface.
It verifies that the interface is correctly defined and that concrete implementations
can be created and used as expected.
"""

import sys
import os
import pytest

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.interfaces.linkedin_gateway import LinkedInGateway
from src.domain.entities.linkedin_publication import LinkedInPublication
from src.domain.exceptions import LinkedInError


def test_linkedin_gateway_is_abstract():
    """
    Test that LinkedInGateway cannot be instantiated directly as it is an abstract base class.
    """
    with pytest.raises(TypeError):
        LinkedInGateway()


def test_linkedin_gateway_post_method():
    """
    Test that LinkedInGateway has a post method and that it can be implemented
    in a concrete subclass.
    """
    assert hasattr(LinkedInGateway, 'post')

    class ConcreteLinkedInGateway(LinkedInGateway):
        def post(self, publication: LinkedInPublication):
            return {"id": "123456", "text": publication.get_text()}

    gateway = ConcreteLinkedInGateway()
    assert callable(gateway.post)
    publication = LinkedInPublication("Test LinkedIn post")
    result = gateway.post(publication)
    assert isinstance(result, dict)
    assert "id" in result
    assert "text" in result


def test_linkedin_gateway_post_raises_error():
    """
    Test that a concrete implementation of LinkedInGateway can raise a LinkedInError
    when post encounters an error.
    """
    class ErrorLinkedInGateway(LinkedInGateway):
        def post(self, publication: LinkedInPublication):
            raise LinkedInError("Test error")

    gateway = ErrorLinkedInGateway()
    publication = LinkedInPublication("Test LinkedIn post")
    with pytest.raises(LinkedInError):
        gateway.post(publication)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
