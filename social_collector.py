#!/usr/bin/env python3
"""
Social Media Collector - Main Orchestrator
Twitter functionality temporarily disabled for YouTube testing
"""

import os
import sys
import argparse
import pandas as pd
from datetime import datetime
from pathlib import Path

# Import configuration
from config import config

# Import individual collectors
try:
    from youtube_collector import YouTubeCollector
    # Twitter collector temporarily disabled
    # from twitter_collector import TwitterCollector
except ImportError as e:
    print(f"Error importing collectors: {e}")
    print("Make sure youtube_collector.py is in the same directory.")
    sys.exit(1)


class SocialMediaOrchestrator:
    def __init__(self):
        """Initialize the orchestrator with settings from config"""
        self.collectors = {}
        
        # Ensure output directory exists
        config.ensure_output_dir()
        
        print("\n" + "="*60)
        print("INITIALIZING SOCIAL MEDIA COLLECTOR")
        print("NOTE: Twitter functionality is temporarily disabled")
        print("Testing YouTube collector first")
        print("="*60)
    
    def _init_youtube_collector(self, api_key=None):
        """Initialize YouTube collector"""
        try:
            api_key = api_key or config.YOUTUBE_API_KEY
            self.collectors['youtube'] = YouTubeCollector(api_key=api_key)
            print("✓ YouTube collector ready")
            return True
        except Exception as e:
            print(f"✗ Failed to initialize YouTube collector: {e}")
            return False
    
    def _init_twitter_collector(self, method='auto', bearer_token=None):
        """Initialize Twitter collector - TEMPORARILY DISABLED"""
        print("⚠️ Twitter collector is temporarily disabled for testing")
        print("⚠️ Will be enabled after YouTube testing is complete")
        return False
    
    def collect(self, hashtag, platforms=None, **kwargs):
        """
        Collect data from specified platforms
        
        Args:
            hashtag: Hashtag to search for
            platforms: List of platforms to collect from
            **kwargs: Additional parameters for collectors
        
        Returns:
            Dictionary with platform DataFrames
        """
        # Use config defaults if not specified
        platforms = platforms or config.DEFAULT_PLATFORMS
        
        # Remove 'twitter' from platforms if included (temporarily disabled)
        if 'twitter' in platforms:
            print("\n⚠️  Twitter collection is temporarily disabled")
            print("⚠️  Testing YouTube first, then will enable Twitter")
            platforms = [p for p in platforms if p != 'twitter']
        
        if not platforms:
            print("No platforms available for collection.")
            return {}
        
        results = {}
        
        print(f"\n{'='*60}")
        print(f"COLLECTING DATA FOR: #{hashtag}")
        print(f"PLATFORMS: {', '.join(platforms)} (Twitter disabled for now)")
        print('='*60)
        
        # YouTube collection
        if 'youtube' in platforms:
            if 'youtube' not in self.collectors:
                if not self._init_youtube_collector(kwargs.get('youtube_api_key')):
                    print("Skipping YouTube collection")
                    platforms.remove('youtube')
            
            if 'youtube' in platforms:
                print(f"\n📹 COLLECTING FROM YOUTUBE...")
                try:
                    youtube_df = self.collectors['youtube'].get_comments_by_hashtag(
                        hashtag=hashtag,
                        max_comments=kwargs.get('youtube_max_comments', config.DEFAULT_MAX_RESULTS),
                        max_videos=kwargs.get('youtube_max_videos', 10),
                        include_replies=kwargs.get('youtube_include_replies', config.INCLUDE_REPLIES)
                    )
                    results['youtube'] = youtube_df
                    print(f"✅ YouTube: Collected {len(youtube_df)} comments")
                except Exception as e:
                    print(f"❌ YouTube collection failed: {e}")
                    results['youtube'] = pd.DataFrame()
        
        # Twitter collection - TEMPORARILY DISABLED
        if 'twitter' in platforms:
            print(f"\n🐦 TWITTER COLLECTION TEMPORARILY DISABLED")
            print("Will be enabled after YouTube testing")
            results['twitter'] = pd.DataFrame()
        
        return results
    
    def save_results(self, results, hashtag, separate_files=True):
        """
        Save collection results
        
        Args:
            results: Dictionary with platform DataFrames
            hashtag: Original hashtag
            separate_files: Save each platform to separate file
        
        Returns:
            List of saved file paths
        """
        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if separate_files:
            # Save each platform separately
            for platform, df in results.items():
                if df is not None and not df.empty:
                    filename = os.path.join(config.OUTPUT_DIR, f"{platform}_{hashtag}_{timestamp}.csv")
                    df.to_csv(filename, index=False, encoding='utf-8')
                    saved_files.append(filename)
                    print(f"💾 Saved {len(df)} {platform} items to {filename}")
        else:
            # Combine all platforms into one file
            all_data = []
            for platform, df in results.items():
                if df is not None and not df.empty:
                    all_data.append(df)
            
            if all_data:
                combined_df = pd.concat(all_data, ignore_index=True)
                filename = os.path.join(config.OUTPUT_DIR, f"social_media_{hashtag}_{timestamp}.csv")
                combined_df.to_csv(filename, index=False, encoding='utf-8')
                saved_files.append(filename)
                print(f"💾 Saved {len(combined_df)} total items to {filename}")
        
        return saved_files


