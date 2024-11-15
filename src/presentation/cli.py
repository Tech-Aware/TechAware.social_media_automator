# src/presentation/cli.py

"""
This module implements the Command Line Interface (CLI) for the social media automator.
It handles user interaction and coordinates the execution of various use cases for
posting content to different social media platforms (Twitter, Facebook, LinkedIn).
"""

import time
from src.use_cases.post_tweet import PostTweetUseCase
from src.use_cases.post_facebook import PostFacebookUseCase
from src.use_cases.post_linkedin import PostLinkedInUseCase
from src.use_cases.generate_tweet import GenerateTweetUseCase
from src.use_cases.generate_facebook_publication import GenerateFacebookPublicationUseCase
from src.use_cases.generate_linkedin_post import GenerateLinkedInPostUseCase
from src.infrastructure.config.environment import initialize_environment
from src.infrastructure.external.twitter_api import TwitterAPI
from src.infrastructure.external.facebook_api import FacebookAPI
from src.infrastructure.external.linkedin_api import LinkedInAPI
from src.infrastructure.external.openai_api import OpenAIAPI
from src.infrastructure.logging.logger import logger, log_method
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
            # Initialiser l'environnement avant toute autre chose
            logger.info("Initializing environment")
            if not initialize_environment():
                raise ConfigurationError("Failed to initialize environment")

            logger.info("Environment initialized successfully")

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
    def menu(self):
        """Display the menu and handle user input."""
        asking_user = input("Would you like to create a blog article ? [y/n] ")
        if asking_user == "y":
            print("You want to create a blog article first !")
        else:
            self.run()

    @log_method(logger)
    def run(self):
        """
        Run the CLI, handling platform-specific content generation and posting.
        This method handles the entire workflow of generating and posting content
        to multiple social media platforms.
        """
        try:
            # Generate and post content for each platform
            counter = 3
            time.sleep(1)
            print("Waiting for facebook generation")
            while counter != 0:
                print("...")
                time.sleep(1)
                counter -= 1

            # Facebook
            logger.debug("Generating Facebook post")
            facebook_text = self.generate_facebook_use_case.execute()
            logger.success("Facebook publication created successfully")
            print(f"Generated Facebook post successfully: {facebook_text[0:50]}")
            counter = 3
            time.sleep(1)
            print("Waiting for linkedin generation")
            while counter != 0:
                print("...")
                time.sleep(1)
                counter -= 1

            # LinkedIn
            logger.debug("Generating Linkedin post")
            linkedin_text = self.generate_linkedin_use_case.execute()
            logger.success("Linkedin publication created successfully")
            print(f"Generated Linkedin post successfully: {linkedin_text[0:50]}")
            counter = 3
            time.sleep(1)
            print("Waiting for X tweet generation")
            while counter != 0:
                print("...")
                time.sleep(1)
                counter -= 1

            # X
            logger.debug("Generating x post")
            x_text = self.generate_tweet_use_case.execute()
            logger.success("X publication created successfully")
            print(f"Generated x post successfully: {x_text[0:50]}")
            counter = 3
            time.sleep(1)
            print("Posting in facebook")
            while counter != 0:
                print("...")
                time.sleep(1)
                counter -= 1

            # Post to platforms
            logger.debug("Posting to Facebook")
            facebook_result = self.post_facebook_use_case.execute(facebook_text)
            logger.success(f"Facebook post published successfully. Post ID: {facebook_result['id']}")
            print(f"Facebook post published successfully. Post ID: {facebook_result['id']}")
            counter = 3
            time.sleep(1)
            print("Posting in LinkedIn")
            while counter != 0:
                print("...")
                time.sleep(1)
                counter -= 1

            logger.debug("Posting to LinkedIn")
            linkedin_result = self.post_linkedin_use_case.execute(linkedin_text)
            logger.success("Linkedin post published successfully")
            print(f"Linkedin post published successfully. {linkedin_result}")
            counter = 3
            time.sleep(1)
            print("Posting in X")
            while counter != 0:
                print("...")
                time.sleep(1)
                counter -= 1

            logger.debug("Posting to X")
            x_result = self.post_tweet_use_case.execute(x_text)
            logger.success(f"X post published successfully.")
            print(f"X post published successfully")

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