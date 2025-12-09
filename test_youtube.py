#!/usr/bin/env python3
# test_youtube.py
"""
Test script to verify YouTube collector works correctly
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append('.')

try:
    from config import config
    from youtube_collector import YouTubeCollector
    print("✅ Imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_configuration():
    """Test configuration loading"""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION")
    print("="*60)
    
    config.print_config_summary()
    
    errors = config.validate()
    if errors:
        print("❌ Configuration test failed")
        return False
    
    print("✅ Configuration test passed")
    return True

def test_youtube_collector_small():
    """Test YouTube collector with small sample"""
    print("\n" + "="*60)
    print("TESTING YOUTUBE COLLECTOR")
    print("="*60)
    
    try:
        # Initialize collector
        collector = YouTubeCollector()
        print("✅ YouTubeCollector initialized")
        
        # Test with a small hashtag search
        test_hashtag = "python"  # Common hashtag for testing
        print(f"\nTesting with hashtag: #{test_hashtag}")
        print("Collecting 10 comments from 2 videos...")
        
        # Search for videos
        video_ids = collector.search_videos_by_hashtag(test_hashtag, max_videos=2)
        
        if not video_ids:
            print("❌ No videos found. This could mean:")
            print("   - The hashtag doesn't exist on YouTube")
            print("   - API key doesn't have proper permissions")
            print("   - Try a different hashtag like 'vlog' or 'music'")
            return False
        
        print(f"✅ Found {len(video_ids)} videos")
        
        # Get comments from first video
        if video_ids:
            print(f"\nTesting comment collection for video: {video_ids[0]}")
            comments = collector.get_video_comments(
                video_id=video_ids[0],
                max_comments=5,
                include_replies=False
            )
            
            if comments:
                print(f"✅ Successfully collected {len(comments)} comments")
                print("\nSample comments:")
                for i, comment in enumerate(comments[:3]):
                    print(f"  {i+1}. {comment['author']}: {comment['text'][:50]}...")
                return True
            else:
                print("❌ No comments collected")
                print("This could be because:")
                print("   - Comments are disabled on the video")
                print("   - Video has no comments")
                print("   - Try a different video ID")
                return False
        
    except Exception as e:
        print(f"❌ Error during YouTube test: {e}")
        return False

def test_full_collection():
    """Test full collection with minimal data"""
    print("\n" + "="*60)
    print("FULL COLLECTION TEST (Minimal)")
    print("="*60)
    
    try:
        collector = YouTubeCollector()
        
        # Use a common hashtag that should have videos
        hashtag = "tutorial"  # Common on YouTube
        
        print(f"Testing full collection for: #{hashtag}")
        print("Collecting up to 20 comments from 3 videos...")
        
        df = collector.get_comments_by_hashtag(
            hashtag=hashtag,
            max_comments=20,
            max_videos=3,
            include_replies=False
        )
        
        if not df.empty:
            print(f"\n✅ Success! Collected {len(df)} comments")
            
            # Save test results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_youtube_{hashtag}_{timestamp}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ Saved test results to: {filename}")
            
            # Show summary
            print("\n📊 Test Results Summary:")
            print(f"  Total comments: {len(df)}")
            print(f"  Unique videos: {df['video_id'].nunique()}")
            print(f"  Unique authors: {df['author'].nunique()}")
            if 'likes' in df.columns:
                print(f"  Average likes: {df['likes'].mean():.1f}")
            
            return True
        else:
            print("❌ No data collected")
            print("Try a different hashtag or check your API key permissions")
            return False
            
    except Exception as e:
        print(f"❌ Error during full collection test: {e}")
        return False

def main():
    """Run all tests"""
    print("YouTube Collector Testing")
    print("="*60)
    
    # Run tests
    tests = [
        ("Configuration", test_configuration),
        ("YouTube Collector (Small)", test_youtube_collector_small),
        ("Full Collection", test_full_collection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n▶️ Running: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nNext steps:")
        print("1. Test with other hashtags: python youtube_collector.py [hashtag]")
        print("2. Increase comment limits: python youtube_collector.py python --max-comments 100")
        print("3. When YouTube is working, we'll enable Twitter")
    else:
        print("\n⚠️ Some tests failed.")
        print("\nTroubleshooting tips:")
        print("1. Check your YouTube API key in .env file")
        print("2. Make sure YouTube Data API v3 is enabled in Google Cloud")
        print("3. Try a more common hashtag like 'music', 'vlog', 'gaming'")
        print("4. Check your API quota at: https://console.cloud.google.com/")
    
    print("="*60)

if __name__ == "__main__":
    main()