def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(
        description="Collect social media data (Twitter temporarily disabled)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s python
  %(prog)s machinelearning --youtube-max-comments 200
  
Note: Twitter collection is temporarily disabled for YouTube testing.
      Test YouTube first, then Twitter will be enabled.
        """
    )
    
    parser.add_argument("hashtag", help="Hashtag to search for (without #)")
    
    # Platform selection
    parser.add_argument(
        "--platforms",
        default="youtube",  # Only youtube by default for now
        help="Platforms to collect from (default: youtube, twitter is disabled)"
    )
    
    # YouTube parameters
    parser.add_argument(
        "--youtube-api-key",
        help="YouTube API key (overrides .env)"
    )
    
    parser.add_argument(
        "--youtube-max-comments",
        type=int,
        default=config.DEFAULT_MAX_RESULTS,
        help=f"Maximum YouTube comments (default: {config.DEFAULT_MAX_RESULTS})"
    )
    
    parser.add_argument(
        "--youtube-max-videos",
        type=int,
        default=10,
        help="Maximum YouTube videos to process (default: 10)"
    )
    
    parser.add_argument(
        "--youtube-include-replies",
        action="store_true",
        default=config.INCLUDE_REPLIES,
        help="Include YouTube comment replies"
    )
    
    parser.add_argument(
        "--youtube-no-replies",
        dest="youtube_include_replies",
        action="store_false",
        help="Exclude YouTube comment replies"
    )
    
    # Output options
    parser.add_argument(
        "--output-dir",
        default=config.OUTPUT_DIR,
        help=f"Output directory (default: {config.OUTPUT_DIR})"
    )
    
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Save all platforms to one combined file"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Parse platforms
    platforms = [p.strip().lower() for p in args.platforms.split(',')]
    valid_platforms = ['youtube']  # Only youtube for now
    
    # Filter out any 'twitter' mentions
    platforms = [p for p in platforms if p in valid_platforms]
    
    if not platforms:
        print("ERROR: No valid platforms specified. Use: youtube")
        sys.exit(1)
    
    # Show configuration
    config.print_config_summary()
    
    # Validate required API keys
    errors = config.validate()
    if 'youtube' in platforms and 'youtube_api' in errors and not args.youtube_api_key:
        print("ERROR: YouTube API key is required for YouTube collection.")
        print("Set YOUTUBE_API_KEY in .env file or use --youtube-api-key")
        sys.exit(1)
    
    try:
        # Initialize orchestrator
        orchestrator = SocialMediaOrchestrator()
        
        # Collect data
        results = orchestrator.collect(
            hashtag=args.hashtag,
            platforms=platforms,
            youtube_api_key=args.youtube_api_key,
            youtube_max_comments=args.youtube_max_comments,
            youtube_max_videos=args.youtube_max_videos,
            youtube_include_replies=args.youtube_include_replies,
        )
        
        # Save results
        saved_files = orchestrator.save_results(
            results=results,
            hashtag=args.hashtag,
            separate_files=not args.combined
        )
        
        if saved_files:
            print(f"\n{'='*60}")
            print("✅ YOUTUBE COLLECTION COMPLETE!")
            print("Twitter testing will follow after YouTube verification")
            print(f"Saved {len(saved_files)} file(s):")
            for file in saved_files:
                print(f"  📄 {os.path.basename(file)}")
            
            # Summary
            total_items = sum(len(df) for df in results.values() if df is not None)
            print(f"\n📊 Total items collected: {total_items:,}")
            for platform, df in results.items():
                if df is not None and not df.empty:
                    print(f"  • {platform.capitalize()}: {len(df):,} items")
            print('='*60)
        else:
            print("\n❌ No data was collected.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Collection interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during collection: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()