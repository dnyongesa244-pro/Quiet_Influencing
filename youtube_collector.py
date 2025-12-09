#!/usr/bin/env python3
"""
YouTube Comments Collector
Now uses config.py for API keys
"""

import os
import sys
import argparse
import pandas as pd
import time
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import configuration
from config import config


class YouTubeCollector:
    def __init__(self, api_key=None):
        """
        Initialize YouTube collector
        
        Args:
            api_key: YouTube Data API v3 key (optional, uses config if not provided)
        """
        # Use provided API key or get from config
        self.api_key = api_key or config.YOUTUBE_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "YouTube API key is required. "
                "Set it in .env file or provide via --api-key"
            )
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.total_requests = 0
        self.request_delay = config.YOUTUBE_REQUEST_DELAY
    
    def _make_request(self, request_func, **kwargs):
        """Helper method to make API requests with rate limiting"""
        self.total_requests += 1
        
        # Rate limiting
        time.sleep(self.request_delay)
        
        # Log every 10th request
        if self.total_requests % 10 == 0:
            print(f"  Made {self.total_requests} API requests...")
        
        return request_func(**kwargs).execute()
    
    def search_videos_by_hashtag(self, hashtag, max_videos=50):
        """
        Search for videos containing a specific hashtag
        """
        print(f"Searching for videos with hashtag: #{hashtag}")
        
        try:
            search_response = self._make_request(
                self.youtube.search().list,
                q=f'#{hashtag}',
                part='snippet',
                type='video',
                maxResults=min(50, max_videos),
                order='relevance'
            )
            
            video_ids = []
            for item in search_response.get('items', []):
                if 'videoId' in item['id']:
                    video_ids.append(item['id']['videoId'])
            
            print(f"Found {len(video_ids)} videos for #{hashtag}")
            
            # Get video details for the found videos
            if video_ids:
                video_details = self.get_video_details(video_ids)
                for video_id, details in video_details.items():
                    print(f"  • {details['title'][:50]}... (Views: {details['views']:,})")
            
            return video_ids
            
        except HttpError as e:
            print(f"Error searching videos: {e}")
            return []
    
    def get_video_details(self, video_ids):
        """
        Get details for a list of video IDs
        """
        if not video_ids:
            return {}
        
        try:
            video_details = {}
            
            # Process in batches of 50 (YouTube API limit)
            for i in range(0, len(video_ids), 50):
                batch = video_ids[i:i+50]
                
                response = self._make_request(
                    self.youtube.videos().list,
                    part='snippet,statistics',
                    id=','.join(batch)
                )
                
                for item in response.get('items', []):
                    video_details[item['id']] = {
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'channel_title': item['snippet']['channelTitle'],
                        'published_at': item['snippet']['publishedAt'],
                        'views': int(item['statistics'].get('viewCount', 0)),
                        'likes': int(item['statistics'].get('likeCount', 0)),
                        'comments': int(item['statistics'].get('commentCount', 0))
                    }
            
            return video_details
            
        except HttpError as e:
            print(f"Error getting video details: {e}")
            return {}
    
    def get_video_comments(self, video_id, max_comments=100, include_replies=None):
        """
        Get comments for a specific video
        """
        # Use config default if not specified
        if include_replies is None:
            include_replies = config.INCLUDE_REPLIES
        
        comments_data = []
        
        try:
            video_details = self.get_video_details([video_id])
            video_info = video_details.get(video_id, {})
            
            request = self.youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                maxResults=min(100, max_comments),
                textFormat='plainText'
            )
            
            while request and len(comments_data) < max_comments:
                response = self._make_request(lambda: request)
                
                for item in response.get('items', []):
                    comment = item['snippet']['topLevelComment']['snippet']
                    
                    comments_data.append({
                        'platform': 'YouTube',
                        'video_id': video_id,
                        'video_title': video_info.get('title', 'Unknown'),
                        'video_views': video_info.get('views', 0),
                        'channel_title': video_info.get('channel_title', 'Unknown'),
                        'comment_id': item['id'],
                        'parent_id': '',
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'likes': comment.get('likeCount', 0),
                        'published_at': comment['publishedAt'],
                        'updated_at': comment.get('updatedAt', ''),
                        'is_reply': False,
                        'collected_at': datetime.now().isoformat(),
                        'hashtag_query': f'#{self.current_hashtag}' if hasattr(self, 'current_hashtag') else ''
                    })
                    
                    if include_replies and 'replies' in item:
                        for reply in item['replies']['comments']:
                            reply_snippet = reply['snippet']
                            
                            comments_data.append({
                                'platform': 'YouTube',
                                'video_id': video_id,
                                'video_title': video_info.get('title', 'Unknown'),
                                'video_views': video_info.get('views', 0),
                                'channel_title': video_info.get('channel_title', 'Unknown'),
                                'comment_id': reply['id'],
                                'parent_id': item['id'],
                                'author': reply_snippet['authorDisplayName'],
                                'text': reply_snippet['textDisplay'],
                                'likes': reply_snippet.get('likeCount', 0),
                                'published_at': reply_snippet['publishedAt'],
                                'updated_at': reply_snippet.get('updatedAt', ''),
                                'is_reply': True,
                                'collected_at': datetime.now().isoformat(),
                                'hashtag_query': f'#{self.current_hashtag}' if hasattr(self, 'current_hashtag') else ''
                            })
                    
                    if len(comments_data) >= max_comments:
                        break
                
                if 'nextPageToken' in response and len(comments_data) < max_comments:
                    request = self.youtube.commentThreads().list(
                        part='snippet,replies',
                        videoId=video_id,
                        pageToken=response['nextPageToken'],
                        maxResults=min(100, max_comments - len(comments_data)),
                        textFormat='plainText'
                    )
                else:
                    request = None
            
            return comments_data
            
        except HttpError as e:
            if e.resp.status == 403 and 'commentsDisabled' in str(e):
                print(f"Comments disabled for video {video_id}")
            elif e.resp.status == 404:
                print(f"Video {video_id} not found")
            else:
                print(f"Error fetching comments: {e}")
            return comments_data
    
    def get_comments_by_hashtag(self, hashtag, max_comments=None, max_videos=None, include_replies=None):
        """
        Main method to get comments from videos matching a hashtag
        """
        # Use config defaults if not specified
        max_comments = max_comments or config.DEFAULT_MAX_RESULTS
        max_videos = max_videos or 10
        include_replies = include_replies if include_replies is not None else config.INCLUDE_REPLIES
        
        # Store hashtag for metadata
        self.current_hashtag = hashtag
        
        print(f"\n{'='*60}")
        print(f"Starting YouTube collection for #{hashtag}")
        print(f"Maximum comments: {max_comments:,}")
        print(f"Maximum videos: {max_videos}")
        print(f"Include replies: {include_replies}")
        print('='*60)
        
        all_comments = []
        
        video_ids = self.search_videos_by_hashtag(hashtag, max_videos)
        
        if not video_ids:
            print("No videos found for the given hashtag.")
            return pd.DataFrame()
        
        for i, video_id in enumerate(video_ids[:max_videos]):
            print(f"\nProcessing video {i+1}/{min(len(video_ids), max_videos)} (ID: {video_id})")
            
            comments = self.get_video_comments(
                video_id=video_id,
                max_comments=max_comments - len(all_comments),
                include_replies=include_replies
            )
            
            all_comments.extend(comments)
            print(f"  Collected {len(comments)} comments (Total: {len(all_comments)})")
            
            if len(all_comments) >= max_comments:
                print(f"Reached maximum comments limit ({max_comments})")
                break
        
        df = pd.DataFrame(all_comments)
        
        print(f"\n{'='*60}")
        print(f"Collection complete!")
        print(f"Total comments: {len(df):,}")
        print(f"Total API requests: {self.total_requests}")
        print('='*60)
        
        return df


