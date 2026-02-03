#!/usr/bin/env python3
"""
Daily AI and OpenClaw News Digest Script
This script gathers recent news on AI developments and OpenClaw updates
and sends them to Telegram using OpenClaw's messaging system.
"""

import json
import datetime
import re
from typing import List, Dict
from urllib.parse import urlparse

# Import required libraries (will need to install if not available)
try:
    import feedparser  # For RSS feeds
    import requests    # For general HTTP requests
except ImportError:
    print("Required packages not found. Install with: pip install feedparser requests")
    exit(1)


def load_config():
    """Load configuration settings from config file"""
    try:
        with open('news_digest_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default config if file doesn't exist
        return {
            "enabled": True,
            "sources": [
                {"name": "OpenClaw Releases", "url": "https://api.github.com/repos/openclaw/openclaw/releases"},
                {"name": "AI News - TechCrunch", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
                {"name": "AI News - Ars Technica", "url": "https://arstechnica.com/tag/artificial-intelligence/feed/"},
                {"name": "AI News - X/Twitter", "url": "https://x.com/search?q=artificial%20intelligence%20OR%20AI%20OR%20machine%20learning%20lang%3Aen&src=typed_query"},
                {"name": "AI Videos - YouTube", "url": "https://www.youtube.com/feed/trending?gl=US&hl=en&category=28"}
            ],
            "delivery_time": "09:00",
            "max_items": 10
        }


def save_config(config):
    """Save configuration settings"""
    with open('news_digest_config.json', 'w') as f:
        json.dump(config, f, indent=2)


def fetch_github_releases(url: str) -> List[Dict]:
    """Fetch OpenClaw releases from GitHub API"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        releases = response.json()
        
        items = []
        for release in releases[:3]:  # Get latest 3 releases
            items.append({
                "title": release.get("name", "No title"),
                "source": "OpenClaw GitHub",
                "date": release.get("published_at", "")[:10],
                "summary": release.get("body", "No description available")[:200] + "..."
            })
        return items
    except Exception as e:
        print(f"Error fetching GitHub releases: {e}")
        return []


def fetch_rss_feed(url: str, source_name: str) -> List[Dict]:
    """Fetch news from RSS feed sources like TechCrunch, Ars Technica"""
    try:
        feed = feedparser.parse(url)
        items = []
        
        for entry in feed.entries[:3]:  # Get latest 3 entries
            items.append({
                "title": entry.title,
                "source": source_name,
                "date": entry.published.split('T')[0] if hasattr(entry, 'published') else str(datetime.date.today()),
                "summary": entry.summary if hasattr(entry, 'summary') else "No summary available"
            })
        return items
    except Exception as e:
        print(f"Error fetching RSS feed from {url}: {e}")
        return []


def fetch_twitter_content(url: str) -> List[Dict]:
    """Fetch AI-related content from Twitter/X (placeholder implementation)"""
    # NOTE: Twitter/X API requires authentication, so this is a simplified version
    # In a production environment, you would need to use the Twitter API with proper authentication
    try:
        # This is a placeholder - actual implementation would require Twitter API access
        return [{
            "title": "Twitter/X AI Discussions",
            "source": "X/Twitter",
            "date": str(datetime.date.today()),
            "summary": "Recent discussions about AI on X/Twitter platform. (Requires Twitter API for actual implementation)"
        }]
    except Exception as e:
        print(f"Error fetching Twitter content: {e}")
        return []


def fetch_youtube_content(url: str) -> List[Dict]:
    """Fetch trending AI videos from YouTube (placeholder implementation)"""
    # NOTE: YouTube API requires API key, so this is a simplified version
    # In a production environment, you would need to use the YouTube Data API
    try:
        # This is a placeholder - actual implementation would require YouTube API access
        return [{
            "title": "YouTube AI Videos",
            "source": "YouTube",
            "date": str(datetime.date.today()),
            "summary": "Trending AI-related videos on YouTube. (Requires YouTube API for actual implementation)"
        }]
    except Exception as e:
        print(f"Error fetching YouTube content: {e}")
        return []


def gather_ai_news() -> List[Dict]:
    """Gather recent AI news from various sources"""
    config = load_config()
    all_news = []
    
    for source in config.get("sources", []):
        source_name = source["name"]
        url = source["url"]
        parsed_url = urlparse(url)
        
        if "github.com" in parsed_url.netloc:
            all_news.extend(fetch_github_releases(url))
        elif "techcrunch.com" in parsed_url.netloc or "arstechnica.com" in parsed_url.netloc:
            all_news.extend(fetch_rss_feed(url, source_name))
        elif "x.com" in parsed_url.netloc or "twitter.com" in parsed_url.netloc:
            all_news.extend(fetch_twitter_content(url))
        elif "youtube.com" in parsed_url.netloc:
            all_news.extend(fetch_youtube_content(url))
        else:
            print(f"Unsupported source type for: {url}")
    
    # Sort by date (most recent first) and limit to max_items
    sorted_news = sorted(all_news, key=lambda x: x['date'], reverse=True)
    max_items = config.get("max_items", 10)
    return sorted_news[:max_items]


def format_telegram_message(news_items: List[Dict]) -> str:
    """Format news items for Telegram delivery"""
    header = f"*Daily AI & OpenClaw Digest*\n_{datetime.date.today().strftime('%B %d, %Y')}_\n\n"
    
    if not news_items:
        return header + "No new items found today."
    
    formatted_items = []
    for i, item in enumerate(news_items):
        formatted_item = (
            f"*{i+1}. {item['title']}*\n"
            f"_Source: {item['source']} | {item['date']}_\n"
            f"{item['summary']}\n\n"
        )
        formatted_items.append(formatted_item)
    
    return header + "".join(formatted_items)


def send_to_telegram(message: str):
    """Send the formatted message to Telegram using OpenClaw's messaging system"""
    # This function will be called from within the OpenClaw environment
    # where the message tool is available
    import sys
    import os
    
    # Add the workspace directory to the path
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, workspace_dir)
    
    try:
        # Since this script will be executed within OpenClaw's environment,
        # we'll use the message tool that's available in this context
        from openclaw.core.tools.message import message_tool
        
        result = message_tool({
            "action": "send",
            "channel": "telegram",
            "to": 8273779429,  # Your chat ID
            "message": message
        })
        
        if result and result.get("ok"):
            print("✅ Successfully sent news digest to Telegram!")
            return True
        else:
            print(f"❌ Failed to send news digest to Telegram: {result}")
            return False
            
    except ImportError:
        print("❌ Unable to import OpenClaw's message tool. This script must be run within OpenClaw's environment.")
        return False
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")
        return False


def main():
    """Main function to run the daily digest"""
    config = load_config()
    
    if not config.get("enabled", False):
        print("News digest is currently disabled. To enable, set 'enabled': true in news_digest_config.json")
        return
    
    try:
        news_items = gather_ai_news()
        telegram_message = format_telegram_message(news_items)
        
        # In the OpenClaw environment, this will be handled by the calling system
        # which has access to the message tool
        print("DIGEST_READY")
        print(telegram_message)
        
        # For testing purposes when run directly:
        # print("Would send to Telegram:", telegram_message[:200], "...")
        
    except Exception as e:
        print(f"Error processing daily digest: {e}")


if __name__ == "__main__":
    main()