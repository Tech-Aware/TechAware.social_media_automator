# Changelog

All notable changes to this project will be documented in this file.


## [Unreleased]


### Added

- (exceptions) add new exceptions for linkedin and facebook generation (caab39a2)
- (prompting) add module fodler (d436fdff)
- (use_cases) change prompt call for improve performance (a89e66f3)
- (prompt_builder_gateway) change prompt method for improve performance (778e59bb)
- (prompt_builder) change prompt method for improve performance (d7e32fb4)
- (content_type/test_content_type) change url to join base url (67441e1f)
- (content_type/test_content_type) add scraper content for techaware.net/webpage (1ce51958)
- (uses_cases) add more prompt details (WIP_prompting_scrapping) (0660a22e)
- (uses_cases) Enhance IA guidelines in prompt (22a83f3c)
- (exceptions) add new exceptions for odoo next release (b79cbe35)
- (cli) add linkedin generation and post (3341e854)
- (generate_facebook_publication) Adding instruction to prompt message (69e60c4a)
- (generate_facebook_publication) Adding instruction to prompt message (04314c03)
- (generate_linkedinpost) add post generation for linkedin plateform (8804d01c)
- (main) changed programm entry for menu selection (5b0b0961)
- (cli) add menu selection for new feature/blog_article_integration (a0c1bc14)
- (cli) add time for console visibility - add a timer, while loop for emulate a waiting process into terminal (ba19458e)
- (openai_api) add prompt functionnality - add guidelines content - add relevant_link[topic] dict with random selection - fix ** format into generation (5cbf8ab0)
- (facebook_api) add verifications, logs and exceptions: - add more debug message to better follow process - add a verification of page acces to post in facebook - add personnalized exceptions (b1c77494)
- (cli) integrate Facebook posting capabilities (ce32b3a3)
- (usecase) add Facebook content generation (9fda32bc)
- (usecase) add Facebook post functionality (e84c839c)
- (api) implement Facebook API integration (ee82acc1)
- (interface) add FacebookGateway abstract class (c9b2ca02)
- (config) add Facebook environment configuration (45e748ec)
- (entity) implement FacebookPublication with validation (fbae2869)
- (exceptions) add FacebookError class (02f829a8)
- (cli) add LinkedIn API integration to CLI commands (92b32e31)
- (run_tests) Add script for running all unit tests (89788767)
- (post_tweet) Add explicit tweet validation before posting (8df06986)

### Build

- (deps) add initial project dependencies (07d7ca88)

### CI

- (github-actions) add automated changelog generation workflow (e041213a)

### Changed

- (cli) canceled file_reader and add imroved prompting continuity (cb53eae1)
- (cli) changed process to generate and publish - add media social post generation separatly to better integration (b8a282f6)
- (exceptions) add LinkedInError for LinkedIn API error handling (4faed540)
- (test_post_tweet) Improve test coverage for PostTweetUseCase (66d7f758)
- (test_cli) Enhance test coverage and error handling for CLI class (24d56f92)
- (test_loger) Enhance test coverage and improve mock usage (18bd5097)
- (test_openai_api) Enhance test coverage and improve mock responses (103994fc)
- (cli) Streamline tweet generation and posting process (091fe6f3)

### Documentation

- (readme) cancel #TEST line (39ac922c)
- update changelog [skip ci] (869f10b5)
- (readme) cancel #TEST line (f2e4fff1)
- update changelog [skip ci] (75a319a0)
- (changelog) add historical changelog content (4da8935e)
- update changelog [skip ci] (be496825)
- (readme/requirements) updated according to last implementation (0979018b)
- (readme) update arborescence (d055e975)
- (readme) upadted (2848d738)

### Fixed

- (openai_api) changed error raised from tweeter to OpenAIError (ca038d06)
- (logger) cancel debug message who returned result in everything (ddcfcc11)
- (generate_facebook_publication) add log message for debug (b437175e)
- rename 'entitites' folder to 'entities' for consistency (8bba4be5)
- (openai_api) Improve error handling and generated tweet formatting (24034417)
- (README) repository url adress - changed te default url adress to the correct url.git (1764fc71)

### Maintenance

- (tests) add __init__.py for utils tests (b98e87c6)
- (config) update environment to include LinkedIn credentials (be4726d4)
- (test_file_reader) Enhance test coverage for read_prompt_file function (796a702e)
- Initial project setup (2bb94934)

### Other

- (use-case) create PostLinkedInUseCase (2b1637d2)
- (interface) create LinkedInGateway abstract base class (8497e80d)
- (utils) add LinkedIn user info retrieval function (67e93b02)
- (api) create LinkedInAPI class (0f5cb085)
- (config) set up LinkedIn environment configuration (60e465e6)
- (entity) create LinkedInPublication class (9bf53d20)

### Testing

- (worflow) test ci worflow changelog generation (becb779a)
- (test_prompt_builder_gateway) add test for prompt_builder_gateway.py (c31b6fb9)
- (test_prompt_builder) add test for prompt_builder.py (b497aa03)
- (use-case) create initial tests for PostLinkedInUseCase (5ac9081a)
- (interface) add initial tests for LinkedInGateway (6d81e68e)
- (api) create initial tests for LinkedInAPI (031613e8)
- (config) add initial tests for LinkedIn config (f387b349)
- (entity) set up initial tests for LinkedInPublication (325ea9f2)
- (config) add tests for LinkedIn credentials in environment config (0015c633)
- (exceptions) add unit tests for LinkedInError (9abfa8f7)