# tests/infrastructure/prompting/test_prompt_builder.py

"""
This module contains unit tests for the PromptBuilder class, verifying both
its implementation of the PromptBuilderGateway interface and its concrete
functionality for building prompts. Tests include print outputs for manual verification.
"""

import pytest
from unittest.mock import patch
from typing import Dict
from src.infrastructure.prompting.prompt_builder import PromptBuilder
from src.interfaces.prompt_builder_gateway import PromptBuilderGateway
from src.domain.exceptions import ValidationError, ConfigurationError


class TestPromptBuilder:
    @pytest.fixture
    def builder(self) -> PromptBuilderGateway:
        """Provide a fresh PromptBuilder instance for each test."""
        return PromptBuilder()

    def test_implements_gateway_interface(self, builder: PromptBuilderGateway):
        """Test that PromptBuilder correctly implements PromptBuilderGateway."""
        print("\nTest: Implementation of PromptBuilderGateway interface")
        print(f"Builder class: {builder.__class__.__name__}")
        print(f"Implemented methods: {[method for method in dir(builder) if not method.startswith('_')]}")

        assert isinstance(builder, PromptBuilderGateway)
        assert all(hasattr(builder, attr) for attr in ['reset', 'select_random_topic',
                                                       'set_platform_and_topic_category',
                                                       'add_custom_instructions', 'build'])

    def test_initial_state(self, builder: PromptBuilder):
        """Test the initial state of a new PromptBuilder instance."""
        print("\nTest: Initial state of PromptBuilder")
        print(f"Platform: {builder.platform}")
        print(f"Topic category: {builder.topic_category}")
        print(f"Selected topic: {builder.selected_topic}")
        print(f"Custom instructions: '{builder.custom_instructions}'")

        assert builder.platform is None
        assert builder.topic_category is None
        assert builder.selected_topic is None
        assert builder.custom_instructions == ""

    def test_create_twitter_business_prompt(self, builder: PromptBuilder):
        """Test creating a Twitter prompt for business category."""
        prompt = builder.set_platform_and_topic_category('twitter', 'business').build()

        print("\nTest: Twitter Business Prompt Generation")
        print("Generated Prompt:")
        print("-" * 80)
        print(prompt)
        print("-" * 80)
        print(f"Platform: {builder.platform}")
        print(f"Topic category: {builder.topic_category}")
        print(f"Selected topic: {builder.selected_topic['subject']}")

        assert 'Generate a twitter post' in prompt
        assert 'Longueur maximale: 280' in prompt
        # assert 'pour-les-entreprises' in prompt # todo

    def test_create_linkedin_developer_prompt(self, builder: PromptBuilder):
        """Test creating a LinkedIn prompt for developer category."""
        prompt = builder.set_platform_and_topic_category('linkedin', 'developer').build()

        print("\nTest: LinkedIn Developer Prompt Generation")
        print("Generated Prompt:")
        print("-" * 80)
        print(prompt)
        print("-" * 80)
        print(f"Selected topic: {builder.selected_topic['subject']}")

        assert 'Generate a linkedin post' in prompt
        assert 'Longueur maximale: 3000' in prompt
        assert 'pour-les-développeurs' in prompt

    def test_create_facebook_slides_prompt(self, builder: PromptBuilder):
        """Test creating a Facebook prompt for slides category."""
        prompt = builder.set_platform_and_topic_category('facebook', 'slides').build()

        print("\nTest: Facebook Slides Prompt Generation")
        print("Generated Prompt:")
        print("-" * 80)
        print(prompt)
        print("-" * 80)

        assert 'Generate a facebook post' in prompt
        assert 'Longueur maximale: 63206' in prompt
        assert '/slides/' in prompt

    def test_custom_instructions_handling(self, builder: PromptBuilder):
        """Test adding and retrieving custom instructions."""
        test_instructions = "Focus on cost reduction benefits and ROI metrics"

        builder.set_platform_and_topic_category('twitter', 'business')
        builder.add_custom_instructions(test_instructions)
        prompt = builder.build()

        print("\nTest: Custom Instructions Integration")
        print(f"Added instructions: {test_instructions}")
        print("Generated Prompt:")
        print("-" * 80)
        print(prompt)
        print("-" * 80)

        assert builder.custom_instructions == test_instructions
        assert test_instructions in prompt

    @patch('random.choice')
    def test_topic_selection(self, mock_choice, builder: PromptBuilder):
        """Test topic selection mechanism."""
        test_topic = {
            'subject': 'Test Subject',
            'context': 'Test Context',
            'problem': 'Test Problem',
            'solution': 'Test Solution',
            'link': 'https://test.com'
        }
        mock_choice.return_value = test_topic

        print("\nTest: Topic Selection")
        print("Test topic:")
        for key, value in test_topic.items():
            print(f"{key}: {value}")

        selected_topic = builder.select_random_topic('business')
        print("\nSelected topic:")
        for key, value in selected_topic.items():
            print(f"{key}: {value}")

        assert selected_topic == test_topic

    @pytest.mark.parametrize("platform,expected_limit", [
        ('twitter', '280'),
        ('linkedin', '3000'),
        ('facebook', '63206')
    ])
    def test_platform_specific_limits(self, builder: PromptBuilder, platform: str, expected_limit: str):
        """Test that each platform has correct character limits."""
        prompt = builder.set_platform_and_topic_category(platform, 'business').build()

        print(f"\nTest: {platform.capitalize()} Character Limit")
        print(f"Expected limit: {expected_limit} characters")
        print("Generated Prompt:")
        print("-" * 80)
        print(prompt)
        print("-" * 80)

        assert f"Longueur maximale: {expected_limit}" in prompt
        assert builder.platform == platform

    def test_method_chaining(self, builder: PromptBuilder):
        """Test that methods can be chained together."""
        print("\nTest: Method Chaining")
        prompt = (
            builder
            .set_platform_and_topic_category('twitter', 'business')
            .add_custom_instructions("Test chained instructions")
            .build()
        )

        print("Generated Prompt using method chaining:")
        print("-" * 80)
        print(prompt)
        print("-" * 80)

        assert isinstance(prompt, str)
        assert "Test chained instructions" in prompt

    def test_invalid_platform(self, builder: PromptBuilder):
        """Test handling of invalid platform."""
        print("\nTest: Invalid Platform Handling")
        invalid_platform = "invalid_platform"
        print(f"Attempting to use invalid platform: {invalid_platform}")

        with pytest.raises(ValidationError) as exc_info:
            builder.set_platform_and_topic_category(invalid_platform, 'business')

        print(f"Caught expected error: {str(exc_info.value)}")
        assert "Unsupported platform" in str(exc_info.value)

    def test_build_without_configuration(self, builder: PromptBuilder):
        """Test building prompt without required configuration."""
        print("\nTest: Build Without Configuration")
        print("Attempting to build prompt without setting platform and topic...")

        with pytest.raises(ConfigurationError) as exc_info:
            builder.build()

        print(f"Caught expected error: {str(exc_info.value)}")
        assert "Platform and topic must be set" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])