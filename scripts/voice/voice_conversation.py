#!/usr/bin/env python3
"""
Voice Conversation Manager for OpenClaw
Manages voice input/output for conversations with the AI assistant
"""

import threading
import time
import queue
from typing import Optional, Callable, Dict, Any
from .audio_utils import AudioUtils
from .stt_engine import STTEngine
from .tts_engine import TTSEngine
import openai  # For integration with OpenAI if needed


class VoiceConversationManager:
    """Manages voice conversations with the AI assistant"""
    
    def __init__(self, 
                 stt_engine_type: str = "whisper",
                 tts_engine_type: str = "pyttsx3",
                 language: str = "en-US",
                 voice_id: Optional[str] = None):
        """
        Initialize voice conversation manager
        """
        self.stt_engine = STTEngine(engine_type=stt_engine_type)
        self.tts_engine = TTSEngine(engine_type=tts_engine_type, voice_id=voice_id)
        self.language = language
        self.is_active = False
        self.conversation_history = []
        
        # Threading and queuing for real-time processing
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        
        # Event to control conversation flow
        self.conversation_event = threading.Event()
    
    def start_conversation(self, 
                          ai_response_callback: Callable[[str], str],
                          greeting: str = "Hello! I'm ready for our voice conversation. Please speak now."):
        """
        Start a voice conversation
        """
        self.is_active = True
        self.conversation_event.clear()
        
        # Greet the user
        print("Voice conversation started")
        self.tts_engine.speak(greeting)
        
        # Start threads for different aspects of conversation
        input_thread = threading.Thread(target=self._listen_loop)
        input_thread.daemon = True
        input_thread.start()
        
        processing_thread = threading.Thread(
            target=self._process_conversation, 
            args=(ai_response_callback,)
        )
        processing_thread.daemon = True
        processing_thread.start()
        
        # Wait for conversation to end
        try:
            while self.is_active:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nConversation interrupted by user")
            self.end_conversation()
    
    def _listen_loop(self):
        """
        Continuously listen for voice input
        """
        while self.is_active:
            try:
                # Record audio until silence is detected
                print("Listening...")
                audio = AudioUtils.record_until_silence(
                    max_duration=10,
                    silence_duration=1.5
                )
                
                if len(audio) > 0 and AudioUtils.detect_voice_activity(audio):
                    print("Audio detected, processing...")
                    
                    # Add to processing queue
                    self.input_queue.put(audio)
                    
                    # Brief pause to avoid overlapping recordings
                    time.sleep(0.5)
                else:
                    # Brief pause to reduce CPU usage
                    time.sleep(0.2)
            
            except Exception as e:
                print(f"Listening error: {str(e)}")
                time.sleep(0.5)
    
    def _process_conversation(self, ai_response_callback: Callable[[str], str]):
        """
        Process incoming audio and generate responses
        """
        while self.is_active:
            try:
                # Wait for audio input
                if not self.input_queue.empty():
                    audio_data = self.input_queue.get(timeout=1)
                    
                    # Transcribe audio to text
                    transcribed_text = self.stt_engine.transcribe_audio(
                        audio_data, 
                        language=self.language
                    )
                    
                    if transcribed_text and transcribed_text.strip():
                        print(f"You said: {transcribed_text}")
                        
                        # Add to conversation history
                        self.conversation_history.append({
                            'speaker': 'user',
                            'text': transcribed_text,
                            'timestamp': time.time()
                        })
                        
                        # Get AI response
                        ai_response = ai_response_callback(transcribed_text)
                        
                        if ai_response:
                            print(f"AI response: {ai_response}")
                            
                            # Add to conversation history
                            self.conversation_history.append({
                                'speaker': 'ai',
                                'text': ai_response,
                                'timestamp': time.time()
                            })
                            
                            # Speak the response
                            self.tts_engine.speak(ai_response)
                    
                    # Small delay before next input
                    time.sleep(0.2)
                else:
                    time.sleep(0.1)
            
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Processing error: {str(e)}")
                time.sleep(0.1)
    
    def end_conversation(self):
        """
        End the current conversation
        """
        print("Ending voice conversation...")
        self.is_active = False
        self.conversation_event.set()
        
        # Stop any ongoing speech
        self.tts_engine.stop_speaking()
    
    def toggle_mute(self):
        """
        Mute/unmute the conversation
        """
        # This would implement mute functionality
        pass
    
    def adjust_volume(self, level: float):
        """
        Adjust speech volume (0.0 to 1.0)
        """
        self.tts_engine.set_volume(level)
    
    def get_conversation_history(self) -> list:
        """
        Get the conversation history
        """
        return self.conversation_history.copy()
    
    def clear_conversation_history(self):
        """
        Clear the conversation history
        """
        self.conversation_history.clear()


def simple_ai_responder(user_input: str) -> str:
    """
    Simple AI responder for testing - replace with actual OpenClaw integration
    """
    # This is a placeholder - in reality, this would connect to OpenClaw
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
        return "Hello there! How can I help you today?"
    elif any(word in user_input_lower for word in ['how are you', 'how do you do']):
        return "I'm doing well, thank you for asking! How can I assist you?"
    elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you']):
        return "Goodbye! Feel free to start another conversation anytime."
    elif any(word in user_input_lower for word in ['thank', 'thanks']):
        return "You're welcome! Is there anything else I can help with?"
    else:
        # Simple echo response (would be replaced with actual AI logic)
        return f"I heard you say: '{user_input}'. How else can I assist you?"


def main():
    """
    Main function to run voice conversation demo
    """
    print("Starting voice conversation demo...")
    
    # Create voice conversation manager
    voice_manager = VoiceConversationManager(
        stt_engine_type="whisper",  # Use whisper for offline STT
        tts_engine_type="pyttsx3",  # Use pyttsx3 for offline TTS
        language="en-US"
    )
    
    try:
        # Start conversation with simple responder
        voice_manager.start_conversation(
            ai_response_callback=simple_ai_responder,
            greeting="Voice conversation demo started. Please speak now."
        )
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    finally:
        voice_manager.end_conversation()
        print("Voice conversation demo ended")


if __name__ == "__main__":
    main()