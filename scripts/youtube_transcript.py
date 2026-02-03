#!/usr/bin/env python3
"""
YouTube Transcript Extractor for OpenClaw
Extracts transcripts from YouTube videos using youtube-transcript-api
"""

import sys
import json
import re
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs


def extract_video_id(youtube_url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats
    """
    # Pattern matching for different YouTube URL formats
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)',
        r'(?:youtube\.com/embed/|youtube\.com/v/)([^&\n?#]+)',
        r'(?:youtube\.com/shorts/)([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    # Handle the case where URL is already just the video ID
    if len(youtube_url) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', youtube_url):
        return youtube_url
    
    return None


def get_youtube_transcript(video_url_or_id: str, languages: List[str] = ['en']) -> Dict:
    """
    Get transcript from a YouTube video
    """
    try:
        # Import here to avoid dependency issues if not installed
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.formatters import TextFormatter
        
        # Extract video ID if a URL was provided
        video_id = extract_video_id(video_url_or_id) if '://' in video_url_or_id else video_url_or_id
        
        if not video_id:
            return {
                'error': 'Invalid YouTube URL or video ID',
                'video_id': video_url_or_id
            }
        
        # Fetch available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Find a transcript in one of the preferred languages
        transcript = None
        available_languages = []
        
        for lang in languages:
            try:
                transcript = transcript_list.find_transcript([lang])
                break
            except:
                available_languages.extend([t.language_code for t in transcript_list])
        
        # If we still don't have a transcript, try to get any available one
        if not transcript:
            try:
                transcript = transcript_list.find_transcript(available_languages)
            except:
                return {
                    'error': f'No transcript available in requested languages {languages}',
                    'available_languages': available_languages,
                    'video_id': video_id
                }
        
        # Fetch the actual transcript
        transcript_data = transcript.fetch()
        
        # Format as plain text
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript_data)
        
        # Return detailed information
        return {
            'video_id': video_id,
            'title': f"YouTube Video: {video_id}",
            'languages_available': available_languages,
            'requested_language': languages[0],
            'transcript': formatted_transcript,
            'segments': transcript_data,
            'success': True
        }
        
    except ImportError:
        return {
            'error': 'youtube-transcript-api library not installed. Install with: pip install youtube-transcript-api',
            'video_id': extract_video_id(video_url_or_id) if '://' in video_url_or_id else video_url_or_id
        }
    except Exception as e:
        return {
            'error': str(e),
            'video_id': extract_video_id(video_url_or_id) if '://' in video_url_or_id else video_url_or_id
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript.py <youtube_url_or_id> [language]")
        sys.exit(1)
    
    video_identifier = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'en'
    
    result = get_youtube_transcript(video_identifier, [language])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()