import os
import argparse
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_youtube_comments(api_key, hashtag, max_results=100):
    """
    Collect comments from YouTube videos with a specific hashtag
    
    Args:
        api_key: YouTube Data API v3 key
        hashtag: Hashtag to search for (without #)
        max_results: Maximum number of comments to collect
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    comments_data = []
    
    try:
        # Search for videos with the hashtag
        search_response = youtube.search().list(
            q=f'#{hashtag}',
            part='snippet',
            type='video',
            maxResults=50
        ).execute()
        
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        for video_id in video_ids:
            try:
                # Get video comments
                comments_response = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=min(100, max_results - len(comments_data)),
                    textFormat='plainText'
                ).execute()
                
                for item in comments_response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    
                    comments_data.append({
                        'platform': 'YouTube',
                        'video_id': video_id,
                        'comment_id': item['id'],
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'likes': comment.get('likeCount', 0),
                        'published_at': comment['publishedAt'],
                        'updated_at': comment.get('updatedAt', ''),
                        'parent_id': ''
                    })
                    
                    # Get replies if they exist
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            reply_snippet = reply['snippet']
                            comments_data.append({
                                'platform': 'YouTube',
                                'video_id': video_id,
                                'comment_id': reply['id'],
                                'author': reply_snippet['authorDisplayName'],
                                'text': reply_snippet['textDisplay'],
                                'likes': reply_snippet.get('likeCount', 0),
                                'published_at': reply_snippet['publishedAt'],
                                'updated_at': reply_snippet.get('updatedAt', ''),
                                'parent_id': item['id']
                            })
                    
                    if len(comments_data) >= max_results:
                        break
                        
            except HttpError as e:
                print(f"Error fetching comments for video {video_id}: {e}")
                continue
                
            if len(comments_data) >= max_results:
                break
                
    except HttpError as e:
        print(f"Search error: {e}")
        
    return pd.DataFrame(comments_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collect YouTube comments for videos matching a hashtag."
    )
    parser.add_argument("hashtag", help="Hashtag without #")
    parser.add_argument(
        "--api-key",
        default=os.getenv("YOUTUBE_API_KEY"),
        help="YouTube Data API key (or set YOUTUBE_API_KEY env var)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum comments to collect (across videos).",
    )
    parser.add_argument(
        "--output",
        default="youtube_comments.csv",
        help="Path to CSV output (default: youtube_comments.csv)",
    )

    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit(
            "YouTube API key is required. Provide --api-key or set YOUTUBE_API_KEY."
        )

    df = get_youtube_comments(args.api_key, args.hashtag, args.max_results)
    df.to_csv(args.output, index=False)
    print(f"Saved {len(df)} comments to {args.output}")