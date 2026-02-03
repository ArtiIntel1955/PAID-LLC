#!/usr/bin/env python3
"""
Audio Utilities for Voice Communication System
Provides common audio processing functions
"""

import wave
import pyaudio
import numpy as np
import soundfile as sf
from typing import Tuple, Optional
import io


class AudioUtils:
    """Utility class for common audio operations"""
    
    # Audio configuration constants
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # Standard rate for speech recognition
    CHUNK = 1024
    THRESHOLD = 500  # Minimum amplitude to consider as voice
    
    @staticmethod
    def record_audio(seconds: int = 5, device_index: Optional[int] = None) -> np.ndarray:
        """
        Record audio for specified duration
        Returns numpy array of audio samples
        """
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=AudioUtils.FORMAT,
            channels=AudioUtils.CHANNELS,
            rate=AudioUtils.RATE,
            input=True,
            frames_per_buffer=AudioUtils.CHUNK,
            input_device_index=device_index
        )
        
        frames = []
        
        for _ in range(0, int(AudioUtils.RATE / AudioUtils.CHUNK * seconds)):
            data = stream.read(AudioUtils.CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Convert byte frames to numpy array
        audio_data = b''.join(frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        return audio_array
    
    @staticmethod
    def record_until_silence(max_duration: int = 10, silence_threshold: int = 300, 
                           silence_duration: float = 1.0) -> np.ndarray:
        """
        Record audio until a period of silence is detected
        """
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=AudioUtils.FORMAT,
            channels=AudioUtils.CHANNELS,
            rate=AudioUtils.RATE,
            input=True,
            frames_per_buffer=AudioUtils.CHUNK
        )
        
        frames = []
        silent_chunks = 0
        max_silent_chunks = int(silence_duration * AudioUtils.RATE / AudioUtils.CHUNK)
        total_chunks = 0
        max_chunks = int(max_duration * AudioUtils.RATE / AudioUtils.CHUNK)
        
        while total_chunks < max_chunks:
            data = stream.read(AudioUtils.CHUNK)
            frames.append(data)
            
            # Convert to numpy to check amplitude
            audio_chunk = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_chunk).mean()
            
            if amplitude < silence_threshold:
                silent_chunks += 1
                if silent_chunks >= max_silent_chunks:
                    break  # Stop recording after period of silence
            else:
                silent_chunks = 0  # Reset counter when voice detected
            
            total_chunks += 1
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Convert byte frames to numpy array
        audio_data = b''.join(frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        return audio_array
    
    @staticmethod
    def save_wav(audio_array: np.ndarray, filename: str, rate: int = 16000):
        """Save numpy audio array to WAV file"""
        sf.write(filename, audio_array, rate)
    
    @staticmethod
    def normalize_audio(audio_array: np.ndarray, target_level: float = 0.8) -> np.ndarray:
        """Normalize audio to target level"""
        max_amplitude = np.max(np.abs(audio_array))
        if max_amplitude > 0:
            normalized = audio_array * (target_level * 32767 / max_amplitude)
            return normalized.astype(np.int16)
        return audio_array
    
    @staticmethod
    def detect_voice_activity(audio_array: np.ndarray, threshold: int = 300) -> bool:
        """Detect if voice is present in audio array"""
        avg_amplitude = np.abs(audio_array).mean()
        return avg_amplitude > threshold
    
    @staticmethod
    def audio_to_bytesio(audio_array: np.ndarray, rate: int = 16000) -> io.BytesIO:
        """Convert numpy audio array to BytesIO object in WAV format"""
        buffer = io.BytesIO()
        sf.write(buffer, audio_array, rate, format='WAV')
        buffer.seek(0)
        return buffer


if __name__ == "__main__":
    # Test audio utilities
    print("Testing audio utilities...")
    
    # Record a short sample
    print("Recording 3 seconds of audio...")
    audio_sample = AudioUtils.record_audio(3)
    print(f"Recorded {len(audio_sample)} samples")
    
    # Check if voice was detected
    has_voice = AudioUtils.detect_voice_activity(audio_sample)
    print(f"Voice detected: {has_voice}")
    
    # Normalize audio
    normalized_audio = AudioUtils.normalize_audio(audio_sample)
    print("Audio normalized")
    
    print("Audio utilities test completed successfully!")