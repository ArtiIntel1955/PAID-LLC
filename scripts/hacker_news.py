#!/usr/bin/env python3
"""
Hacker News API Client for OpenClaw
Fetches top stories, newest stories, and specific story details from Hacker News
"""

import sys
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime


def get_top_stories(limit: int = 10) -> List[Dict]:
    """
    Get top stories from Hacker News
    """
    try:
        # Get top story IDs
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=10)
            story_data = story_response.json()
            
            if story_data:
                story = {
                    'id': story_data.get('id'),
                    'title': story_data.get('title', 'No title'),
                    'url': story_data.get('url', ''),
                    'score': story_data.get('score', 0),
                    'by': story_data.get('by', 'Unknown'),
                    'time': datetime.fromtimestamp(story_data.get('time', 0)).isoformat() if story_data.get('time') else '',
                    'descendants': story_data.get('descendants', 0),
                    'type': story_data.get('type', 'story'),
                    'text': story_data.get('text', '')  # For Ask HN or other text posts
                }
                stories.append(story)
        
        return stories
    except Exception as e:
        return [{'error': f'Error fetching top stories: {str(e)}'}]


def get_new_stories(limit: int = 10) -> List[Dict]:
    """
    Get newest stories from Hacker News
    """
    try:
        # Get new story IDs
        new_stories_url = "https://hacker-news.firebaseio.com/v0/newstories.json"
        response = requests.get(new_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=10)
            story_data = story_response.json()
            
            if story_data:
                story = {
                    'id': story_data.get('id'),
                    'title': story_data.get('title', 'No title'),
                    'url': story_data.get('url', ''),
                    'score': story_data.get('score', 0),
                    'by': story_data.get('by', 'Unknown'),
                    'time': datetime.fromtimestamp(story_data.get('time', 0)).isoformat() if story_data.get('time') else '',
                    'descendants': story_data.get('descendants', 0),
                    'type': story_data.get('type', 'story'),
                    'text': story_data.get('text', '')
                }
                stories.append(story)
        
        return stories
    except Exception as e:
        return [{'error': f'Error fetching new stories: {str(e)}'}]


def get_ask_stories(limit: int = 10) -> List[Dict]:
    """
    Get Ask HN stories from Hacker News
    """
    try:
        # Get Ask HN story IDs
        ask_stories_url = "https://hacker-news.firebaseio.com/v0/askstories.json"
        response = requests.get(ask_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=10)
            story_data = story_response.json()
            
            if story_data:
                story = {
                    'id': story_data.get('id'),
                    'title': story_data.get('title', 'No title'),
                    'url': story_data.get('url', ''),
                    'score': story_data.get('score', 0),
                    'by': story_data.get('by', 'Unknown'),
                    'time': datetime.fromtimestamp(story_data.get('time', 0)).isoformat() if story_data.get('time') else '',
                    'descendants': story_data.get('descendants', 0),
                    'type': story_data.get('type', 'story'),
                    'text': story_data.get('text', '')
                }
                stories.append(story)
        
        return stories
    except Exception as e:
        return [{'error': f'Error fetching Ask HN stories: {str(e)}'}]


def get_show_stories(limit: int = 10) -> List[Dict]:
    """
    Get Show HN stories from Hacker News
    """
    try:
        # Get Show HN story IDs
        show_stories_url = "https://hacker-news.firebaseio.com/v0/showstories.json"
        response = requests.get(show_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=10)
            story_data = story_response.json()
            
            if story_data:
                story = {
                    'id': story_data.get('id'),
                    'title': story_data.get('title', 'No title'),
                    'url': story_data.get('url', ''),
                    'score': story_data.get('score', 0),
                    'by': story_data.get('by', 'Unknown'),
                    'time': datetime.fromtimestamp(story_data.get('time', 0)).isoformat() if story_data.get('time') else '',
                    'descendants': story_data.get('descendants', 0),
                    'type': story_data.get('type', 'story'),
                    'text': story_data.get('text', '')
                }
                stories.append(story)
        
        return stories
    except Exception as e:
        return [{'error': f'Error fetching Show HN stories: {str(e)}'}]


def get_job_stories(limit: int = 10) -> List[Dict]:
    """
    Get Job stories from Hacker News
    """
    try:
        # Get Job story IDs
        job_stories_url = "https://hacker-news.firebaseio.com/v0/jobstories.json"
        response = requests.get(job_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=10)
            story_data = story_response.json()
            
            if story_data:
                story = {
                    'id': story_data.get('id'),
                    'title': story_data.get('title', 'No title'),
                    'url': story_data.get('url', ''),
                    'score': story_data.get('score', 0),
                    'by': story_data.get('by', 'Unknown'),
                    'time': datetime.fromtimestamp(story_data.get('time', 0)).isoformat() if story_data.get('time') else '',
                    'descendants': story_data.get('descendants', 0),
                    'type': story_data.get('type', 'job'),
                    'text': story_data.get('text', '')
                }
                stories.append(story)
        
        return stories
    except Exception as e:
        return [{'error': f'Error fetching Job stories: {str(e)}'}]


def get_story_by_id(story_id: int) -> Dict:
    """
    Get a specific story by its ID
    """
    try:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        response = requests.get(story_url, timeout=10)
        response.raise_for_status()
        story_data = response.json()
        
        if story_data:
            return {
                'id': story_data.get('id'),
                'title': story_data.get('title', 'No title'),
                'url': story_data.get('url', ''),
                'score': story_data.get('score', 0),
                'by': story_data.get('by', 'Unknown'),
                'time': datetime.fromtimestamp(story_data.get('time', 0)).isoformat() if story_data.get('time') else '',
                'descendants': story_data.get('descendants', 0),
                'type': story_data.get('type', 'story'),
                'text': story_data.get('text', ''),
                'kids': story_data.get('kids', [])  # Comment IDs
            }
        else:
            return {'error': f'Story with ID {story_id} not found'}
    except Exception as e:
        return {'error': f'Error fetching story {story_id}: {str(e)}'}


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python hacker_news.py top [limit] - Get top stories")
        print("  python hacker_news.py new [limit] - Get newest stories")
        print("  python hacker_news.py ask [limit] - Get Ask HN stories")
        print("  python hacker_news.py show [limit] - Get Show HN stories")
        print("  python hacker_news.py jobs [limit] - Get job listings")
        print("  python hacker_news.py get <id> - Get specific story by ID")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'top':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        stories = get_top_stories(limit)
        print(json.dumps(stories, indent=2))
    
    elif command == 'new':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        stories = get_new_stories(limit)
        print(json.dumps(stories, indent=2))
    
    elif command == 'ask':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        stories = get_ask_stories(limit)
        print(json.dumps(stories, indent=2))
    
    elif command == 'show':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        stories = get_show_stories(limit)
        print(json.dumps(stories, indent=2))
    
    elif command == 'jobs':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        stories = get_job_stories(limit)
        print(json.dumps(stories, indent=2))
    
    elif command == 'get':
        if len(sys.argv) < 3:
            print("Missing story ID for 'get' command")
            sys.exit(1)
        story_id = int(sys.argv[2])
        story = get_story_by_id(story_id)
        print(json.dumps(story, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: top, new, ask, show, jobs, get")
        sys.exit(1)


if __name__ == "__main__":
    main()