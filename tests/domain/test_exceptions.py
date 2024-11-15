# Location: tests/domain/test_exceptions.py

"""
This module contains unit tests for the custom exceptions
defined in the src.domain.exceptions module.

It verifies that each type of exception can be raised correctly and
tests the exception inheritance hierarchy to ensure they are properly structured.
"""

import pytest
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.domain.exceptions import (
    AutomatorError,
    TwitterError,
    OpenAIError,
    TweetGenerationError,
    ConfigurationError,
    ValidationError,
    LinkedInError,
    FacebookError,
    OdooError,
    OdooConnectionError,
    OdooAuthenticationError,
    OdooValidationError,
    OdooPublicationError
)


def test_automator_error():
    with pytest.raises(AutomatorError):
        raise AutomatorError("Test AutomatorError")


def test_twitter_error():
    with pytest.raises(TwitterError):
        raise TwitterError("Test TwitterError")


def test_openai_error():
    with pytest.raises(OpenAIError):
        raise OpenAIError("Test OpenAIError")


def test_tweet_generation_error():
    with pytest.raises(TweetGenerationError):
        raise TweetGenerationError("Test TweetGenerationError")


def test_configuration_error():
    with pytest.raises(ConfigurationError):
        raise ConfigurationError("Test ConfigurationError")


def test_validation_error():
    with pytest.raises(ValidationError):
        raise ValidationError("Test ValidationError")


def test_linkedin_error():
    with pytest.raises(LinkedInError):
        raise LinkedInError("Test LinkedInError")


def test_facebook_error():
    with pytest.raises(FacebookError):
        raise FacebookError("Test FacebookError")


def test_odoo_error():
    with pytest.raises(OdooError):
        raise OdooError("Test OdooError")


def test_odoo_connection_error():
    with pytest.raises(OdooConnectionError):
        raise OdooConnectionError("Test OdooConnectionError")


def test_odoo_authentication_error():
    with pytest.raises(OdooAuthenticationError):
        raise OdooAuthenticationError("Test OdooAuthenticationError")


def test_odoo_validation_error():
    with pytest.raises(OdooValidationError):
        raise OdooValidationError("Test OdooValidationError")


def test_odoo_publication_error():
    with pytest.raises(OdooPublicationError):
        raise OdooPublicationError("Test OdooPublicationError")


def test_error_inheritance():
    assert issubclass(TwitterError, AutomatorError)
    assert issubclass(OpenAIError, AutomatorError)
    assert issubclass(TweetGenerationError, OpenAIError)
    assert issubclass(ConfigurationError, AutomatorError)
    assert issubclass(ValidationError, AutomatorError)
    assert issubclass(LinkedInError, AutomatorError)
    assert issubclass(FacebookError, AutomatorError)
    # Test Odoo exceptions hierarchy
    assert issubclass(OdooError, AutomatorError)
    assert issubclass(OdooConnectionError, OdooError)
    assert issubclass(OdooAuthenticationError, OdooError)
    assert issubclass(OdooValidationError, OdooError)
    assert issubclass(OdooPublicationError, OdooError)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])