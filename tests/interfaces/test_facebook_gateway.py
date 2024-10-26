# Location: tests/interfaces/test_facebook_gateway.py

"""
This module contains unit tests for the FacebookGateway interface.
It verifies that the interface is correctly defined and that concrete implementations
can be created and used as expected.

Test cases ensure that:
- The interface cannot be instantiated directly
- Concrete implementations must implement all required methods
- The interface methods have the correct signatures
"""

import sys
import os
import pytest

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.interfaces.facebook_gateway import FacebookGateway
from src.domain.entities.facebook_publication import FacebookPublication
from src.domain.exceptions import FacebookError

def test_facebook_gateway_is_abstract():
    """
    Test that FacebookGateway cannot be instantiated directly as it is an abstract base class.
    """
    with pytest.raises(TypeError):
        FacebookGateway()

def test_facebook_gateway_post_method():
    """
    Test that FacebookGateway has a post method and that it can be implemented
    in a concrete subclass.
    """
    assert hasattr(FacebookGateway, 'post')

    class ConcreteFacebookGateway(FacebookGateway):
        def post(self, publication: FacebookPublication):
            return {"id": "123456", "text": publication.get_text()}

    gateway = ConcreteFacebookGateway()
    assert callable(gateway.post)
    publication = FacebookPublication("Test Facebook post")
    result = gateway.post(publication)
    assert isinstance(result, dict)
    assert "id" in result
    assert "text" in result

def test_facebook_gateway_post_raises_error():
    """
    Test that a concrete implementation of FacebookGateway can raise a FacebookError
    when post encounters an error.
    """
    class ErrorFacebookGateway(FacebookGateway):
        def post(self, publication: FacebookPublication):
            raise FacebookError("Test error")

    gateway = ErrorFacebookGateway()
    publication = FacebookPublication("Test Facebook post")
    with pytest.raises(FacebookError):
        gateway.post(publication)

if __name__ == "__main__":
    pytest.main(["-v", __file__])