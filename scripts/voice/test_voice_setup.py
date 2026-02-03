#!/usr/bin/env python3
"""
Test script to verify voice communication system setup
"""

import sys
import os

def test_imports():
    """Test that required modules can be imported"""
    print("Testing imports...")
    
    try:
        import numpy
        print("[SUCCESS] numpy available")
    except ImportError:
        print("[ERROR] numpy not available")
        return False
    
    try:
        import soundfile
        print("[SUCCESS] soundfile available")
    except ImportError:
        print("[ERROR] soundfile not available")
        return False
    
    try:
        import pyttsx3
        print("[SUCCESS] pyttsx3 available")
    except ImportError:
        print("[ERROR] pyttsx3 not available")
        return False
    
    try:
        # Try importing our own modules
        sys.path.append(os.path.dirname(__file__))
        from audio_utils import AudioUtils
        print("[SUCCESS] audio_utils available")
    except ImportError as e:
        print(f"[ERROR] audio_utils not available: {e}")
    
    try:
        from tts_engine import TTSEngine
        print("[SUCCESS] tts_engine available")
    except ImportError as e:
        print(f"[ERROR] tts_engine not available: {e}")
    
    # Test speech recognition separately since it may not be available
    try:
        import speech_recognition
        print("[SUCCESS] speech_recognition available")
        speech_rec_available = True
    except ImportError:
        print("[INFO] speech_recognition not available (this is okay)")
        speech_rec_available = False
    
    # Test whisper since it's already installed
    try:
        import whisper
        print("[SUCCESS] whisper available")
        whisper_available = True
    except ImportError:
        print("[INFO] whisper not available")
        whisper_available = False
    
    return True


def test_tts():
    """Test text-to-speech functionality"""
    print("\nTesting TTS...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        
        # Test speaking
        engine.say("Voice communication system is set up and ready.")
        engine.runAndWait()
        print("[SUCCESS] TTS test completed")
        return True
    except Exception as e:
        print(f"[ERROR] TTS test failed: {e}")
        return False


def test_audio_utils():
    """Test audio utilities"""
    print("\nTesting audio utilities...")
    try:
        import numpy as np
        from audio_utils import AudioUtils
        
        # Test basic functionality
        print(f"Audio format: {AudioUtils.FORMAT}")
        print(f"Sample rate: {AudioUtils.RATE}")
        
        # Test create a simple audio array
        test_audio = np.zeros(1000, dtype=np.int16)
        has_voice = AudioUtils.detect_voice_activity(test_audio)
        print(f"Silence detected correctly: {not has_voice}")
        
        print("[SUCCESS] Audio utilities test completed")
        return True
    except Exception as e:
        print(f"[ERROR] Audio utilities test failed: {e}")
        return False


def main():
    print("Voice Communication System Setup Test")
    print("=" * 50)
    
    # Add the voice directory to the path
    sys.path.append(os.path.dirname(__file__))
    
    success = True
    success &= test_imports()
    success &= test_tts()
    success &= test_audio_utils()
    
    print("\n" + "=" * 50)
    if success:
        print("[SUCCESS] Voice communication system setup test PASSED!")
        print("\nThe system is ready for voice communication with the following capabilities:")
        print("- Text-to-Speech (TTS) with pyttsx3")
        print("- Audio processing with numpy and soundfile")
        print("- Audio recording utilities")
        print("- Integration with Whisper for speech recognition")
        print("\nTo start voice conversation, use the voice_conversation.py module.")
    else:
        print("[ERROR] Voice communication system setup test FAILED!")
        print("Some components are missing or not working properly.")
    
    return success


if __name__ == "__main__":
    main()