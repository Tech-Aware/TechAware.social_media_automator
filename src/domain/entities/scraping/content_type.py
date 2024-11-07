# Location: src/domain/entities/scraping/content_type.py

"""
This module defines the ContentType enumeration used to categorize different types
of content that can be scraped from the TechAware website. It provides a standardized
way to specify content types across the application, with proper error handling
and logging.
"""

from enum import Enum, auto
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import ValidationError


class ContentType(Enum):
    """
    Enumeration of content types available for scraping from TechAware website.

    Attributes:
        BUSINESS: Business-oriented content about TechAware's services for companies
        DEVELOPER: Content targeted at developers and career changers
        CASE_STUDY: Detailed case studies of successful projects
        TESTIMONIAL: Client testimonials and success stories
        BLOG: Blog articles and technical content
    """

    BUSINESS = auto()
    DEVELOPER = auto()
    CASE_STUDY = auto()
    TESTIMONIAL = auto()
    BLOG = auto()

    @log_method(logger)
    def get_url_path(self) -> str:
        """
        Get the corresponding URL path for each content type.

        Returns:
            str: The URL path segment for the content type

        Raises:
            ValidationError: If the URL path is not defined for the content type
        """
        url_paths = {
            ContentType.BUSINESS: "/pour-les-entreprises",
            ContentType.DEVELOPER: "/pour-les-developpeurs",
            ContentType.CASE_STUDY: "/etude-de-cas",
            ContentType.TESTIMONIAL: "/temoignage-satochip",
            ContentType.BLOG: "/blog"
        }

        try:
            url_path = url_paths[self]
            logger.debug(f"Retrieved URL path for {self.name}: {url_path}")
            return url_path
        except KeyError:
            error_msg = f"URL path not defined for content type: {self.name}"
            logger.error(error_msg)
            raise ValidationError(error_msg)

    @log_method(logger)
    def get_key_themes(self) -> list[str]:
        """
        Get the key themes associated with each content type.

        Returns:
            list[str]: List of key themes for the content type

        Raises:
            ValidationError: If themes are not defined for the content type
        """
        theme_map = {
            ContentType.BUSINESS: ["cost_reduction", "talent_acquisition", "mentorship"],
            ContentType.DEVELOPER: ["practical_experience", "mentorship", "community"],
            ContentType.CASE_STUDY: ["success_story", "transformation", "growth"],
            ContentType.TESTIMONIAL: ["client_success", "project_delivery", "satisfaction"],
            ContentType.BLOG: ["technical_expertise", "industry_insights", "best_practices"]
        }

        try:
            themes = theme_map[self]
            logger.debug(f"Retrieved themes for {self.name}: {themes}")
            return themes
        except KeyError:
            error_msg = f"Themes not defined for content type: {self.name}"
            logger.error(error_msg)
            raise ValidationError(error_msg)

    @log_method(logger)
    def get_value_props(self) -> list[str]:
        """
        Get the value propositions associated with each content type.

        Returns:
            list[str]: List of value propositions for the content type

        Raises:
            ValidationError: If value propositions are not defined for the content type
        """
        value_prop_map = {
            ContentType.BUSINESS: ["70% cost reduction", "qualified developers", "expert mentoring"],
            ContentType.DEVELOPER: ["real projects", "expert guidance", "peer support"],
            ContentType.CASE_STUDY: ["proven results", "successful transitions", "real impact"],
            ContentType.TESTIMONIAL: ["client satisfaction", "project success", "team integration"],
            ContentType.BLOG: ["technical insights", "industry trends", "practical solutions"]
        }

        try:
            value_props = value_prop_map[self]
            logger.debug(f"Retrieved value propositions for {self.name}: {value_props}")
            return value_props
        except KeyError:
            error_msg = f"Value propositions not defined for content type: {self.name}"
            logger.error(error_msg)
            raise ValidationError(error_msg)

    @classmethod
    @log_method(logger)
    def from_string(cls, content_type_str: str) -> 'ContentType':
        """
        Create a ContentType from a string representation.

        Args:
            content_type_str: String representation of content type

        Returns:
            ContentType: The corresponding ContentType enum value

        Raises:
            ValidationError: If the string doesn't match any content type
        """
        try:
            return cls[content_type_str.upper()]
        except KeyError:
            error_msg = f"Invalid content type string: {content_type_str}"
            logger.error(error_msg)
            valid_types = [t.name for t in cls]
            error_msg = f"{error_msg}. Valid types are: {', '.join(valid_types)}"
            raise ValidationError(error_msg)

    def __str__(self) -> str:
        """
        Get string representation of the content type.

        Returns:
            str: String representation of the content type
        """
        return self.name.lower()