def main():
    """Command-line interface for YouTube collector"""
    parser = argparse.ArgumentParser(
        description="Collect YouTube comments from videos matching a hashtag",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s python --max-comments 200
  %(prog)s machinelearning --max-videos 5
  %(prog)s ai --no-replies --output results.csv
        """
    )
    
    parser.add_argument("hashtag", help="Hashtag to search for (without #)")
    
    parser.add_argument(
        "--api-key",
        help="YouTube API key (overrides .env file)"
    )
    
    parser.add_argument(
        "--max-comments",
        type=int,
        default=config.DEFAULT_MAX_RESULTS,
        help=f"Maximum comments to collect (default: {config.DEFAULT_MAX_RESULTS})"
    )
    
    parser.add_argument(
        "--max-videos",
        type=int,
        default=10,
        help="Maximum videos to process (default: 10)"
    )
    
    parser.add_argument(
        "--include-replies",
        dest="include_replies",
        action="store_true",
        default=config.INCLUDE_REPLIES,
        help="Include comment replies"
    )
    
    parser.add_argument(
        "--no-replies",
        dest="include_replies",
        action="store_false",
        help="Exclude comment replies"
    )
    
    parser.add_argument(
        "--output",
        help="Output CSV file (default: youtube_[hashtag]_[timestamp].csv)"
    )
    
    parser.add_argument(
        "--output-dir",
        default=config.OUTPUT_DIR,
        help=f"Output directory (default: {config.OUTPUT_DIR})"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Print config summary
    config.print_config_summary()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Initialize collector
        collector = YouTubeCollector(api_key=args.api_key)
        
        # Collect comments
        df = collector.get_comments_by_hashtag(
            hashtag=args.hashtag,
            max_comments=args.max_comments,
            max_videos=args.max_videos,
            include_replies=args.include_replies
        )
        
        # Save results
        if not df.empty:
            if args.output:
                filename = args.output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(args.output_dir, f"youtube_{args.hashtag}_{timestamp}.csv")
            
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"\n✅ Saved {len(df)} comments to {filename}")
            
            if args.verbose:
                print("\nFirst 3 comments:")
                print(df[['author', 'text', 'likes']].head(3).to_string())
        else:
            print("\n❌ No comments collected.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()