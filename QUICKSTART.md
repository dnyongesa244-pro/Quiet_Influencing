# YouTube Collector - Quick Start Test

## Step 1: Setup
```bash
# 1. Install dependencies
pip install pandas google-api-python-client google-auth-oauthlib python-dotenv

# 2. Create .env file
cp .env.example .env

# 3. Edit .env and add your YouTube API key
nano .env  # Add: YOUTUBE_API_KEY=your_key_here