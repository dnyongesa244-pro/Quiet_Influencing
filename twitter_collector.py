#!/usr/bin/env python3
"""
Twitter (X) Tweets Collector - TEMPORARILY COMMENTED OUT
Will be enabled after YouTube testing is complete
"""

import os
import sys
import argparse
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict

# Import configuration
from config import config


class TwitterCollector:
    def __init__(self, method=None, bearer_token=None, consumer_key=None, 
                 consumer_secret=None, access_token=None, access_token_secret=None):
        """
        Initialize Twitter collector - TEMPORARILY DISABLED
        """
        print("⚠️ Twitter collector is temporarily disabled for YouTube testing")
        print("⚠️ This feature will be enabled after YouTube testing is complete")
        raise NotImplementedError("Twitter collector is temporarily disabled for testing")
    
    def collect_tweets(self, hashtag, max_tweets=None, since_date=None, until_date=None, 
                      include_retweets=None, language=None):
        """Main method to collect tweets - TEMPORARILY DISABLED"""
        print("Twitter collection is temporarily disabled")
        return pd.DataFrame()


def main():
    """Command-line interface for Twitter collector - TEMPORARILY DISABLED"""
    parser = argparse.ArgumentParser(
        description="Twitter collector - TEMPORARILY DISABLED",
        epilog="This feature will be enabled after YouTube testing"
    )
    
    parser.add_argument("hashtag", help="Hashtag to search for (without #)")
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("TWITTER COLLECTOR - TEMPORARILY DISABLED")
    print("="*60)
    print(f"\nWould have searched for: #{args.hashtag}")
    print("\n⚠️  Twitter collection is disabled for now.")
    print("⚠️  Testing YouTube collector first.")
    print("⚠️  Run: python youtube_collector.py {args.hashtag}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()