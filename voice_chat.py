#!/usr/bin/env python3
"""
Simple Voice Chat for OpenClaw
A direct integration for voice communication
"""

import pyttsx3
import speech_recognition as sr
import threading
import time
import queue
from typing import Callable, Optional


class SimpleVoiceChat:
    """
    Simple voice chat system that integrates with OpenClaw
    Uses the available components without complex setup
    """
    
    def __init__(self, ai_responder: Callable[[str], str]):
        self.ai_responder = ai_responder
        self.listening = False
        self.should_stop = False
        
        # Initialize TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Initialize STT recognizer
        self.stt_recognizer = sr.Recognizer()
        self.stt_recognizer.energy_threshold = 400
        self.stt_recognizer.dynamic_energy_threshold = True
        
        # Microphone
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise, please wait...")
        with self.microphone:
            self.stt_recognizer.adjust_for_ambient_noise(self.microphone, duration=1)
        print("Ready for voice communication!")
    
    def speak(self, text: str):
        """Speak text using TTS"""
        print(f"AI: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen_once(self) -> Optional[str]:
        """Listen for a single voice input"""
        try:
            print("Listening... (speak now)")
            with self.microphone as source:
                audio = self.stt_recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Processing speech...")
            # Try to recognize speech
            text = self.stt_recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
    
    def start_conversation(self, greeting: str = "Hello! Voice chat is now active. How can I help you?"):
        """Start continuous conversation"""
        self.speak(greeting)
        
        while not self.should_stop:
            try:
                # Listen for user input
                user_input = self.listen_once()
                
                if user_input:
                    # Get AI response
                    response = self.ai_responder(user_input)
                    
                    # Speak the response
                    if response:
                        self.speak(response)
                    else:
                        self.speak("I'm not sure how to respond to that.")
                
                # Brief pause before next iteration
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\nConversation ended by user")
                break
        
        print("Voice chat ended")
    
    def stop(self):
        """Stop the conversation"""
        self.should_stop = True


def simple_responder(user_input: str) -> str:
    """
    Simple AI responder for testing
    """
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello there! I'm your AI assistant. How can I help you today?"
    elif any(word in user_input_lower for word in ['how are you', 'how do you do', 'how are things']):
        return "I'm doing well, thank you for asking! How can I assist you?"
    elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Goodbye! Feel free to start another conversation anytime."
    elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
        return "You're welcome! Is there anything else I can help with?"
    elif any(word in user_input_lower for word in ['help', 'assist', 'what can you do']):
        return "I can chat with you, answer questions, help with tasks, and more! What would you like to talk about?"
    else:
        return f"I heard you say: '{user_input}'. How can I help you further?"


def main():
    """Main function to run the voice chat"""
    print("Starting Simple Voice Chat for OpenClaw...")
    print("Make sure your microphone and speakers are working properly.")
    
    try:
        # Create voice chat instance
        voice_chat = SimpleVoiceChat(simple_responder)
        
        # Start conversation
        voice_chat.start_conversation("Hello! I'm ready for voice conversation. Please speak now.")
        
    except Exception as e:
        print(f"Error starting voice chat: {e}")
        print("Make sure you have a working microphone and audio system.")


if __name__ == "__main__":
    main()