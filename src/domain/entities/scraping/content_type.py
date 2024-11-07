# Location: ./src/domain/entities/scraping/content_type.py

from enum import Enum
from urllib.parse import urljoin
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import ValidationError


class ContentType(Enum):
    """
    Enumeration of content types available for scraping from TechAware website.
    """

    BUSINESS = "business"
    DEVELOPER = "developer"
    CASE_STUDY = "case_study"
    TESTIMONIAL = "testimonial"
    COURSE = "course"

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
            ContentType.COURSE: "/slide"
        }

        try:
            return url_paths[self]
        except KeyError:
            error_msg = f"URL path not defined for content type: {self.name}"
            logger.error(error_msg)
            raise ValidationError(error_msg)

    @log_method(logger)
    def get_full_url(self) -> str:
        """
        Get the complete URL for the content type.

        Returns:
            str: The complete URL including base URL and path

        Raises:
            ValidationError: If the URL construction fails
        """
        base_url = "https://www.techaware.net"
        try:
            path = self.get_url_path()
            full_url = urljoin(base_url, path)
            logger.debug(f"Generated full URL for {self.name}: {full_url}")
            return full_url
        except Exception as e:
            error_msg = f"Failed to construct full URL for {self.name}: {str(e)}"
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
            ContentType.COURSE: ["technical_expertise", "industry_insights", "best_practices"]
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
            ContentType.COURSE: ["technical insights", "industry trends", "practical solutions"]
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
