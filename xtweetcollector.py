from datetime import datetime
from typing import Optional

import pandas as pd

try:
    import snscrape.modules.twitter as sntwitter
except ImportError:
    sntwitter = None


def get_twitter_comments(hashtag: str, max_results: int = 100) -> pd.DataFrame:
    """
    Collect tweets with a specific hashtag using snscrape (no API key needed).
    """
    if sntwitter is None:
        raise ImportError(
            "snscrape is required. Install with: pip install snscrape"
        )

    tweets_data = []
    scraper = sntwitter.TwitterHashtagScraper(hashtag)

    for tweet in scraper.get_items():
        tweets_data.append(
            {
                "platform": "Twitter",
                "tweet_id": tweet.id,
                "conversation_id": getattr(tweet, "conversationId", None),
                "author_id": tweet.user.id,
                "author_username": tweet.user.username,
                "author_name": tweet.user.displayname,
                "text": tweet.content,
                "created_at": tweet.date,
                "retweet_count": tweet.retweetCount,
                "reply_count": getattr(tweet, "replyCount", None),
                "like_count": tweet.likeCount,
                "quote_count": getattr(tweet, "quoteCount", None),
                "in_reply_to_user_id": getattr(tweet, "inReplyToUser", None),
                "in_reply_to_tweet_id": getattr(tweet, "inReplyToTweetId", None),
                "permalink": tweet.url,
            }
        )

        if len(tweets_data) >= max_results:
            break

    return pd.DataFrame(tweets_data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Collect hashtag tweets via snscrape (no API key)."
    )
    parser.add_argument("hashtag", help="Hashtag without #")
    parser.add_argument(
        "--max-results", type=int, default=100, help="Number of tweets to fetch"
    )
    parser.add_argument(
        "--output",
        default="twitter_hashtag.csv",
        help="Path to CSV output (default: twitter_hashtag.csv)",
    )

    args = parser.parse_args()
    df = get_twitter_comments(args.hashtag, args.max_results)
    df.to_csv(args.output, index=False)
    print(f"Saved {len(df)} tweets to {args.output}")