"""
Voice Communication System for OpenClaw
Main entry point for voice functionality
"""

from .audio_utils import AudioUtils
from .stt_engine import STTEngine
from .tts_engine import TTSEngine
from .voice_conversation import VoiceConversationManager

__version__ = "1.0.0"
__author__ = "OpenClaw Voice Team"
__all__ = [
    'AudioUtils',
    'STTEngine', 
    'TTSEngine',
    'VoiceConversationManager'
]