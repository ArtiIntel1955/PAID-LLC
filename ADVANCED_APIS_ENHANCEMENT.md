# Advanced APIs Enhancement for OpenClaw

This document outlines the comprehensive capabilities added to OpenClaw for free API usage, including Hacker News, IP geolocation, DuckDuckGo search, YouTube transcripts, local Whisper, weather data, and Brave search.

## New Capabilities Added

### 1. Hacker News (HN) Skill
- **Function**: Access Hacker News top stories, newest stories, Ask HN, Show HN, and job listings
- **Usage**: `python scripts/hacker_news.py <command> [limit|id]`
- **Commands**:
  - `top [limit]` - Get top stories (default: 10)
  - `new [limit]` - Get newest stories (default: 10)
  - `ask [limit]` - Get Ask HN stories (default: 10)
  - `show [limit]` - Get Show HN stories (default: 10)
  - `jobs [limit]` - Get job listings (default: 10)
  - `get <id>` - Get specific story by ID
- **Features**: No API key required, rich story metadata

### 2. IP Geolocation
- **Function**: Get location information for IP addresses
- **Usage**: `python scripts/ip_geolocation.py [ip_address]`
- **Features**:
  - If no IP provided, returns current IP info
  - Uses multiple services for reliability (ip-api.com, ipapi.co, ipinfo.io)
  - Provides comprehensive location data including country, region, city, coordinates, ISP, etc.
  - Handles proxy and hosting detection

### 3. DuckDuckGo Search
- **Function**: Free web search using DuckDuckGo's Instant Answer API
- **Usage**: `python scripts/ddg_search.py "search query" [max_results]`
- **Features**: No API key required, instant answers, related topics

### 4. YouTube Transcripts
- **Function**: Extract transcripts from YouTube videos
- **Usage**: `python scripts/youtube_transcript.py <video_url_or_id> [language]`
- **Features**: Works with any YouTube video, supports multiple languages

### 5. Local Whisper Speech-to-Text
- **Function**: Transcribe audio files using local Whisper model
- **Usage**: `python scripts/local_whisper.py <audio_file_path> [model]`
- **Features**: No API costs, works offline, multiple model sizes available

### 6. Weather Data
- **Function**: Get current weather using wttr.in (no API key required)
- **Already integrated**: Uses OpenClaw's built-in weather skill
- **Features**: Global weather data, detailed conditions

### 7. Brave Search
- **Function**: Web search using Brave Search
- **Already integrated**: Uses OpenClaw's built-in web_search tool
- **Features**: Privacy-focused search, no tracking

## Unified Interface

### Advanced API Enhancement Script
- **Function**: Unified interface for all capabilities
- **Usage**: `python scripts/advanced_apis_enhancement.py <category> <command> [args]`
- **Categories**:
  - `hn` - Hacker News commands
  - `ip` - IP geolocation
  - `ddg` - DuckDuckGo search
  - `yt` - YouTube transcripts
  - `whisper` - Local audio transcription
  - `weather` - Weather information

## Scripts Location

- `scripts/hacker_news.py` - Hacker News functionality
- `scripts/ip_geolocation.py` - IP address geolocation
- `scripts/ddg_search.py` - DuckDuckGo search functionality
- `scripts/youtube_transcript.py` - YouTube transcript extraction
- `scripts/local_whisper.py` - Local audio transcription
- `scripts/advanced_apis_enhancement.py` - Unified interface for all capabilities
- `scripts/free_apis_enhancement.py` - Original unified interface
- `scripts/setup_free_apis.py` - Setup script for dependencies
- `FREE_APIS_ENHANCEMENT.md` - Original documentation
- `ADVANCED_APIS_ENHANCEMENT.md` - This documentation

## Installation Requirements

All required packages were already installed in the previous enhancement:
- `requests` (for HTTP requests)
- `youtube-transcript-api` (for YouTube transcripts)
- `openai-whisper` (for local Whisper)

## Usage Examples

### Hacker News
```bash
# Get top 5 stories
python scripts/hacker_news.py top 5

# Get newest 10 stories
python scripts/hacker_news.py new 10

# Get specific story by ID
python scripts/hacker_news.py get 123456789

# Get Ask HN stories
python scripts/hacker_news.py ask 5
```

### IP Geolocation
```bash
# Get info for current IP
python scripts/ip_geolocation.py

# Get info for specific IP
python scripts/ip_geolocation.py 8.8.8.8

# Get info for your public IP
python scripts/ip_geolocation.py myip
```

### Unified Interface
```bash
# Hacker News top stories
python scripts/advanced_apis_enhancement.py hn top 5

# IP geolocation
python scripts/advanced_apis_enhancement.py ip 8.8.8.8

# DuckDuckGo search
python scripts/advanced_apis_enhancement.py ddg "AI developments" 5

# YouTube transcript
python scripts/advanced_apis_enhancement.py yt "https://www.youtube.com/watch?v=example" en

# Local Whisper transcription
python scripts/advanced_apis_enhancement.py whisper "audio.mp3" base

# Weather lookup
python scripts/advanced_apis_enhancement.py weather "New York"
```

## Integration with OpenClaw

These capabilities can be integrated into OpenClaw workflows as follows:

1. **News Monitoring**: Use Hacker News to track trending technology discussions
2. **Security**: Use IP geolocation to analyze traffic sources and detect suspicious activity
3. **Research**: Combine DuckDuckGo and Brave search for comprehensive results
4. **Content Analysis**: Extract transcripts from educational YouTube videos
5. **Audio Processing**: Transcribe meetings, interviews, or podcasts locally
6. **Environmental Context**: Provide location-based weather data

## Benefits

- **Cost-effective**: All capabilities use free APIs or local processing
- **Privacy-focused**: No data sent to third-party services unnecessarily
- **Reliable**: Multiple fallback options for each capability
- **Scalable**: Can handle various input types and volumes
- **Offline-ready**: Whisper works without internet connection once installed
- **Comprehensive**: Wide range of data sources and information types

## Troubleshooting

### Common Issues:

1. **API timeouts**: Some services may occasionally be slow or unavailable; the system has fallbacks
2. **IP geolocation fails**: Different services may have different success rates
3. **Hacker News API limits**: The official API has rate limits; results may be delayed
4. **YouTube transcript unavailable**: Not all videos have captions available

### Performance Tips:

1. Use appropriate limits for Hacker News queries to avoid unnecessary data transfer
2. Cache IP geolocation results to reduce API calls for the same IPs
3. Use smaller Whisper models (tiny, base) for faster processing
4. Combine multiple data sources for comprehensive information gathering