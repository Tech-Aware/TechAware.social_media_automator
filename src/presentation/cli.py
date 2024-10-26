# Location: src/presentation/cli.py

"""
This module implements the Command Line Interface (CLI) for the social media automator.
It handles user interaction and coordinates the execution of various use cases for
posting content to different social media platforms (Twitter, Facebook, LinkedIn),
using platform-specific prompts for content generation.
"""

import time
from src.use_cases.post_tweet import PostTweetUseCase
from src.use_cases.post_facebook import PostFacebookUseCase
from src.use_cases.post_linkedin import PostLinkedInUseCase
from src.use_cases.generate_tweet import GenerateTweetUseCase
from src.use_cases.generate_facebook_publication import GenerateFacebookPublicationUseCase
from src.use_cases.generate_linkedin_post import GenerateLinkedInPostUseCase
from src.infrastructure.external.twitter_api import TwitterAPI
from src.infrastructure.external.facebook_api import FacebookAPI
from src.infrastructure.external.linkedin_api import LinkedInAPI
from src.infrastructure.external.openai_api import OpenAIAPI
from src.infrastructure.logging.logger import logger, log_method
from src.infrastructure.utils.file_reader import read_prompt_file
from src.domain.exceptions import (
    AutomatorError, TwitterError, FacebookError, LinkedInError,
    ConfigurationError, ValidationError, OpenAIError,
    TweetGenerationError
)


class CLI:
    @log_method(logger)
    def __init__(self):
        """
        Initialize the CLI with necessary use cases and gateways for all platforms.

        Raises:
            AutomatorError: If initialization of any component fails
        """
        try:
            # Initialize gateways
            logger.debug("Creating API instances")
            twitter_gateway = TwitterAPI()
            facebook_gateway = FacebookAPI()
            linkedin_gateway = LinkedInAPI()
            openai_gateway = OpenAIAPI()
            logger.debug("All API instances created")

            # Initialize use cases
            logger.debug("Creating use case instances")
            self.post_tweet_use_case = PostTweetUseCase(twitter_gateway)
            self.post_facebook_use_case = PostFacebookUseCase(facebook_gateway)
            self.post_linkedin_use_case = PostLinkedInUseCase(linkedin_gateway)
            self.generate_tweet_use_case = GenerateTweetUseCase(openai_gateway)
            self.generate_facebook_use_case = GenerateFacebookPublicationUseCase(openai_gateway)
            self.generate_linkedin_use_case = GenerateLinkedInPostUseCase(openai_gateway)
            logger.debug("All use case instances created")

        except ConfigurationError as e:
            error_msg = f"Failed to initialize CLI due to configuration error: {str(e)}"
            logger.error(error_msg)
            raise AutomatorError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error during CLI initialization: {str(e)}"
            logger.error(error_msg)
            raise AutomatorError(error_msg) from e

    @log_method(logger)
    def read_platform_prompt(self, platform: str) -> str:
        """
        Read the prompt file for a specific platform.

        Args:
            platform (str): The platform name ('twitter', 'facebook', or 'linkedin')

        Returns:
            str: The prompt content, or a default prompt if reading fails

        Raises:
            AutomatorError: If there's an error reading the prompt file
        """
        try:
            logger.debug(f"Reading prompt file for {platform}")
            return read_prompt_file(platform)
        except (FileNotFoundError, IOError) as e:
            error_msg = f"Error reading {platform} prompt file: {str(e)}"
            logger.warning(error_msg)
            logger.info(f"Using default prompt for {platform}")
            return f"Generate an engaging {platform} post about technology."
        except Exception as e:
            error_msg = f"Unexpected error reading prompt file for {platform}: {str(e)}"
            logger.error(error_msg)
            raise AutomatorError(error_msg) from e

    @log_method(logger)
    def run(self):
        """
        Run the CLI, handling platform-specific content generation and posting.

        This method handles the entire workflow of generating and posting content
        to multiple social media platforms, with appropriate error handling for each step.
        """
        try:
            # Generate and post content for each platform

            # Facebook
            facebook_prompt = self.read_platform_prompt("facebook")
            logger.debug("Generating Facebook post")
            facebook_text = self.generate_facebook_use_case.execute(facebook_prompt)
            print(f"Generated Facebook post: {facebook_text}")

            # Add delay between posts
            time.sleep(5)

            # Post to Facebook platform
            logger.debug("Posting to Facebook")
            facebook_result = self.post_facebook_use_case.execute(facebook_text)
            print(f"Facebook post created successfully. Post ID: {facebook_result['id']}")

        except ValidationError as e:
            error_msg = f"Invalid content: {str(e)}"
            logger.warning(error_msg)
            print(error_msg)
            raise AutomatorError(error_msg) from e
        except TwitterError as e:
            error_msg = f"Twitter error: {str(e)}"
            logger.error(error_msg)
            print(error_msg)
            raise AutomatorError(error_msg) from e
        except FacebookError as e:
            error_msg = f"Facebook error: {str(e)}"
            logger.error(error_msg)
            print(error_msg)
            raise AutomatorError(error_msg) from e
        except LinkedInError as e:
            error_msg = f"LinkedIn error: {str(e)}"
            logger.error(error_msg)
            print(error_msg)
            raise AutomatorError(error_msg) from e
        except TweetGenerationError as e:
            error_msg = f"Content generation error: {str(e)}"
            logger.error(error_msg)
            print(error_msg)
            raise AutomatorError(error_msg) from e
        except OpenAIError as e:
            error_msg = f"OpenAI error: {str(e)}"
            logger.error(error_msg)
            print(error_msg)
            raise AutomatorError(error_msg) from e
        except AutomatorError as e:
            logger.error(f"Automator error: {str(e)}")
            print(f"An error occurred: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(error_msg, exc_info=True)
            print(error_msg)
            raise AutomatorError(error_msg) from e