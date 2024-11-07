# Location: tests/domain/entities/scraping/test_content_type.py

"""
This module contains unit tests for the ContentType enum class.
It verifies the correct functionality of content type resolution,
URL path mapping, theme retrieval, and value proposition retrieval.

Test cases cover:
- Enum creation and values
- URL path retrieval
- Key themes retrieval
- Value propositions retrieval
- String conversion
- Error handling and exceptions
- Edge cases
"""

import sys
import os
import pytest
from typing import Any

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from src.domain.entities.scraping.content_type import ContentType
from src.domain.exceptions import ValidationError


class TestContentType:
    def test_enum_values_exist(self):
        """
        Test that all expected ContentType enum values exist.
        """
        assert ContentType.BUSINESS.name == "BUSINESS"
        assert ContentType.DEVELOPER.name == "DEVELOPER"
        assert ContentType.CASE_STUDY.name == "CASE_STUDY"
        assert ContentType.TESTIMONIAL.name == "TESTIMONIAL"
        assert ContentType.BLOG.name == "BLOG"

    def test_url_path_retrieval_success(self):
        """
        Test successful URL path retrieval for each content type.
        """
        assert ContentType.BUSINESS.get_url_path() == "/pour-les-entreprises"
        assert ContentType.DEVELOPER.get_url_path() == "/pour-les-developpeurs"
        assert ContentType.CASE_STUDY.get_url_path() == "/etude-de-cas"
        assert ContentType.TESTIMONIAL.get_url_path() == "/temoignage-satochip"
        assert ContentType.BLOG.get_url_path() == "/blog"

    def test_key_themes_retrieval_success(self):
        """
        Test successful key themes retrieval for each content type.
        """
        business_themes = ContentType.BUSINESS.get_key_themes()
        assert isinstance(business_themes, list)
        assert "cost_reduction" in business_themes
        assert "talent_acquisition" in business_themes
        assert "mentorship" in business_themes

    def test_value_props_retrieval_success(self):
        """
        Test successful value propositions retrieval for each content type.
        """
        business_props = ContentType.BUSINESS.get_value_props()
        assert isinstance(business_props, list)
        assert "70% cost reduction" in business_props
        assert "qualified developers" in business_props

    @pytest.mark.parametrize("input_str, expected_type", [
        ("business", ContentType.BUSINESS),
        ("DEVELOPER", ContentType.DEVELOPER),
        ("case_study", ContentType.CASE_STUDY),
        ("TESTIMONIAL", ContentType.TESTIMONIAL),
        ("Blog", ContentType.BLOG)
    ])
    def test_from_string_valid_inputs(self, input_str: str, expected_type: ContentType):
        """
        Test creation from valid string inputs.

        Args:
            input_str: Input string to convert
            expected_type: Expected ContentType result
        """
        assert ContentType.from_string(input_str) == expected_type

    @pytest.mark.parametrize("invalid_input", [
        "",
        "invalid",
        "unknown",
        "123",
        "not_a_type"
    ])
    def test_from_string_invalid_inputs(self, invalid_input: str):
        """
        Test from_string with invalid inputs.

        Args:
            invalid_input: Invalid string input to test
        """
        with pytest.raises(ValidationError) as exc_info:
            ContentType.from_string(invalid_input)
        assert "Invalid content type string" in str(exc_info.value)
        assert "Valid types are" in str(exc_info.value)

    @pytest.mark.parametrize("content_type, expected_str", [
        (ContentType.BUSINESS, "business"),
        (ContentType.DEVELOPER, "developer"),
        (ContentType.CASE_STUDY, "case_study"),
        (ContentType.TESTIMONIAL, "testimonial"),
        (ContentType.BLOG, "blog")
    ])
    def test_string_representation(self, content_type: ContentType, expected_str: str):
        """
        Test string representation of content types.

        Args:
            content_type: ContentType to test
            expected_str: Expected string representation
        """
        assert str(content_type) == expected_str

    def test_themes_list_independence(self):
        """
        Test that modifying returned themes list doesn't affect original.
        """
        themes1 = ContentType.BUSINESS.get_key_themes()
        themes2 = ContentType.BUSINESS.get_key_themes()

        themes1.append("new_theme")
        assert "new_theme" not in themes2

    def test_value_props_list_independence(self):
        """
        Test that modifying returned value props list doesn't affect original.
        """
        props1 = ContentType.BUSINESS.get_value_props()
        props2 = ContentType.BUSINESS.get_value_props()

        props1.append("new_prop")
        assert "new_prop" not in props2

    def test_enum_immutability(self):
        """
        Test that enum values cannot be modified.
        """
        with pytest.raises(AttributeError):
            ContentType.BUSINESS.name = "CHANGED"

    def test_valid_keys_present(self):
        """
        Test that all enum values have corresponding data in maps.
        """
        for content_type in ContentType:
            assert content_type.get_url_path()
            assert content_type.get_key_themes()
            assert content_type.get_value_props()


if __name__ == "__main__":
    pytest.main(["-v", __file__])