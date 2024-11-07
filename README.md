# TechAware Social Media Automator

## Overview
TechAware Social Media Automator is a sophisticated content generation and publishing system designed to manage social media presence and blog content. It leverages OpenAI's GPT models, web scraping, and platform-specific optimization to create engaging, brand-consistent content across multiple platforms.

## Features
- Multi-platform content generation and publishing
- Platform-specific content optimization
- Automated content scheduling
- Brand voice consistency
- SEO optimization for blog content
- Content scraping and analysis
- Error handling and retry mechanisms
- Comprehensive logging

## Project Structure
```
automator/
├── docs/
├── resources/
│   ├── knowledge/
│   └── prompts/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── scraping/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── content_type.py                   # Implemented
│   │   │   │   └── scraped_content.py               # To be implemented
│   │   │   ├── __init__.py
│   │   │   ├── tweet.py
│   │   │   ├── facebook_publication.py
│   │   │   ├── linkedin_publication.py
│   │   │   └── blog_article.py                      # To be implemented
│   │   ├── __init__.py
│   │   └── exceptions.py
│   ├── infrastructure/
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── environment.py
│   │   │   ├── environment_twitter.py
│   │   │   ├── environment_facebook.py
│   │   │   ├── environment_linkedin.py
│   │   │   ├── environment_openai.py
│   │   │   └── environment_odoo.py
│   │   ├── external/
│   │   │   ├── __init__.py
│   │   │   ├── twitter_api.py
│   │   │   ├── facebook_api.py
│   │   │   ├── linkedin_api.py
│   │   │   ├── openai_api.py
│   │   │   └── odoo_api.py
│   │   ├── logging/
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   ├── scraping/                                # New module from architecture changes
│   │   │   ├── __init__.py                         # To be implemented
│   │   │   └── techaware_scraper.py                # To be implemented
│   │   ├── prompting/                              # New module from architecture changes
│   │   │   ├── __init__.py                         # To be implemented
│   │   │   └── prompt_builder.py                   # To be implemented
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── file_reader.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── twitter_gateway.py
│   │   ├── facebook_gateway.py
│   │   ├── linkedin_gateway.py
│   │   ├── openai_gateway.py
│   │   ├── odoo_gateway.py
│   │   ├── scraping_gateway.py                     # To be implemented
│   │   └── prompt_builder_gateway.py               # To be implemented
│   ├── presentation/
│   │   ├── __init__.py
│   │   └── cli.py
│   └── use_cases/
│       ├── __init__.py
│       ├── generate_tweet.py
│       ├── generate_facebook_publication.py
│       ├── generate_linkedin_post.py
│       ├── generate_blog_article.py                 # To be implemented
│       ├── post_tweet.py
│       ├── post_facebook.py
│       ├── post_linkedin.py
│       └── post_blog_article.py                    # To be implemented
└── tests/
    ├── domain/
    │   ├── entities/
    │   │   ├── scraping/
    │   │   │   ├── __init__.py
    │   │   │   ├── test_content_type.py            # Implemented
    │   │   │   └── test_scraped_content.py         # To be implemented
    │   │   ├── test_tweet.py
    │   │   ├── test_facebook_publication.py
    │   │   ├── test_linkedin_publication.py
    │   │   └── test_blog_article.py                # To be implemented
    │   └── test_exceptions.py
    ├── infrastructure/
    │   ├── config/
    │   │   ├── test_environment.py
    │   │   ├── test_environment_twitter.py
    │   │   ├── test_environment_facebook.py
    │   │   ├── test_environment_linkedin.py
    │   │   ├── test_environment_openai.py
    │   │   └── test_environment_odoo.py
    │   ├── external/
    │   │   ├── test_twitter_api.py
    │   │   ├── test_facebook_api.py
    │   │   ├── test_linkedin_api.py
    │   │   ├── test_openai_api.py
    │   │   └── test_odoo_api.py
    │   ├── scraping/                               # New test module
    │   │   └── test_techaware_scraper.py           # To be implemented
    │   ├── prompting/                              # New test module
    │   │   └── test_prompt_builder.py              # To be implemented
    │   └── logging/
    │       └── test_logger.py
    ├── interfaces/
    │   ├── test_twitter_gateway.py
    │   ├── test_facebook_gateway.py
    │   ├── test_linkedin_gateway.py
    │   ├── test_openai_gateway.py
    │   ├── test_odoo_gateway.py
    │   ├── test_scraping_gateway.py                # To be implemented
    │   └── test_prompt_builder_gateway.py          # To be implemented
    ├── presentation/
    │   └── test_cli.py
    └── use_cases/
        ├── test_generate_tweet.py
        ├── test_generate_facebook_publication.py
        ├── test_generate_linkedin_post.py
        ├── test_generate_blog_article.py           # To be implemented
        ├── test_post_tweet.py
        ├── test_post_facebook.py
        ├── test_post_linkedin.py
        └── test_post_blog_article.py               # To be implemented
```

## Requirements
- Python 3.8+
- pip
- Virtual environment (recommended)

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd automator
```

2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Twitter API Credentials
CONSUMER_KEY=your_twitter_consumer_key
CONSUMER_SECRET=your_twitter_consumer_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Facebook API Credentials
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# LinkedIn API Credentials
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_USER_ID=your_linkedin_user_id

# OpenAI API Credentials
OPENAI_API_KEY=your_openai_api_key

# Odoo Credentials
ODOO_URL=your_odoo_url
ODOO_DB=your_database_name
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
```

## Usage

### Command Line Interface
```bash
# Generate and post a tweet
python -m src.presentation.cli twitter

# Generate and post a Facebook publication
python -m src.presentation.cli facebook

# Generate and post a LinkedIn post
python -m src.presentation.cli linkedin

# Generate and post a blog article (Coming soon)
python -m src.presentation.cli blog
```

## Development

### Running Tests
```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/path/to/test_file.py

# Run tests in verbose mode
python -m pytest -v
```

### Code Style
The project follows PEP 8 guidelines. Install development dependencies and run:
```bash
# Check code style
flake8 src tests

# Sort imports
isort src tests
```

## Documentation
- API documentation is available in the `docs/` directory
- For detailed implementation guides, see `docs/implementation/`
- For contribution guidelines, see `CONTRIBUTING.md`

## Architecture

### Key Components
1. **Domain Layer**
   - Business entities
   - Business rules
   - Exception handling

2. **Infrastructure Layer**
   - External service integrations
   - Configuration management
   - Logging and monitoring

3. **Interfaces Layer**
   - Gateway interfaces
   - Service contracts
   - Data transfer objects

4. **Use Cases Layer**
   - Business logic implementation
   - Command handling
   - Service orchestration

5. **Presentation Layer**
   - Command-line interface
   - User interaction
   - Output formatting

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Project Link: [https://github.com/yourusername/automator](https://github.com/yourusername/automator)

## Acknowledgments
- OpenAI GPT Models
- Twitter API
- Facebook Graph API
- LinkedIn API
- Odoo API