# Location: tests/domain/entities/test_facebook_publication.py

"""
This module contains unit tests for the FacebookPublication entity.
It verifies the correct functionality of creation, validation,
and methods of the FacebookPublication entity.

Test cases cover:
- Publication creation
- Text validation
- Privacy settings validation
- Getters and setters
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

from src.domain.entities.facebook_publication import FacebookPublication
from src.domain.exceptions import ValidationError


class TestFacebookPublication:
    def test_publication_creation_default_privacy(self):
        """
        Test creating a FacebookPublication with default privacy setting.
        """
        text = "This is a valid Facebook publication"
        publication = FacebookPublication(text)
        assert publication.get_text() == text
        assert publication.get_privacy() == "PUBLIC"

    def test_publication_creation_custom_privacy(self):
        """
        Test creating a FacebookPublication with custom privacy setting.
        """
        text = "This is a private Facebook publication"
        publication = FacebookPublication(text, privacy="FRIENDS")
        assert publication.get_text() == text
        assert publication.get_privacy() == "FRIENDS"

    @pytest.mark.parametrize("invalid_text", [
        None,
        123,
        ["text"],
        {"text": "content"}
    ])
    def test_publication_creation_invalid_text_type(self, invalid_text: Any):
        """
        Test creation fails with invalid text type.

        Args:
            invalid_text: Various invalid text inputs
        """
        with pytest.raises(TypeError) as exc_info:
            FacebookPublication(invalid_text)
        assert "Publication text must be a string" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_privacy", [
        None,
        123,
        ["PUBLIC"],
        {"privacy": "PUBLIC"}
    ])
    def test_publication_creation_invalid_privacy_type(self, invalid_privacy: Any):
        """
        Test creation fails with invalid privacy type.

        Args:
            invalid_privacy: Various invalid privacy inputs
        """
        with pytest.raises(TypeError) as exc_info:
            FacebookPublication("Valid text", privacy=invalid_privacy)
        assert "Privacy setting must be a string" in str(exc_info.value)

    def test_publication_validation_valid(self):
        """
        Test validation of a valid Facebook publication.
        """
        publication = FacebookPublication("A valid Facebook publication")
        publication.validate()  # Should not raise any exception

    def test_publication_validation_empty(self):
        """
        Test validation fails with empty text.
        """
        with pytest.raises(ValidationError) as exc_info:
            FacebookPublication("")
        assert "Facebook publication text cannot be empty" in str(exc_info.value)

    def test_publication_validation_whitespace(self):
        """
        Test validation fails with whitespace-only text.
        """
        with pytest.raises(ValidationError) as exc_info:
            FacebookPublication("   ")
        assert "Facebook publication text cannot be empty" in str(exc_info.value)

    def test_publication_validation_too_long(self):
        """
        Test validation fails with text exceeding maximum length.
        """
        long_text = "x" * 63207  # Facebook's limit is 63,206 characters
        with pytest.raises(ValidationError) as exc_info:
            FacebookPublication(long_text)
        assert "Facebook publication text must be 63,206 characters or less" in str(exc_info.value)

    def test_publication_get_text_success(self):
        """
        Test successful retrieval of publication text.
        """
        publication = FacebookPublication("Test text")
        assert publication.get_text() == "Test text"

    def test_publication_get_privacy_success(self):
        """
        Test successful retrieval of privacy setting.
        """
        publication = FacebookPublication("Test text", privacy="FRIENDS")
        assert publication.get_privacy() == "FRIENDS"

    def test_publication_set_text_valid(self):
        """
        Test setting valid text after creation.
        """
        publication = FacebookPublication("Initial text")
        new_text = "Updated text"
        publication.set_text(new_text)
        assert publication.get_text() == new_text

    def test_publication_set_text_invalid_type(self):
        """
        Test setting invalid text type after creation.
        """
        publication = FacebookPublication("Initial text")
        with pytest.raises(TypeError) as exc_info:
            publication.set_text(123)  # type: ignore
        assert "New text must be a string" in str(exc_info.value)

    def test_publication_set_text_empty(self):
        """
        Test setting empty text after creation.
        """
        publication = FacebookPublication("Initial text")
        with pytest.raises(ValidationError) as exc_info:
            publication.set_text("")
        assert "Facebook publication text cannot be empty" in str(exc_info.value)

    def test_publication_set_privacy_valid(self):
        """
        Test setting valid privacy setting after creation.
        """
        publication = FacebookPublication("Test text")
        publication.set_privacy("FRIENDS")
        assert publication.get_privacy() == "FRIENDS"

    def test_publication_set_privacy_invalid_type(self):
        """
        Test setting invalid privacy type after creation.
        """
        publication = FacebookPublication("Test text")
        with pytest.raises(TypeError) as exc_info:
            publication.set_privacy(123)  # type: ignore
        assert "New privacy setting must be a string" in str(exc_info.value)

    def test_publication_set_privacy_invalid_value(self):
        """
        Test setting invalid privacy value after creation.
        """
        publication = FacebookPublication("Test text")
        with pytest.raises(ValidationError) as exc_info:
            publication.set_privacy("INVALID")
        assert "Invalid privacy setting" in str(exc_info.value)

    def test_publication_privacy_case_insensitive(self):
        """
        Test privacy setting is case insensitive.
        """
        publication = FacebookPublication("Test text", privacy="friends")
        assert publication.get_privacy() == "FRIENDS"

    def test_publication_maximum_length(self):
        """
        Test publication with maximum allowed length.
        """
        text = "x" * 63206  # Maximum allowed length
        publication = FacebookPublication(text)
        assert len(publication.get_text()) == 63206

    @pytest.mark.parametrize("privacy", ["PUBLIC", "FRIENDS", "ONLY_ME"])
    def test_publication_valid_privacy_values(self, privacy: str):
        """
        Test all valid privacy settings.

        Args:
            privacy: The privacy setting to test
        """
        publication = FacebookPublication("Test text", privacy=privacy)
        assert publication.get_privacy() == privacy

    def test_publication_attribute_corruption(self):
        """
        Test validation when attributes are corrupted or missing.
        """
        publication = FacebookPublication("Test text")
        delattr(publication, 'text')  # Simulate corrupted state

        with pytest.raises(AttributeError) as exc_info:
            publication.validate()
        assert "Publication text is missing" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main(["-v", __file__])