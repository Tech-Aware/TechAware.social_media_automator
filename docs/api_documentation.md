# API Documentation

## Overview
The TechAware Social Media Automator exposes several API endpoints through its gateway interfaces, allowing interaction with various social media platforms and content generation services.

## Gateway Interfaces

### OpenAI Gateway
Interface for generating content using OpenAI's APIs.

```python
def generate(prompt: str) -> str:
    """
    Generate content based on the provided prompt.
    
    Args:
        prompt (str): The input prompt for content generation
        
    Returns:
        str: The generated content
        
    Raises:
        OpenAIError: If content generation fails
    """
```

### Social Media Gateways

#### Twitter Gateway
```python
def post_tweet(tweet: Tweet) -> dict:
    """
    Post a tweet to Twitter.
    
    Args:
        tweet (Tweet): The Tweet entity to post
        
    Returns:
        dict: Response from Twitter API
        
    Raises:
        TwitterError: If posting fails
    """
```

#### Facebook Gateway
```python
def post(publication: FacebookPublication) -> dict:
    """
    Post a publication to Facebook.
    
    Args:
        publication (FacebookPublication): The publication to post
        
    Returns:
        dict: Response from Facebook API
        
    Raises:
        FacebookError: If posting fails
    """
```

#### LinkedIn Gateway
```python
def post(publication: LinkedInPublication) -> dict:
    """
    Post a publication to LinkedIn.
    
    Args:
        publication (LinkedInPublication): The publication to post
        
    Returns:
        dict: Response from LinkedIn API
        
    Raises:
        LinkedInError: If posting fails
    """
```

## Entities

### Tweet
Represents a tweet with validation logic.

**Properties**:
- text (str): The tweet content

**Methods**:
- validate(): Ensures tweet meets Twitter's requirements
- get_text(): Returns the tweet text
- set_text(new_text): Updates the tweet text

### FacebookPublication
Represents a Facebook post with validation logic.

**Properties**:
- text (str): The publication content
- privacy (str): Privacy setting ("PUBLIC", "FRIENDS", "ONLY_ME")

**Methods**:
- validate(): Ensures publication meets Facebook's requirements
- get_text(): Returns the publication text
- set_text(new_text): Updates the publication text
- get_privacy(): Returns the privacy setting
- set_privacy(new_privacy): Updates the privacy setting

### LinkedInPublication
Represents a LinkedIn post with validation logic.

**Properties**:
- text (str): The publication content

**Methods**:
- validate(): Ensures publication meets LinkedIn's requirements
- get_text(): Returns the publication text