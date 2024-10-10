# tests/domain/test_exceptions.py

"""
Ce module contient les tests unitaires pour les exceptions personnalisées
définies dans le module src.domain.exceptions.

Il vérifie que chaque type d'exception peut être levé correctement et
teste la hiérarchie d'héritage des exceptions pour s'assurer qu'elles
sont correctement structurées.
"""

import pytest
import sys
import os


# Ajoute le répertoire racine du projet au chemin d'importation
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.domain.exceptions import (
    AutomatorError,
    TwitterError,
    OpenAIError,
    TweetGenerationError,
    ConfigurationError,
    ValidationError
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


def test_error_inheritance():
    assert issubclass(TwitterError, AutomatorError)
    assert issubclass(OpenAIError, AutomatorError)
    assert issubclass(TweetGenerationError, OpenAIError)
    assert issubclass(ConfigurationError, AutomatorError)
    assert issubclass(ValidationError, AutomatorError)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

