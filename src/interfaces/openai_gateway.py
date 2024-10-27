# src/interfaces/openai_gateway.py

"""
This module defines the OpenAIGateway abstract base class, which serves as
an interface for interacting with the OpenAI API. It provides a contract
for implementing concrete OpenAI API interaction classes, specifically
for generating tweet content.
"""

from abc import ABC, abstractmethod


class OpenAIGateway(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate tweet content based on the given prompt using OpenAI's API.

        Args:
            prompt (str): The input prompt for tweet generation.

        Returns:
            str: The generated tweet content.

        Raises:
            OpenAIError: If there's an error during tweet generation.
        """
        pass