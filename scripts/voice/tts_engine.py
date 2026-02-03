#!/usr/bin/env python3
"""
Text-to-Speech Engine for Voice Communication System
Handles converting text responses to speech
"""

import pyttsx3
import pygame
import tempfile
import os
from typing import Optional
import threading
import queue


class TTSEngine:
    """Text-to-Speech engine with multiple backend support"""
    
    def __init__(self, engine_type: str = "pyttsx3", voice_id: Optional[str] = None):
        """
        Initialize TTS engine
        engine_type: "pyttsx3", "gtts" (Google TTS requires internet)
        """
        self.engine_type = engine_type
        self.voice_id = voice_id
        self.current_audio_queue = queue.Queue()
        
        if engine_type == "pyttsx3":
            self.engine = pyttsx3.init()
            
            # Configure properties
            self.engine.setProperty('rate', 180)  # Speed percent (default is 200)
            self.engine.setProperty('volume', 0.9)  # Volume 0-1 (default is 1)
            
            # Set voice if specified
            if voice_id:
                self.engine.setProperty('voice', voice_id)
            else:
                # Use default voice or select a good quality one
                voices = self.engine.getProperty('voices')
                if voices:
                    # Prefer female voice if available (often clearer)
                    female_voices = [v for v in voices if 'female' in v.name.lower() or 'zira' in v.name.lower().lower()]
                    if female_voices:
                        self.engine.setProperty('voice', female_voices[0].id)
                    else:
                        self.engine.setProperty('voice', voices[0].id)
        
        elif engine_type == "gtts":
            try:
                from gtts import gTTS
                self.gtts = gTTS
            except ImportError:
                raise ImportError("Please install gtts: pip install gtts")
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
    
    def speak(self, text: str, blocking: bool = True):
        """
        Speak the given text
        """
        if self.engine_type == "pyttsx3":
            if blocking:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Non-blocking: run in separate thread
                thread = threading.Thread(target=self._speak_non_blocking, args=(text,))
                thread.daemon = True
                thread.start()
        elif self.engine_type == "gtts":
            self._speak_with_gtts(text, blocking)
    
    def _speak_non_blocking(self, text: str):
        """
        Speak text in a non-blocking manner
        """
        self.engine.say(text)
        self.engine.runAndWait()
    
    def _speak_with_gtts(self, text: str, blocking: bool = True):
        """
        Speak using Google TTS
        """
        try:
            # Create gTTS object
            tts = self.gtts(text=text, lang='en', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                temp_filename = tmp_file.name
            
            try:
                # Load and play the audio
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                
                if blocking:
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
            finally:
                # Clean up temp file
                pygame.mixer.music.unload()
                os.unlink(temp_filename)
        
        except Exception as e:
            print(f"GTTS playback error: {str(e)}")
    
    def get_voices(self):
        """
        Get available voices (pyttsx3 only)
        """
        if self.engine_type == "pyttsx3":
            return self.engine.getProperty('voices')
        else:
            return []
    
    def set_voice(self, voice_id: str):
        """
        Set voice by ID (pyttsx3 only)
        """
        if self.engine_type == "pyttsx3":
            self.engine.setProperty('voice', voice_id)
    
    def set_rate(self, rate: int):
        """
        Set speech rate (pyttsx3 only)
        """
        if self.engine_type == "pyttsx3":
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """
        Set speech volume (pyttsx3 only)
        """
        if self.engine_type == "pyttsx3":
            self.engine.setProperty('volume', volume)
    
    def save_to_file(self, text: str, filename: str, language: str = 'en'):
        """
        Save speech to audio file
        """
        if self.engine_type == "gtts":
            try:
                tts = self.gtts(text=text, lang=language, slow=False)
                tts.save(filename)
                return True
            except Exception as e:
                print(f"Error saving to file: {str(e)}")
                return False
        else:
            # For pyttsx3, we'd need to route through SAPI or another mechanism
            print("File saving only supported with GTTS engine")
            return False
    
    def stop_speaking(self):
        """
        Stop current speech
        """
        if self.engine_type == "pyttsx3":
            self.engine.stop()


if __name__ == "__main__":
    # Test TTS engine
    print("Testing TTS engine...")
    
    try:
        tts = TTSEngine(engine_type="pyttsx3")
        print("TTS engine initialized")
        
        # Test speaking
        print("Speaking test message...")
        tts.speak("Hello, this is a test of the text to speech system. Voice communication is now available.")
        print("TTS test completed successfully!")
        
    except Exception as e:
        print(f"TTS engine test failed: {e}")
        
        # Try with GTTS if available
        try:
            tts = TTSEngine(engine_type="gtts")
            print("TTS engine initialized with GTTS")
            print("TTS GTTS test completed!")
        except ImportError:
            print("Neither pyttsx3 nor gtts is available")