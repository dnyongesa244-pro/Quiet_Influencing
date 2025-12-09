# Social Media Collector

A modular Python tool for collecting comments and tweets from YouTube and Twitter.

## Features
- **YouTube**: Collect comments from videos matching a hashtag
- **Twitter**: Collect tweets using snscrape (free) or Tweepy API
- **Modular**: Each platform in separate files for easy debugging
- **Configurable**: Command-line options for fine-grained control

## Installation

```bash
# Clone or create project directory
mkdir social-media-collector
cd social-media-collector

# Install dependencies
pip install -r requirements.txt

# Set up API keys (optional)
export YOUTUBE_API_KEY="your_key_here"
export TWITTER_BEARER_TOKEN="your_token_here"


# testiing youtube api replace keyword with brand name
python youtube_collector.py keyword --max-comments 5 --max-videos 1 --verbose