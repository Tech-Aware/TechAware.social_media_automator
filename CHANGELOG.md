# TechAware Social Media Automator - Changelog

## [1.3.0] - 2024-11-08
### Added
- New prompting module (d436fdff2715)
- Comprehensive unit tests for prompt_builder.py (b497aa037e5e)
- Comprehensive unit tests for prompt_builder_gateway.py (c31b6fb9be22)

### Changed
- Optimized prompt_builder performance (d7e32fb43cc3)
- Optimized prompt_builder_gateway performance (778e59bb1669)
- Refactored use cases for better performance (a89e66f389c2)
- Modified CLI to remove file_reader dependency (cb53eae1eb82)

### Removed
- Complete removal of scraping module and associated files (f97d12f16926)
- Removed file_reader functionality (cb53eae1eb82)

### Documentation
- Updated README and requirements (0979018be5df)

### Integration
- Merged feature/prompting_integration into develop branch (69fddea47ef3)

## [1.2.0] - 2024-11-07
### Added
- Integrated scraping for techaware.net with relative URLs (67441e1f219c)
- Implemented content types and associated themes
- Enhanced prompts in use cases (0660a22e9116)

### Changed
- Modified URLs to use urljoin (67441e1f219c)

### Documentation
- Updated README directory structure (d055e975d777)

## [1.1.0] - 2024-11-04
### Added
- Roadmap for blog article integration (c368ca7bfcb3)
- New exceptions for future Odoo integration (b79cbe35a905)
- LinkedIn generation and publishing capabilities (3341e854e915)
- Enhanced Facebook prompt instructions (69e60c4a67fd, 04314c036f73)
- LinkedIn post generation support (8804d01c124)

### Fixed
- Fixed OpenAI error handling (ca038d06536c)
- Replaced Twitter errors with OpenAI errors in openai_api

### Dependencies
- Updated project dependencies (07d7ca88ef9)
  - pytest for testing framework
  - python-dotenv for environment management
  - requests for API calls
  - requests-oauthlib for Twitter authentication
  - openai for content generation

## [1.0.0] - 2024-10-28
### Added
- Blog article selection menu (a0c1bc1460c7)
- Console visibility timer (ba19458ec48b)
- OpenAI prompt improvements (5cbf8ab08568)
  - Added content guidelines
  - Random relevant link selection
  - Format correction

### Changed
- Modified entry point for menu selection (5b0b0961792)
- Restructured generation and publishing process (b8a282f63dc)

### Fixed
- Removed superfluous debug messages (7b9ba5e18bbd)

## [0.3.0] - 2024-10-26
### Added
- Complete Facebook integration
  - Facebook API implementation (ee82acc1a6b)
  - FacebookGateway interface (c9b2ca0226)
  - Facebook environment configuration (45e748ec2d)
  - FacebookPublication entity with validation (fbae28693f6)
  - FacebookError exception (02f829a83cf)
- Facebook publishing features
  - Content generation (9fda32bca7f)
  - Post publishing (e84c839c3bb)
  - CLI integration (ce32b3a36d7)

### Enhanced
- Facebook API verifications and logging (b1c77494fea)
- Custom error handling (b1c77494fea)
- Facebook-specific exceptions

## [0.2.0] - 2024-10-12
### Added
- Complete LinkedIn integration
  - LinkedInPublication entity initialization (9bf53d200b0)
  - LinkedIn environment configuration (60e465e6da2)
  - LinkedInAPI class implementation (0f5cb085b27)
  - LinkedIn user info retrieval function (67e93b02722)
  - LinkedInGateway interface (8497e80d336)
  - LinkedIn publishing use case (2b1637d275)

### Testing
- Unit tests for LinkedInPublication (325ea9f2e72)
- LinkedIn configuration tests (f387b349912)
- LinkedIn API tests (031613e8e4d)
- LinkedIn gateway tests (6d81e68e64d)
- LinkedIn use case tests (5ac9081a10a)

### Changed
- Renamed 'entitites' folder to 'entities' (8bba4be5dba)

## [0.1.0] - 2024-10-10
### Added
- Centralized unit testing script (89788767a01)
  - Automatic test discovery
  - Individual file execution
  - Results reporting

### Enhanced
- Improved PostTweetUseCase tests (66d7f75869)
- Enhanced CLI testing (24d56f92ab0)
- Improved logger testing (18bd509797)
- Added file_reader tests (796a702e89b)
- Explicit tweet validation (8df06986a44)

### Changed
- Simplified tweet generation process (091fe6f38b5)
- Improved generated tweet formatting (24034417a24)

### Fixed
- Fixed repository URL in README (1764fc71c9d)

## [0.0.1] - 2024-10-10
### Added
- Initial project setup (2bb9493457)
- Basic project structure
- Development environment configuration