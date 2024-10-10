# src/interfaces/test_twitter_gateway.py

"""
This module defines the TwitterGateway abstract base class, which serves as
an interface for interacting with the Twitter API. It provides a contract
for implementing concrete Twitter API interaction classes.
"""

from abc import ABC, abstractmethod
from src.domain.entities.tweet import Tweet

class TwitterGateway(ABC):
    @abstractmethod
    def post_tweet(self, tweet: Tweet):
        pass