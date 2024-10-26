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



# Find the class LinkedInError and add the FacebookError class after it
class FacebookError(AutomatorError):
    """Raised when there's an error interacting with Facebook API"""
