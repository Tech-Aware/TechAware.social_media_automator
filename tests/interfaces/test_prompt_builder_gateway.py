# tests/interfaces/test_prompt_builder_gateway.py

"""
This module contains tests for the PromptBuilderGateway interface.
It verifies that the interface is properly defined and that concrete
implementations must implement all required methods.
"""

import pytest
from typing import Dict, Optional
from unittest.mock import Mock
from src.interfaces.prompt_builder_gateway import PromptBuilderGateway
from src.domain.exceptions import ValidationError, ConfigurationError


class TestPromptBuilderGateway:
    class MockPromptBuilder(PromptBuilderGateway):
        """Mock implementation of PromptBuilderGateway for testing."""

        def __init__(self):
            self._platform: Optional[str] = None
            self._topic_category: Optional[str] = None
            self._selected_topic: Optional[Dict] = None
            self._custom_instructions: str = ""

        @property
        def platform(self) -> Optional[str]:
            return self._platform

        @property
        def topic_category(self) -> Optional[str]:
            return self._topic_category

        @property
        def selected_topic(self) -> Optional[Dict]:
            return self._selected_topic

        @property
        def custom_instructions(self) -> str:
            return self._custom_instructions

        def reset(self) -> None:
            print("\nReset called")
            self._platform = None
            self._topic_category = None
            self._selected_topic = None
            self._custom_instructions = ""

        def select_random_topic(self, category: str) -> Dict:
            print(f"\nSelecting random topic for category: {category}")
            topic = {
                'subject': 'Test Subject',
                'context': 'Test Context',
                'problem': 'Test Problem',
                'solution': 'Test Solution',
                'link': 'https://test.com'
            }
            return topic

        def set_platform_and_topic_category(self, platform: str, topic_category: str) -> 'PromptBuilderGateway':
            print(f"\nSetting platform: {platform} and topic category: {topic_category}")
            self._platform = platform
            self._topic_category = topic_category
            self._selected_topic = self.select_random_topic(topic_category)
            return self

        def add_custom_instructions(self, instructions: str) -> 'PromptBuilderGateway':
            print(f"\nAdding custom instructions: {instructions}")
            self._custom_instructions = instructions
            return self

        def build(self) -> str:
            print("\nBuilding prompt")
            if not all([self._platform, self._topic_category, self._selected_topic]):
                raise ConfigurationError("Platform and topic must be set before building prompt")
            return "Test prompt"

    @pytest.fixture
    def gateway(self) -> PromptBuilderGateway:
        """Provide a mock implementation of PromptBuilderGateway for testing."""
        print("\nCreating new MockPromptBuilder instance")
        return TestPromptBuilderGateway.MockPromptBuilder()

    def test_interface_methods_exist(self):
        """Test that all required interface methods are defined."""
        print("\nTest: Verifying interface methods existence")
        required_methods = [
            'reset',
            'select_random_topic',
            'set_platform_and_topic_category',
            'add_custom_instructions',
            'build'
        ]

        required_properties = [
            'platform',
            'topic_category',
            'selected_topic',
            'custom_instructions'
        ]

        # Check methods
        for method in required_methods:
            print(f"Verifying method: {method}")
            assert hasattr(PromptBuilderGateway, method)
            assert callable(getattr(PromptBuilderGateway, method))

        # Check properties
        for prop in required_properties:
            print(f"Verifying property: {prop}")
            assert hasattr(PromptBuilderGateway, prop)

    def test_abstract_class_instantiation(self):
        """Test that PromptBuilderGateway cannot be instantiated directly."""
        print("\nTest: Attempting to instantiate abstract class")
        with pytest.raises(TypeError) as exc_info:
            PromptBuilderGateway()
        print(f"Caught expected error: {str(exc_info.value)}")
        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_concrete_implementation(self, gateway: PromptBuilderGateway):
        """Test that a concrete implementation works correctly."""
        print("\nTest: Concrete implementation functionality")

        # Test initial state
        assert gateway.platform is None
        assert gateway.topic_category is None
        assert gateway.selected_topic is None
        assert gateway.custom_instructions == ""
        print("Initial state verified")

        # Test method chaining and state changes
        result = (gateway
                  .set_platform_and_topic_category('test_platform', 'test_category')
                  .add_custom_instructions('test instructions')
                  .build())

        print(f"Built prompt result: {result}")

        # Verify final state
        assert gateway.platform == 'test_platform'
        assert gateway.topic_category == 'test_category'
        assert isinstance(gateway.selected_topic, dict)
        assert gateway.custom_instructions == 'test instructions'
        print("Final state verified")

    def test_reset_functionality(self, gateway: PromptBuilderGateway):
        """Test that reset properly clears the state."""
        print("\nTest: Reset functionality")

        # Setup initial state
        gateway.set_platform_and_topic_category('test_platform', 'test_category')
        gateway.add_custom_instructions('test instructions')

        print("State before reset:")
        print(f"Platform: {gateway.platform}")
        print(f"Topic category: {gateway.topic_category}")
        print(f"Selected topic: {gateway.selected_topic}")
        print(f"Custom instructions: {gateway.custom_instructions}")

        # Reset
        gateway.reset()

        print("\nState after reset:")
        print(f"Platform: {gateway.platform}")
        print(f"Topic category: {gateway.topic_category}")
        print(f"Selected topic: {gateway.selected_topic}")
        print(f"Custom instructions: {gateway.custom_instructions}")

        # Verify reset state
        assert gateway.platform is None
        assert gateway.topic_category is None
        assert gateway.selected_topic is None
        assert gateway.custom_instructions == ""

    def test_build_without_configuration(self, gateway: PromptBuilderGateway):
        """Test that building without configuration raises appropriate error."""
        print("\nTest: Build without configuration")
        with pytest.raises(ConfigurationError) as exc_info:
            gateway.build()
        print(f"Caught expected error: {str(exc_info.value)}")
        assert "Platform and topic must be set" in str(exc_info.value)

    def test_method_return_types(self, gateway: PromptBuilderGateway):
        """Test that methods return appropriate types."""
        print("\nTest: Method return types")

        print("Testing set_platform_and_topic_category return type")
        result = gateway.set_platform_and_topic_category('test_platform', 'test_category')
        assert isinstance(result, PromptBuilderGateway)

        print("Testing add_custom_instructions return type")
        result = gateway.add_custom_instructions('test')
        assert isinstance(result, PromptBuilderGateway)

        print("Testing select_random_topic return type")
        result = gateway.select_random_topic('test_category')
        assert isinstance(result, dict)

        print("Testing build return type")
        result = gateway.build()
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])