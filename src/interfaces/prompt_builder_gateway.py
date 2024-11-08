# src/interfaces/prompt_builder_gateway.py

"""
This module defines the PromptBuilderGateway abstract base class, which serves as
an interface for prompt building operations. It provides a contract for implementing
concrete prompt builder classes that generate prompts for different social media platforms.

The interface ensures consistency in how prompts are built across different implementations
while allowing for platform-specific customization.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class PromptBuilderGateway(ABC):
    """
    Abstract base class defining the interface for prompt building operations.
    This interface ensures that any concrete implementation provides the
    necessary methods for building and customizing prompts.
    """

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the builder to its initial state.
        """
        pass

    @abstractmethod
    def select_random_topic(self, category: str) -> Dict:
        """
        Select a random topic from the specified category.

        Args:
            category (str): The topic category to select from

        Returns:
            Dict: The selected topic information

        Raises:
            ValidationError: If category is invalid
        """
        pass

    @abstractmethod
    def set_platform_and_topic_category(self, platform: str, topic_category: str) -> 'PromptBuilderGateway':
        """
        Set the target platform and topic category, and select a random topic.

        Args:
            platform (str): The target social media platform
            topic_category (str): The category of content to generate

        Returns:
            PromptBuilderGateway: The builder instance for method chaining

        Raises:
            ValidationError: If parameters are invalid
            ConfigurationError: If configuration fails
        """
        pass

    @abstractmethod
    def add_custom_instructions(self, instructions: str) -> 'PromptBuilderGateway':
        """
        Add custom instructions to the prompt being built.

        Args:
            instructions (str): Additional instructions to customize the prompt

        Returns:
            PromptBuilderGateway: The builder instance for method chaining

        Raises:
            ValidationError: If instructions are invalid
        """
        pass

    @abstractmethod
    def build(self) -> str:
        """
        Build the final prompt combining all configured elements.

        Returns:
            str: The complete prompt ready for content generation

        Raises:
            ValidationError: If prompt cannot be built
            ConfigurationError: If configuration is incomplete
        """
        pass

    @property
    @abstractmethod
    def platform(self) -> Optional[str]:
        """
        Get the currently configured platform.

        Returns:
            Optional[str]: The platform name, or None if not set
        """
        pass

    @property
    @abstractmethod
    def topic_category(self) -> Optional[str]:
        """
        Get the currently configured topic category.

        Returns:
            Optional[str]: The topic category, or None if not set
        """
        pass

    @property
    @abstractmethod
    def selected_topic(self) -> Optional[Dict]:
        """
        Get the currently selected topic.

        Returns:
            Optional[Dict]: The topic information, or None if not selected
        """
        pass

    @property
    @abstractmethod
    def custom_instructions(self) -> str:
        """
        Get the current custom instructions.

        Returns:
            str: The custom instructions, or empty string if none added
        """
        pass