# Free APIs Enhancement for OpenClaw

This document outlines the expanded capabilities added to OpenClaw for free API usage, including DuckDuckGo search, YouTube transcripts, local Whisper, weather data, and Brave search.

## Enhanced Capabilities

### 1. DuckDuckGo Search
- **Function**: Free web search using DuckDuckGo's Instant Answer API
- **Usage**: `python scripts/ddg_search.py "search query" [max_results]`
- **Example**: `python scripts/ddg_search.py "latest AI developments" 5`
- **Features**: No API key required, instant answers, related topics

### 2. YouTube Transcripts
- **Function**: Extract transcripts from YouTube videos
- **Usage**: `python scripts/youtube_transcript.py <video_url_or_id> [language]`
- **Example**: `python scripts/youtube_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" en`
- **Features**: Works with any YouTube video, supports multiple languages

### 3. Local Whisper Speech-to-Text
- **Function**: Transcribe audio files using local Whisper model
- **Usage**: `python scripts/local_whisper.py <audio_file_path> [model]`
- **Example**: `python scripts/local_whisper.py "recording.mp3" base`
- **Features**: No API costs, works offline, multiple model sizes available

### 4. Weather Data
- **Function**: Get current weather using wttr.in (no API key required)
- **Already integrated**: Uses OpenClaw's built-in weather skill
- **Usage**: Built into OpenClaw's weather tool
- **Features**: Global weather data, detailed conditions

### 5. Brave Search
- **Function**: Web search using Brave Search
- **Already integrated**: Uses OpenClaw's built-in web_search tool
- **Usage**: `web_search("query")` in OpenClaw
- **Features**: Privacy-focused search, no tracking

## Installation Requirements

The following packages are required for the new capabilities:

```bash
pip install youtube-transcript-api
pip install openai-whisper
```

Note: Whisper installation may take some time as it downloads model files on first use.

## Scripts Location

- `scripts/ddg_search.py` - DuckDuckGo search functionality
- `scripts/youtube_transcript.py` - YouTube transcript extraction
- `scripts/local_whisper.py` - Local audio transcription
- `scripts/free_apis_enhancement.py` - Unified interface for all capabilities
- `scripts/setup_free_apis.py` - Setup script for dependencies

## Usage Examples

### DuckDuckGo Search
```python
import json
from scripts.ddg_search import search_ddg

results = search_ddg("latest AI news", 5)
print(json.dumps(results, indent=2))
```

### YouTube Transcript
```python
import json
from scripts.youtube_transcript import get_youtube_transcript

transcript = get_youtube_transcript("https://www.youtube.com/watch?v=example", "en")
print(json.dumps(transcript, indent=2))
```

### Local Whisper
```python
import json
from scripts.local_whisper import transcribe_audio_local

result = transcribe_audio_local("audio_file.mp3", "base")
print(json.dumps(result, indent=2))
```

## Integration with OpenClaw

These capabilities can be integrated into OpenClaw workflows as follows:

1. **Web Research**: Combine DuckDuckGo and Brave search for comprehensive results
2. **Content Analysis**: Extract transcripts from educational YouTube videos
3. **Audio Processing**: Transcribe meetings, interviews, or podcasts locally
4. **Weather Information**: Provide location-based weather data
5. **Multimodal Input**: Process both text and audio inputs seamlessly

## Benefits

- **Cost-effective**: All capabilities use free APIs or local processing
- **Privacy-focused**: No data sent to third-party services unnecessarily
- **Reliable**: Multiple fallback options for each capability
- **Scalable**: Can handle various input types and volumes
- **Offline-ready**: Whisper works without internet connection once installed

## Troubleshooting

### Common Issues:

1. **Whisper not found**: Ensure Whisper is installed with `pip install openai-whisper`
2. **DDG search fails**: Check internet connection and query formatting
3. **YouTube transcript error**: Video might not have captions or be region-locked
4. **Weather lookup fails**: Check location spelling and formatting

### Performance Tips:

1. Use smaller Whisper models (tiny, base) for faster processing
2. Limit search results to reduce processing time
3. Cache frequently accessed data to reduce API calls
4. Use appropriate tools based on specific needs and constraints