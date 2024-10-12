# Location: tests/domain/entities/test_linkedin_publication.py

import pytest
from src.domain.entities.linkedin_publication import LinkedInPublication
from src.domain.exceptions import ValidationError


def test_linkedin_publication_creation():
    """
    Test the creation of a LinkedInPublication object with valid text.
    Verify that the object is correctly initialized with the provided text.
    """
    text = "This is a valid LinkedIn publication"
    publication = LinkedInPublication(text)
    assert publication.get_text() == text


def test_linkedin_publication_validation_valid():
    """
    Test the validation of a valid LinkedIn publication.
    Verify that no exception is raised for a publication with acceptable length.
    """
    publication = LinkedInPublication("A valid LinkedIn publication with acceptable length")
    try:
        publication.validate()
    except ValidationError:
        pytest.fail("ValidationError was raised unexpectedly")


def test_linkedin_publication_validation_empty():
    """
    Test the validation of an empty LinkedIn publication.
    Verify that a ValidationError is raised for a publication without text.
    """
    with pytest.raises(ValidationError, match="LinkedIn publication text cannot be empty"):
        LinkedInPublication("")


def test_linkedin_publication_validation_too_long():
    """
    Test the validation of a LinkedIn publication that is too long.
    Verify that a ValidationError is raised for a publication exceeding 3000 characters.
    """
    long_text = "x" * 3001
    with pytest.raises(ValidationError, match="LinkedIn publication text must be 3000 characters or less"):
        LinkedInPublication(long_text)


def test_linkedin_publication_get_text():
    """
    Test the get_text method of LinkedInPublication.
    Verify that it correctly returns the text of the publication.
    """
    text = "Test LinkedIn publication text"
    publication = LinkedInPublication(text)
    assert publication.get_text() == text


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
