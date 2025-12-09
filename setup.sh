#!/bin/bash
# setup.sh

echo "Setting up Social Media Collector..."
echo "====================================="

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your API keys."
    else
        echo "❌ .env.example not found. Creating empty .env file..."
        echo "# Social Media Collector Configuration" > .env
        echo "# Add your API keys here" >> .env
        echo "" >> .env
        echo "YOUTUBE_API_KEY=your_key_here" >> .env
        echo "" >> .env
        echo "# Twitter API (optional)" >> .env
        echo "TWITTER_BEARER_TOKEN=your_token_here" >> .env
        echo "TWITTER_CONSUMER_KEY=your_consumer_key" >> .env
        echo "TWITTER_CONSUMER_SECRET=your_consumer_secret" >> .env
        echo "TWITTER_ACCESS_TOKEN=your_access_token" >> .env
        echo "TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret" >> .env
        echo "✅ Created .env file template. Please edit it with your API keys."
    fi
else
    echo "✅ .env file already exists."
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create output directory
mkdir -p collected_data

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Test with: python social_collector.py python --max-comments 10"
echo ""