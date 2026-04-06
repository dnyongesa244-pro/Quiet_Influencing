Social Media Collector & Consumer Behavior Suite
A modular Python toolkit for high-volume data collection from YouTube and x to analyze digital influence and consumer trends.

🚀 Key Features
Multi-Platform: Specialized modules for YouTube (API v3) and Twitter (snscrape/Tweepy).

Analytical Layers: Integrated scripts for Sentiment Analysis and Network Analysis to map consumer behavior.

Operations-Ready: Fully configurable via CLI with verbose logging for debugging data pipelines.

🛠️ Installation & Setup
Environment Setup (Recommended)

Bash
conda create -n socialenv python=3.10
conda activate socialenv
Clone & Install

Bash
git clone https://github.com/dnyongesa244-pro/Quiet_Influencing.git
cd social-media-collector
pip install -r requirements.txt
Configuration
Set your environment variables for seamless API access:

Bash
export YOUTUBE_API_KEY="your_key_here"
export TWITTER_BEARER_TOKEN="your_token_here"
📊 Usage
Data Collection
To test the YouTube collector for a specific brand or keyword:

Bash
python youtube_collector.py "BrandName" --max-comments 5 --max-videos 1 --verbose
Behavioral Analysis
Once data is collected, run the analysis pipeline:

Bash
# Analyze consumer sentiment
python youtube_sentiment_analysis.py

# Map influencer networks
python youtube_network_analysis.py
