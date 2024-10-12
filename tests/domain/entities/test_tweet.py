# tests/domain/entities/test_tweet.py

"""
Ce module contient les tests unitaires pour l'entité Tweet.
Il vérifie le bon fonctionnement de la création, de la validation
et des méthodes de l'entité Tweet.
"""

import sys
import os
import pytest


# Ajoute le répertoire racine du projet au chemin d'importation
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from src.domain.entities.tweet import Tweet
from src.domain.exceptions import ValidationError


def test_tweet_creation():
    """
    Teste la création d'un objet Tweet avec un texte valide.
    Vérifie que l'objet est correctement initialisé avec le texte fourni.
    """
    text = "This is a valid tweet"
    tweet = Tweet(text)
    assert tweet.get_text() == text


def test_tweet_validation_valid():
    """
    Teste la validation d'un tweet valide.
    Vérifie qu'aucune exception n'est levée pour un tweet de longueur acceptable.
    """
    tweet = Tweet("A valid tweet with an acceptable length")
    try:
        tweet.validate()
    except ValidationError:
        pytest.fail("ValidationError was raised unexpectedly")


def test_tweet_validation_empty():
    """
    Teste la validation d'un tweet vide.
    Vérifie qu'une ValidationError est levée pour un tweet sans texte.
    """
    tweet = Tweet("")
    with pytest.raises(ValidationError, match="Tweet cannot be empty"):
        tweet.validate()


def test_tweet_validation_too_long():
    """
    Teste la validation d'un tweet trop long.
    Vérifie qu'une ValidationError est levée pour un tweet dépassant 280 caractères.
    """
    long_text = "x" * 281
    tweet = Tweet(long_text)
    with pytest.raises(ValidationError, match="Tweet must be 280 characters or less"):
        tweet.validate()


def test_tweet_set_text_valid():
    """
    Teste la méthode set_text avec un texte valide.
    Vérifie que le texte du tweet est correctement mis à jour.
    """
    tweet = Tweet("Initial text")
    new_text = "Updated text"
    tweet.set_text(new_text)
    assert tweet.get_text() == new_text


def test_tweet_set_text_invalid():
    """
    Teste la méthode set_text avec un texte invalide.
    Vérifie qu'une ValidationError est levée lors de la tentative de définir un texte invalide.
    """
    tweet = Tweet("Initial text")
    with pytest.raises(ValidationError):
        tweet.set_text("")


def test_tweet_create_tweet_valid():
    """
    Teste la méthode statique create_tweet avec un texte valide.
    Vérifie qu'un objet Tweet est correctement créé et validé.
    """
    text = "A valid tweet for creation"
    tweet = Tweet.create_tweet(text)
    assert isinstance(tweet, Tweet)
    assert tweet.get_text() == text


def test_tweet_create_tweet_invalid():
    """
    Teste la méthode statique create_tweet avec un texte invalide.
    Vérifie qu'une ValidationError est levée lors de la tentative de création d'un tweet invalide.
    """
    with pytest.raises(ValidationError):
        Tweet.create_tweet("")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
