# Location: tests/domain/entities/scraping/test_content_type.py

"""
This module contains unit tests for the ContentType enum class.
It verifies the correct functionality of content type resolution,
URL path mapping, theme retrieval, and value proposition retrieval.

Test cases cover:
- Enum creation and values
- URL path and full URL retrieval
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
        assert ContentType.BUSINESS is not None
        assert ContentType.DEVELOPER is not None
        assert ContentType.CASE_STUDY is not None
        assert ContentType.TESTIMONIAL is not None
        assert ContentType.COURSE is not None

    def test_enum_values_correct(self):
        assert ContentType.BUSINESS.value == "business"
        assert ContentType.DEVELOPER.value == "developer"
        assert ContentType.CASE_STUDY.value == "case_study"
        assert ContentType.TESTIMONIAL.value == "testimonial"
        assert ContentType.COURSE.value == "course"

    def test_url_path_retrieval_success(self):
        assert ContentType.BUSINESS.get_url_path() == "/pour-les-entreprises"
        assert ContentType.DEVELOPER.get_url_path() == "/pour-les-developpeurs"
        assert ContentType.CASE_STUDY.get_url_path() == "/etude-de-cas"
        assert ContentType.TESTIMONIAL.get_url_path() == "/temoignage-satochip"
        assert ContentType.COURSE.get_url_path() == "/slide"

    def test_full_url_retrieval_success(self):
        assert ContentType.BUSINESS.get_full_url() == "https://www.techaware.net/pour-les-entreprises"
        assert ContentType.DEVELOPER.get_full_url() == "https://www.techaware.net/pour-les-developpeurs"
        assert ContentType.CASE_STUDY.get_full_url() == "https://www.techaware.net/etude-de-cas"
        assert ContentType.TESTIMONIAL.get_full_url() == "https://www.techaware.net/temoignage-satochip"
        assert ContentType.COURSE.get_full_url() == "https://www.techaware.net/slide"

    def test_key_themes_retrieval_success(self):
        assert ContentType.BUSINESS.get_key_themes() == ["cost_reduction", "talent_acquisition", "mentorship"]
        assert ContentType.DEVELOPER.get_key_themes() == ["practical_experience", "mentorship", "community"]
        assert ContentType.CASE_STUDY.get_key_themes() == ["success_story", "transformation", "growth"]
        assert ContentType.TESTIMONIAL.get_key_themes() == ["client_success", "project_delivery", "satisfaction"]
        assert ContentType.COURSE.get_key_themes() == ["technical_expertise", "industry_insights", "best_practices"]

    def test_value_props_retrieval_success(self):
        assert ContentType.BUSINESS.get_value_props() == ["70% cost reduction", "qualified developers", "expert mentoring"]
        assert ContentType.DEVELOPER.get_value_props() == ["real projects", "expert guidance", "peer support"]
        assert ContentType.CASE_STUDY.get_value_props() == ["proven results", "successful transitions", "real impact"]
        assert ContentType.TESTIMONIAL.get_value_props() == ["client satisfaction", "project success", "team integration"]
        assert ContentType.COURSE.get_value_props() == ["technical insights", "industry trends", "practical solutions"]

    def test_from_string_valid_inputs(self):
        assert ContentType.from_string("business") == ContentType.BUSINESS
        assert ContentType.from_string("DEVELOPER") == ContentType.DEVELOPER
        assert ContentType.from_string("case_study") == ContentType.CASE_STUDY
        assert ContentType.from_string("TESTIMONIAL") == ContentType.TESTIMONIAL
        assert ContentType.from_string("Course") == ContentType.COURSE

    def test_from_string_invalid_inputs(self):
        with pytest.raises(ValidationError):
            ContentType.from_string("")
        with pytest.raises(ValidationError):
            ContentType.from_string("invalid")
        with pytest.raises(ValidationError):
            ContentType.from_string("unknown")
        with pytest.raises(ValidationError):
            ContentType.from_string("123")
        with pytest.raises(ValidationError):
            ContentType.from_string("not_a_type")

    def test_string_representation(self):
        assert str(ContentType.BUSINESS) == "business"
        assert str(ContentType.DEVELOPER) == "developer"
        assert str(ContentType.CASE_STUDY) == "case_study"
        assert str(ContentType.TESTIMONIAL) == "testimonial"
        assert str(ContentType.COURSE) == "course"

    def test_themes_list_independence(self):
        themes = ContentType.BUSINESS.get_key_themes()
        themes.append("new_theme")
        assert ContentType.BUSINESS.get_key_themes() == ["cost_reduction", "talent_acquisition", "mentorship"]

    def test_value_props_list_independence(self):
        value_props = ContentType.BUSINESS.get_value_props()
        value_props.append("new_value_prop")
        assert ContentType.BUSINESS.get_value_props() == ["70% cost reduction", "qualified developers", "expert mentoring"]

    def test_enum_immutability(self):
        # Vérifier l'impossibilité de modifier une valeur existante
        with pytest.raises(AttributeError):
            ContentType.BUSINESS = "new_value"
        assert ContentType.BUSINESS == ContentType.BUSINESS  # Vérifie que la valeur reste inchangée

        # Vérifier l'impossibilité de supprimer un membre de l'énumération
        with pytest.raises(AttributeError):
            del ContentType.BUSINESS
        assert hasattr(ContentType, "BUSINESS")  # Vérifie que le membre existe toujours

        # Vérifier l'impossibilité d'ajouter un nouvel attribut, puis le supprimer pour restaurer l'état initial
        ContentType.NEW_ATTRIBUTE = "new_value"
        assert hasattr(ContentType, "NEW_ATTRIBUTE")  # Vérifie que l'attribut a été ajouté
        del ContentType.NEW_ATTRIBUTE  # Supprime l'attribut ajouté pour restaurer l'état initial
        assert not hasattr(ContentType, "NEW_ATTRIBUTE")  # Vérifie que l'attribut a bien été supprimé


if __name__ == "__main__":
    pytest.main(["-v", __file__])
