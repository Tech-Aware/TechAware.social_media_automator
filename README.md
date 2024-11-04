# Automator

Automator is a Python application that allows users to generate and post content across multiple platforms using OpenAI's GPT model. It supports blog article generation, social media posts, and automated publication.

## Features

- Generate and publish blog articles using OpenAI's GPT model
- Generate and post tweets using OpenAI's GPT model
- Generate and post Facebook content using OpenAI's GPT model
- Command-line interface for easy interaction
- Robust error handling and logging
- Multi-platform content coordination

## System Architecture

The application follows a clean architecture pattern, divided into the following layers:

1. Presentation Layer (CLI)
2. Application Layer (Use Cases)
3. Domain Layer (Entities)
4. Interface Layer (Gateways)
5. Infrastructure Layer (External APIs, Logging, Configuration)

![Automator System Architecture](./docs/Automator_System_Architecture.png)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Tech-Aware/automator.git
   cd automator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   # Twitter Configuration
   CONSUMER_KEY=your_twitter_consumer_key
   CONSUMER_SECRET=your_twitter_consumer_secret
   ACCESS_TOKEN=your_twitter_access_token
   ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key

   # Facebook Configuration
   FACEBOOK_APP_ID=your_facebook_app_id
   FACEBOOK_APP_SECRET=your_facebook_app_secret
   FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
   FACEBOOK_PAGE_ID=your_facebook_page_id

   # Odoo Configuration
   ODOO_URL=your_odoo_url
   ODOO_DB=your_database_name
   ODOO_USERNAME=your_username
   ODOO_PASSWORD=your_password
   ODOO_BLOG_ID=your_blog_id
   ```

## Usage

Run the application using the following command:

```
python main.py
```

The application will present you with options to:
1. Generate and publish a blog article
2. Generate and post social media content

For blog articles, you can:
- Provide a topic
- Review generated content
- Choose to publish or save as draft
- Optionally create coordinated social media posts

For social media posts:
- Content is automatically generated and posted to configured platforms
- Progress is shown in real-time

## Project Structure

```
automator/
├── .venv/
├── docs/
│   ├── Automator_System_Architecture.png
│   └── guides/
│       ├── blog_feature_guide.md
│       └── social_media_guide.md
├── resources/
│   └── prompts/
│       ├── techaware_pro_prompt_for_x.txt
│       ├── techaware_pro_prompt_for_facebook.txt
│       └── techaware_pro_prompt_for_blog.txt
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── tweet.py
│   │   │   ├── blog_article.py
│   │   │   └── facebook_publication.py
│   │   ├── __init__.py
│   │   └── exceptions.py
│   ├── infrastructure/
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── environment.py
│   │   │   ├── environment_openai.py
│   │   │   ├── environment_twitter.py
│   │   │   ├── environment_facebook.py
│   │   │   └── environment_odoo.py
│   │   ├── external/
│   │   │   ├── __init__.py
│   │   │   ├── openai_api.py
│   │   │   ├── twitter_api.py
│   │   │   ├── facebook_api.py
│   │   │   └── odoo_api.py
[Project structure continues as before, with new files added]
```

## Running Tests

Run all tests with:
```bash
python -m pytest
```

Run specific test files:
```bash
python -m pytest tests/path/to/test_file.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Error Handling

The application includes comprehensive error handling for:
- Platform API errors (Twitter, Facebook, Odoo)
- Content generation errors
- Validation errors
- Configuration errors

All errors are logged with appropriate detail level in the logs directory.

## License

This project is licensed under the MIT License.