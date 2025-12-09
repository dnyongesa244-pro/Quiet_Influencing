#!/usr/bin/env python3
"""
Utility functions for social media collection
"""

import pandas as pd
import json
import csv
from datetime import datetime
from pathlib import Path

def save_to_csv(data, filename):
    """Save data to CSV file"""
    if isinstance(data, pd.DataFrame):
        data.to_csv(filename, index=False, encoding='utf-8')
    elif isinstance(data, list):
        if data and isinstance(data[0], dict):
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
    return filename

def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename

def read_csv(filename):
    """Read CSV file into DataFrame"""
    return pd.read_csv(filename, encoding='utf-8')

def read_json(filename):
    """Read JSON file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text):
    """Basic text cleaning"""
    if not isinstance(text, str):
        return ''
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove URLs (basic)
    import re
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    return text.strip()

def format_timestamp(timestamp, format='%Y-%m-%d %H:%M:%S'):
    """Format timestamp string"""
    if not timestamp:
        return ''
    
    try:
        # Try to parse ISO format
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime(format)
    except:
        try:
            # Try other common formats
            for fmt in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                try:
                    dt = datetime.strptime(timestamp, fmt)
                    return dt.strftime(format)
                except:
                    continue
        except:
            pass
    
    return timestamp

def generate_summary(df, platform):
    """Generate summary statistics for collected data"""
    if df.empty:
        return {}
    
    summary = {
        'platform': platform,
        'total_items': len(df),
        'collection_date': datetime.now().isoformat(),
    }
    
    # Platform-specific summaries
    if platform.lower() == 'youtube':
        if 'author' in df.columns:
            summary['unique_authors'] = df['author'].nunique()
        if 'video_title' in df.columns:
            summary['unique_videos'] = df['video_title'].nunique()
        if 'likes' in df.columns:
            summary['avg_likes'] = df['likes'].mean()
            summary['max_likes'] = df['likes'].max()
    
    elif platform.lower() == 'twitter':
        if 'author_username' in df.columns:
            summary['unique_authors'] = df['author_username'].nunique()
        if 'like_count' in df.columns:
            summary['avg_likes'] = df['like_count'].mean()
            summary['max_likes'] = df['like_count'].max()
        if 'retweet_count' in df.columns:
            summary['avg_retweets'] = df['retweet_count'].mean()
    
    return summary

def merge_datasets(files, output_file):
    """Merge multiple CSV files into one"""
    dataframes = []
    
    for file in files:
        if Path(file).exists():
            df = pd.read_csv(file, encoding='utf-8')
            dataframes.append(df)
            print(f"Loaded {len(df)} rows from {file}")
        else:
            print(f"Warning: File not found: {file}")
    
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)
        merged_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ Merged {len(dataframes)} files into {output_file}")
        print(f"Total rows: {len(merged_df)}")
        return merged_df
    else:
        print("❌ No data to merge")
        return pd.DataFrame()