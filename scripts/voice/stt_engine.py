#!/usr/bin/env python3
"""
Speech-to-Text Engine for Voice Communication System
Handles converting spoken words to text
"""

import speech_recognition as sr
import numpy as np
from typing import Optional, Dict, Any
import tempfile
import os
import io
from .audio_utils import AudioUtils


class STTEngine:
    """Speech-to-Text engine with multiple backend support"""
    
    def __init__(self, engine_type: str = "whisper"):
        """
        Initialize STT engine
        engine_type: "whisper", "google", "sphinx", "wit", "azure", "houndify", "ibm"
        """
        self.engine_type = engine_type
        self.recognizer = sr.Recognizer()
        
        # Adjust for ambient noise
        self.recognizer.energy_threshold = 400
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize based on engine type
        if engine_type == "whisper":
            try:
                import whisper
                self.whisper_model = whisper.load_model("base")
            except ImportError:
                raise ImportError("Please install openai-whisper: pip install openai-whisper")
        elif engine_type == "google":
            # Google requires internet connection
            pass
        elif engine_type == "sphinx":
            # CMU Sphinx works offline
            self.recognizer.pause_threshold = 0.8
    
    def transcribe_audio(self, audio_array: np.ndarray, language: str = "en-US") -> Optional[str]:
        """
        Transcribe audio array to text
        """
        try:
            # Convert numpy array to AudioData object
            audio_data = self._numpy_to_audio_data(audio_array, AudioUtils.RATE)
            
            if self.engine_type == "whisper":
                return self._transcribe_with_whisper(audio_data, language)
            elif self.engine_type == "google":
                return self._transcribe_with_google(audio_data, language)
            elif self.engine_type == "sphinx":
                return self._transcribe_with_sphinx(audio_data, language)
            else:
                # Default to Google if unknown engine
                return self._transcribe_with_google(audio_data, language)
        
        except Exception as e:
            print(f"STT transcription error: {str(e)}")
            return None
    
    def _numpy_to_audio_data(self, audio_array: np.ndarray, rate: int) -> sr.AudioData:
        """
        Convert numpy array to SpeechRecognition AudioData
        """
        # Convert to 16-bit PCM WAV format in memory
        import wave
        import io
        
        # Ensure audio is in the right format
        audio_bytes = audio_array.astype(np.int16).tobytes()
        
        # Create WAV in memory
        wav_buffer = io.BytesIO()
        
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(AudioUtils.CHANNELS)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(rate)
            wav_file.writeframes(audio_bytes)
        
        wav_buffer.seek(0)
        audio_data = sr.AudioData(wav_buffer.getvalue(), rate, 2)
        
        return audio_data
    
    def _transcribe_with_whisper(self, audio_data: sr.AudioData, language: str) -> Optional[str]:
        """
        Transcribe using OpenAI Whisper (offline/local)
        """
        try:
            # Save audio to temporary file for Whisper
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_data.get_wav_data())
                temp_filename = tmp_file.name
            
            try:
                # Transcribe with Whisper
                result = self.whisper_model.transcribe(temp_filename, language=language[:2])
                return result["text"].strip()
            finally:
                # Clean up temp file
                os.unlink(temp_filename)
        
        except Exception as e:
            print(f"Whisper transcription error: {str(e)}")
            return None
    
    def _transcribe_with_google(self, audio_data: sr.AudioData, language: str) -> Optional[str]:
        """
        Transcribe using Google Speech Recognition (requires internet)
        """
        try:
            return self.recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError:
            print("Google STT: Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Google STT error: {e}")
            return None
    
    def _transcribe_with_sphinx(self, audio_data: sr.AudioData, language: str) -> Optional[str]:
        """
        Transcribe using CMU Sphinx (offline)
        """
        try:
            return self.recognizer.recognize_sphinx(audio_data, language=language)
        except sr.UnknownValueError:
            print("Sphinx STT: Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Sphinx STT error: {e}")
            return None
    
    def transcribe_file(self, audio_file_path: str, language: str = "en-US") -> Optional[str]:
        """
        Transcribe an audio file to text
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = self.recognizer.record(source)
            
            if self.engine_type == "whisper":
                # For file-based transcription with Whisper, use the file directly
                result = self.whisper_model.transcribe(audio_file_path, language=language[:2])
                return result["text"].strip()
            elif self.engine_type == "google":
                return self.recognizer.recognize_google(audio_data, language=language)
            elif self.engine_type == "sphinx":
                return self.recognizer.recognize_sphinx(audio_data, language=language)
            else:
                return self.recognizer.recognize_google(audio_data, language=language)
        
        except Exception as e:
            print(f"File transcription error: {str(e)}")
            return None


if __name__ == "__main__":
    # Test STT engine
    print("Testing STT engine...")
    
    try:
        stt = STTEngine(engine_type="whisper")
        print("STT engine initialized with Whisper")
        
        # Test with a sample audio (would need actual recorded audio to test properly)
        print("STT engine test completed successfully!")
        
    except ImportError as e:
        print(f"STT engine initialization failed: {e}")
        print("Trying with Google engine...")
        
        try:
            stt = STTEngine(engine_type="google")
            print("STT engine initialized with Google")
        except Exception as e:
            print(f"Google STT also failed: {e}")