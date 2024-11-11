# Changelog

## [Unreleased]
### Changed
- Change url for developer without 'é'
### Documentation
#### API Integration
- Add api aknolewdment url
- Add documentation for API, implementation and contributong according to readme.md
#### Core Infrastructure
- Cancel file and requirements
- Update changelog [skip ci]
### Fixed
- Fixing test failures
### Other
#### Core Infrastructure
- Merge branch 'develop' of https://github.com/Tech-Aware/TechAware.social_media_automator into develop
#### API Integration
- Refactor-openai_api): changed logic according to prompt builder implentation
### Testing
- Fix retry behavior test for long tweets
## [1.0.0] - 2024-11-09
### Changed
#### Facebook Integration
- Add separation, new test and adjustment:
#### LinkedIn Integration
- Add debug message for improve clarity
#### Core Infrastructure
- Add better output format
- Add semantic versioning into changelo generation
### Documentation
- Update changelog [skip ci]
### Fixed
- Add bug correction, adjustment in assertion... ALL TESTS ARE OK
### Other
- Add assertion adjustment and mock response
- Merge branch 'develop' of https://github.com/Tech-Aware/TechAware.social_media_automator into develop Retrieve changelog
## [0.3.0] - 2024-10-26
### Added
#### Facebook Integration
- Add Facebook environment configuration
- Add Facebook post functionality
- Add FacebookError class
- Add FacebookGateway abstract class
- Add new exceptions for linkedin and facebook generation
- Add verifications, logs and exceptions: - add more debug message to better follow process - add a verification of page acces to post in facebook - add personnalized exceptions
- Adding instruction to prompt message
- Implement FacebookPublication with validation
#### Prompting System Integration
- Add module fodler
- Add more prompt details (WIP_prompting_scrapping)
#### Core Infrastructure
- Add new exceptions for odoo next release
- Change prompt call for improve performance
- Change prompt method for improve performance
- Changed programm entry for menu selection
- Enhance IA guidelines in prompt
#### Content Generation
- Add Facebook content generation
- Add scraper content for techaware.net/webpage
- Change url to join base url
#### CLI Improvements
- Add linkedin generation and post
- Add menu selection for new feature/blog_article_integration
- Add time for console visibility - add a timer, while loop for emulate a waiting process into terminal
- Integrate Facebook posting capabilities
#### LinkedIn Integration
- Add post generation for linkedin plateform
#### API Integration
- Add prompt functionnality - add guidelines content - add relevant_link[topic] dict with random selection - fix ** format into generation
- Implement Facebook API integration
### Changed
- Canceled file_reader and add imroved prompting continuity
- Changed process to generate and publish - add media social post generation separatly to better integration
### Documentation
#### Content Generation
- Add historical changelog content
- Cancel scraping added content: DEPRECATED
#### Core Infrastructure
- Cancel #TEST line
- Upadted
- Update arborescence
- Update changelog [skip ci]
- Updated according to last implementation
### Fixed
#### API Integration
- Changed error raised from tweeter to OpenAIError
#### Core Infrastructure
- Cancel debug message who returned result in everything
#### Facebook Integration
- Add log message for debug
### Other
#### Core Infrastructure
- Add automated changelog generation workflow
- Add initial project dependencies
- Deleted files
- Merge branch 'develop' of https://github.com/Tech-Aware/TechAware.social_media_automator into develop
#### Prompting System Integration
- Merge branch 'develop' into feature/scraping_prompting_integration
- Merge branch 'feature/prompting_integration' into develop
#### Facebook Integration
- Merge branch 'develop' into feature/facebook_integration - add new dependies into the requirements files
- Merge branch 'develop' into feature/facebook_integration - fusion of develop into feature/facebook_integration
- Résolution des conflits et fusion de develop dans feature/facebook_integration
### Testing
- Add test for prompt_builder.py
- Add test for prompt_builder_gateway.py
- Test ci worflow changelog generation
## [0.1.0] - 2024-10-10
### Added
#### CLI Improvements
- Add LinkedIn API integration to CLI commands
#### Core Infrastructure
- Add explicit tweet validation before posting
- Add script for running all unit tests
### Changed
#### LinkedIn Integration
- Add LinkedInError for LinkedIn API error handling
#### Core Infrastructure
- Enhance test coverage and improve mock usage
- Improve test coverage for PostTweetUseCase
#### CLI Improvements
- Enhance test coverage and error handling for CLI class
- Streamline tweet generation and posting process
#### API Integration
- Enhance test coverage and improve mock responses
### Fixed
#### Core Infrastructure
- Rename 'entitites' folder to 'entities' for consistency
- Repository url adress - changed te default url adress to the correct url.git
#### API Integration
- Improve error handling and generated tweet formatting
### Other
#### Core Infrastructure
- Add __init__.py for utils tests
- Enhance test coverage for read_prompt_file function
- Initial project setup
#### LinkedIn Integration
- Add LinkedIn user info retrieval function
- Create LinkedInGateway abstract base class
- Create LinkedInPublication class
- Create PostLinkedInUseCase
- Set up LinkedIn environment configuration
- Update environment to include LinkedIn credentials
#### API Integration
- Create LinkedInAPI class
### Testing
#### LinkedIn Integration
- Add initial tests for LinkedIn config
- Add initial tests for LinkedInGateway
- Add tests for LinkedIn credentials in environment config
- Add unit tests for LinkedInError
- Create initial tests for PostLinkedInUseCase
- Set up initial tests for LinkedInPublication
#### API Integration
- Create initial tests for LinkedInAPI
### Notes
- All dates are in YYYY-MM-DD format
- Version numbers follow semantic versioning
- Commits organized by feature and functionality
- Each version builds upon previous functionality
