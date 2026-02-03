#!/usr/bin/env python3
"""
Comprehensive Free APIs Enhancement for OpenClaw
Integrates DuckDuckGo search, YouTube transcripts, local Whisper, and more
"""

import sys
import json
import os
import subprocess
from typing import Dict, List, Optional, Union
import requests
import urllib.parse


def search_brave(query: str, count: int = 5) -> List[Dict[str, str]]:
    """
    Use OpenClaw's built-in web_search capability (which may use Brave under the hood)
    """
    # This function would interface with OpenClaw's web_search tool
    # For now, we'll simulate the interface
    try:
        # This would normally call the web_search tool
        # For simulation purposes:
        result = {
            'query': query,
            'results_count': count,
            'source': 'brave_search_via_openclaw_tool',
            'note': 'This uses OpenClaw\'s built-in web_search tool which may utilize Brave Search'
        }
        return [result]
    except Exception as e:
        return [{'error': str(e)}]


def search_ddg(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search DuckDuckGo using the Instant Answer API
    """
    try:
        # DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        # Add the main answer if available
        if data.get('AbstractText'):
            results.append({
                'title': data.get('Heading', 'DuckDuckGo Result'),
                'body': data['AbstractText'],
                'url': data.get('AbstractURL', ''),
                'source': 'DuckDuckGo'
            })
        
        # Add related topics
        for topic in data.get('RelatedTopics', [])[:max_results-1]:
            if 'FirstURL' in topic and 'Text' in topic:
                results.append({
                    'title': topic.get('Name', 'Related Topic'),
                    'body': topic['Text'],
                    'url': topic['FirstURL'],
                    'source': 'DuckDuckGo'
                })
        
        return results[:max_results]
    
    except Exception as e:
        return [{'error': f"DuckDuckGo search error: {str(e)}"}]


def get_weather(location: str) -> Dict:
    """
    Get weather information using wttr.in (no API key required)
    """
    try:
        import urllib.parse
        encoded_location = urllib.parse.quote(location)
        url = f"http://wttr.in/{encoded_location}?format=j1"
        
        headers = {'User-Agent': 'curl/7.64.1'}  # wttr.in sometimes requires this
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data['current_condition'][0]
        
        weather_info = {
            'location': location,
            'temperature': current['temp_C'] + "°C (" + current['temp_F'] + "°F)",
            'description': current['weatherDesc'][0]['value'],
            'humidity': current['humidity'] + "%",
            'wind_speed': current['windspeedKmph'] + " km/h",
            'feels_like': current['FeelsLikeC'] + "°C (" + current['FeelsLikeF'] + "°F)"
        }
        
        return weather_info
    
    except Exception as e:
        return {'error': f"Weather lookup error: {str(e)}"}


def get_youtube_transcript(video_url_or_id: str, language: str = 'en') -> Dict:
    """
    Get transcript from YouTube video using youtube-transcript-api
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.formatters import TextFormatter
        import re
        
        # Extract video ID from URL
        if '://' in video_url_or_id:
            # Extract video ID from various YouTube URL formats
            patterns = [
                r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)',
                r'(?:youtube\.com/embed/|youtube\.com/v/)([^&\n?#]+)',
            ]
            
            video_id = None
            for pattern in patterns:
                match = re.search(pattern, video_url_or_id)
                if match:
                    video_id = match.group(1)
                    break
        else:
            video_id = video_url_or_id  # Assume it's already a video ID
        
        if not video_id:
            return {'error': 'Invalid YouTube URL or video ID'}
        
        # Fetch transcript
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Find transcript in requested language
        try:
            transcript = transcript_list.find_transcript([language])
        except:
            # Try to get any available transcript
            transcript = list(transcript_list)[0]
        
        transcript_data = transcript.fetch()
        
        # Format as text
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript_data)
        
        return {
            'video_id': video_id,
            'language': transcript.language_code,
            'transcript': formatted_transcript,
            'segment_count': len(transcript_data)
        }
    
    except ImportError:
        return {'error': 'youtube-transcript-api library not installed. Install with: pip install youtube-transcript-api'}
    except Exception as e:
        return {'error': f"YouTube transcript error: {str(e)}"}


def transcribe_audio_local(audio_file_path: str, model: str = "base") -> Dict:
    """
    Transcribe audio using local Whisper installation
    """
    try:
        # Verify the audio file exists
        if not os.path.exists(audio_file_path):
            return {'error': f'Audio file does not exist: {audio_file_path}'}
        
        # Verify Whisper CLI is available
        result = subprocess.run(['whisper', '--help'], capture_output=True, text=True)
        if result.returncode != 0:
            return {'error': 'Whisper CLI is not installed or not in PATH. Install with: pip install openai-whisper'}
        
        # Run Whisper transcription
        output_file = f"{audio_file_path.rsplit('.', 1)[0]}.txt"
        cmd = [
            'whisper',
            audio_file_path,
            '--model', model,
            '--output_format', 'txt',
            '--output_dir', os.path.dirname(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Read the transcribed text
            with open(output_file, 'r', encoding='utf-8') as f:
                transcription = f.read()
            
            return {
                'success': True,
                'transcription': transcription.strip(),
                'output_file': output_file,
                'model_used': model,
                'audio_file': audio_file_path
            }
        else:
            return {'error': f'Whisper transcription failed: {result.stderr}'}
    
    except FileNotFoundError:
        return {'error': 'Whisper CLI command not found. Please install: pip install openai-whisper'}
    except Exception as e:
        return {'error': f'Error during transcription: {str(e)}'}


def main():
    """
    Main function to demonstrate all capabilities
    Usage: python free_apis_enhancement.py <command> <args>
    Commands: search_ddg, weather, youtube_transcript, whisper
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python free_apis_enhancement.py search_ddg <query>")
        print("  python free_apis_enhancement.py weather <location>")
        print("  python free_apis_enhancement.py youtube_transcript <video_url_or_id> [language]")
        print("  python free_apis_enhancement.py whisper <audio_file> [model]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'search_ddg':
        if len(sys.argv) < 3:
            print("Missing query for search_ddg")
            sys.exit(1)
        query = ' '.join(sys.argv[2:])
        results = search_ddg(query)
        print(json.dumps(results, indent=2))
    
    elif command == 'weather':
        if len(sys.argv) < 3:
            print("Missing location for weather")
            sys.exit(1)
        location = ' '.join(sys.argv[2:])
        result = get_weather(location)
        print(json.dumps(result, indent=2))
    
    elif command == 'youtube_transcript':
        if len(sys.argv) < 3:
            print("Missing video URL or ID for youtube_transcript")
            sys.exit(1)
        video_id = sys.argv[2]
        language = sys.argv[3] if len(sys.argv) > 3 else 'en'
        result = get_youtube_transcript(video_id, language)
        print(json.dumps(result, indent=2))
    
    elif command == 'whisper':
        if len(sys.argv) < 3:
            print("Missing audio file path for whisper")
            sys.exit(1)
        audio_file = sys.argv[2]
        model = sys.argv[3] if len(sys.argv) > 3 else 'base'
        result = transcribe_audio_local(audio_file, model)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: search_ddg, weather, youtube_transcript, whisper")
        sys.exit(1)


if __name__ == "__main__":
    main()