import argparse
import os

import pandas as pd

from xtweetcollector import get_twitter_comments
from youtube_comment_collector import get_youtube_comments


def collect(hashtag: str, max_results: int, youtube_api_key: str | None):
    twitter_df = get_twitter_comments(hashtag, max_results)

    youtube_df = (
        get_youtube_comments(youtube_api_key, hashtag, max_results)
        if youtube_api_key
        else pd.DataFrame()
    )

    return twitter_df, youtube_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collect social data for a hashtag (Twitter via snscrape, YouTube via API key)."
    )
    parser.add_argument("hashtag", help="Hashtag without #")
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum items per platform.",
    )
    parser.add_argument(
        "--youtube-api-key",
        default=os.getenv("YOUTUBE_API_KEY"),
        help="YouTube Data API key; set env YOUTUBE_API_KEY to avoid passing this.",
    )
    parser.add_argument(
        "--twitter-output",
        default="twitter_hashtag.csv",
        help="CSV path for Twitter data.",
    )
    parser.add_argument(
        "--youtube-output",
        default="youtube_comments.csv",
        help="CSV path for YouTube data.",
    )

    args = parser.parse_args()

    twitter_df, youtube_df = collect(
        args.hashtag, args.max_results, args.youtube_api_key
    )

    if not twitter_df.empty:
        twitter_df.to_csv(args.twitter_output, index=False)
        print(f"Saved {len(twitter_df)} tweets to {args.twitter_output}")
    else:
        print("No Twitter data collected.")

    if args.youtube_api_key:
        if not youtube_df.empty:
            youtube_df.to_csv(args.youtube_output, index=False)
            print(f"Saved {len(youtube_df)} comments to {args.youtube_output}")
        else:
            print("No YouTube comments collected (check quota/hashtag).")
    else:
        print("Skipped YouTube collection (no API key provided).")

