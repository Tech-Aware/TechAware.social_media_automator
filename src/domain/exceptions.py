# src/domain/exceptions.py

"""
This module defines custom exception classes for the Automator application.
It provides a hierarchy of exceptions to handle various error scenarios
in a structured manner, allowing for more precise error handling and reporting.
"""


class AutomatorError(Exception):
    """Base exception for the Automator application"""


class TwitterError(AutomatorError):
    """Raised when there's an error interacting with Twitter API"""


class OpenAIError(AutomatorError):
    """Raised when there's an error interacting with OpenAI API"""


class TweetGenerationError(OpenAIError):
    """Raised when there's an error generating a tweet using OpenAI"""


class ConfigurationError(AutomatorError):
    """Raised when there's an error in the configuration"""


class ValidationError(AutomatorError):
    """Raised when there's a validation error"""


# New exception for LinkedIn
class LinkedInError(AutomatorError):
    """Raised when there's an error interacting with LinkedIn API"""


class LinkedInGenerationError(OpenAIError):
    """Raised when there's an error generating a linkedIn publication using OpenAI"""


class FacebookGenerationError(OpenAIError):
    """Raised when there's an error generating a linkedIn publication using OpenAI"""


# Find the class LinkedInError and add the FacebookError class after it
class FacebookError(AutomatorError):
    """Raised when there's an error interacting with Facebook API"""


# New Odoo-related exceptions
class OdooError(AutomatorError):
    """Base exception for Odoo-related errors"""

class OdooConnectionError(OdooError):
    """Raised when there's an error connecting to the Odoo server"""

class OdooAuthenticationError(OdooError):
    """Raised when there's an authentication error with Odoo"""

class OdooValidationError(OdooError):
    """Raised when there's a validation error with Odoo data"""

class OdooPublicationError(OdooError):
    """Raised when there's an error publishing content to Odoo"""
