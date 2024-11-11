# src/presentation/post_command.py

import argparse
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import ConfigurationError, AutomatorError
from src.use_cases.generate_facebook_publication import GenerateFacebookPublicationUseCase
from src.use_cases.generate_linkedin_post import GenerateLinkedInPostUseCase
from src.use_cases.generate_tweet import GenerateTweetUseCase
from src.use_cases.post_facebook import PostFacebookUseCase
from src.use_cases.post_linkedin import PostLinkedInUseCase
from src.use_cases.post_tweet import PostTweetUseCase
from src.infrastructure.external.facebook_api import FacebookAPI
from src.infrastructure.external.linkedin_api import LinkedInAPI
from src.infrastructure.external.twitter_api import TwitterAPI
from src.infrastructure.external.openai_api import OpenAIAPI


class PostCommand:
    @log_method(logger)
    def __init__(self):
        """Initialize command dependencies"""
        try:
            self.openai_gateway = OpenAIAPI()
            logger.debug("OpenAI gateway initialized")
        except Exception as e:
            logger.error(f"Failed to initialize post command: {str(e)}")
            raise

    @log_method(logger)
    def execute(self, platform: str, dry_run: bool = False, topic: str = None):
        """
        Execute posting command for specified platform.

        Args:
            platform (str): Target platform ('facebook', 'linkedin', 'twitter')
            dry_run (bool): If True, only generate content without posting
            topic (str): Optional topic category to use
        """
        try:
            if platform == 'facebook':
                return self._handle_facebook(dry_run, topic)
            elif platform == 'linkedin':
                return self._handle_linkedin(dry_run, topic)
            elif platform == 'twitter':
                return self._handle_twitter(dry_run, topic)
            else:
                raise ValueError(f"Unsupported platform: {platform}")
        except Exception as e:
            logger.error(f"Error executing post command: {str(e)}")
            raise

    @log_method(logger)
    def _handle_facebook(self, dry_run: bool, topic: str = None):
        """Handle Facebook posting"""
        try:
            generate_use_case = GenerateFacebookPublicationUseCase(self.openai_gateway)
            logger.info("Generating Facebook content")
            content = generate_use_case.execute()

            if dry_run:
                logger.info("Dry run - content generated but not posted")
                return content

            facebook_gateway = FacebookAPI()
            post_use_case = PostFacebookUseCase(facebook_gateway)
            logger.info("Posting to Facebook")
            result = post_use_case.execute(content)
            return result

        except Exception as e:
            logger.error(f"Error handling Facebook: {str(e)}")
            raise

    @log_method(logger)
    def _handle_linkedin(self, dry_run: bool, topic: str = None):
        """Handle LinkedIn posting"""
        try:
            generate_use_case = GenerateLinkedInPostUseCase(self.openai_gateway)
            logger.info("Generating LinkedIn content")
            content = generate_use_case.execute()

            if dry_run:
                logger.info("Dry run - content generated but not posted")
                return content

            linkedin_gateway = LinkedInAPI()
            post_use_case = PostLinkedInUseCase(linkedin_gateway)
            logger.info("Posting to LinkedIn")
            result = post_use_case.execute(content)
            return result

        except Exception as e:
            logger.error(f"Error handling LinkedIn: {str(e)}")
            raise

    @log_method(logger)
    def _handle_twitter(self, dry_run: bool, topic: str = None):
        """Handle Twitter posting"""
        try:
            generate_use_case = GenerateTweetUseCase(self.openai_gateway)
            logger.info("Generating tweet")
            content = generate_use_case.execute()

            if dry_run:
                logger.info("Dry run - content generated but not posted")
                return content

            twitter_gateway = TwitterAPI()
            post_use_case = PostTweetUseCase(twitter_gateway)
            logger.info("Posting to Twitter")
            result = post_use_case.execute(content)
            return result

        except Exception as e:
            logger.error(f"Error handling Twitter: {str(e)}")
            raise