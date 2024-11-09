# Changelog
## [1.0.0] - 2024-11-09
### Added
#### Core Functionality
- Add new exceptions for linkedin and facebook generation
- Change prompt method for improve performance
- Change prompt method for improve performance
- Add more prompt details (WIP_prompting_scrapping)
- Enhance IA guidelines in prompt
- Add new exceptions for odoo next release
- Add linkedin generation and post
- Changed programm entry for menu selection
- Add menu selection for new feature/blog_article_integration
- Add time for console visibility - add a timer, while loop for emulate a waiting process into terminal
- Add prompt functionnality - add guidelines content - add relevant_link[topic] dict with random selection - fix ** format into generation
- Integrate Facebook posting capabilities
- Add Facebook content generation
- Add Facebook post functionality
- Implement Facebook API integration
- Add FacebookGateway abstract class
- Add Facebook environment configuration
- Implement FacebookPublication with validation
- Add FacebookError class
- Add LinkedIn API integration to CLI commands
- Add explicit tweet validation before posting
#### Prompting System Integration
- Add module fodler
#### Use Cases Enhancement
- Change prompt call for improve performance
#### Testing Infrastructure
- Change url to join base url
- Add scraper content for techaware.net/webpage
- Add script for running all unit tests
#### Facebook Integration
- Adding instruction to prompt message
- Adding instruction to prompt message
- Add verifications, logs and exceptions: - add more debug message to better follow process - add a verification of page acces to post in facebook - add personnalized exceptions
#### LinkedIn Integration
- Add post generation for linkedin plateform
### Build
#### Core Functionality
- Add initial project dependencies
### CI
#### Core Functionality
- Add automated changelog generation workflow
### Changed
#### Core Functionality
- Add better output format
- Canceled file_reader and add imroved prompting continuity
- Changed process to generate and publish - add media social post generation separatly to better integration
- Add LinkedInError for LinkedIn API error handling
- Streamline tweet generation and posting process
#### Testing Infrastructure
- Improve test coverage for PostTweetUseCase
- Enhance test coverage and error handling for CLI class
- Enhance test coverage and improve mock usage
- Enhance test coverage and improve mock responses
### Documentation
#### Core Functionality
- Cancel scraping added content: DEPRECATED
- Update changelog [skip ci]
- Cancel #TEST line
- Update changelog [skip ci]
- Cancel #TEST line
- Update changelog [skip ci]
- Add historical changelog content
- Update changelog [skip ci]
- Updated according to last implementation
- Update arborescence
- Upadted
### Fixed
#### Core Functionality
- Changed error raised from tweeter to OpenAIError
- Cancel debug message who returned result in everything
- Rename 'entitites' folder to 'entities' for consistency
- Improve error handling and generated tweet formatting
- Repository url adress - changed te default url adress to the correct url.git
#### Facebook Integration
- Add log message for debug
### Maintenance
#### Testing Infrastructure
- Add __init__.py for utils tests
- Enhance test coverage for read_prompt_file function
#### Core Functionality
- Update environment to include LinkedIn credentials
- Initial project setup
### Other
#### Core Functionality
- Create PostLinkedInUseCase
- Create LinkedInGateway abstract base class
- Add LinkedIn user info retrieval function
- Create LinkedInAPI class
- Set up LinkedIn environment configuration
- Create LinkedInPublication class
### Testing
#### Core Functionality
- Test ci worflow changelog generation
- Create initial tests for PostLinkedInUseCase
- Add initial tests for LinkedInGateway
- Create initial tests for LinkedInAPI
- Add initial tests for LinkedIn config
- Set up initial tests for LinkedInPublication
- Add tests for LinkedIn credentials in environment config
- Add unit tests for LinkedInError
#### Testing Infrastructure
- Add test for prompt_builder_gateway.py
- Add test for prompt_builder.py
### Notes
- All dates are in YYYY-MM-DD format
- Version numbers follow semantic versioning
- Commits organized by feature and functionality
- Each version builds upon previous functionality
