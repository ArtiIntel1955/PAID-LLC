#!/usr/bin/env python3
"""
Simple Voice Demo for OpenClaw
Demonstrates voice capabilities with available components
"""

import pyttsx3
from typing import Callable


class VoiceDemo:
    """
    Voice demo system using available components
    Since microphone support isn't available, this demonstrates the TTS portion
    and shows how it would integrate when full voice support is available
    """
    
    def __init__(self, ai_responder: Callable[[str], str]):
        self.ai_responder = ai_responder
        
        # Initialize TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Get and set a good voice
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Prefer a clear voice
            self.tts_engine.setProperty('voice', voices[0].id)
    
    def speak(self, text: str):
        """Speak text using TTS"""
        print(f"AI Voice: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def simulate_voice_input(self, text: str) -> str:
        """Simulate receiving voice input (in real implementation, this would be STT)"""
        print(f"(Simulated voice input recognized as): {text}")
        return text
    
    def chat(self, user_input: str):
        """Simulate a voice chat interaction"""
        # Simulate voice input recognition
        recognized_text = self.simulate_voice_input(user_input)
        
        # Get AI response
        response = self.ai_responder(recognized_text)
        
        # Speak the response
        self.speak(response)
        
        return response


def simple_responder(user_input: str) -> str:
    """
    Simple AI responder for demonstration
    """
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello there! I'm your AI assistant ready for voice conversation. How can I help you today?"
    elif any(word in user_input_lower for word in ['how are you', 'how do you do', 'how are things']):
        return "I'm doing well, thank you for asking! I'm ready for our voice conversation."
    elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Goodbye! I hope our voice communication system works well for you soon."
    elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
        return "You're very welcome! I'm here to help whenever you need."
    elif any(word in user_input_lower for word in ['voice', 'talk', 'speak', 'chat']):
        return "I'm ready to communicate via voice! The system is set up with text-to-speech capabilities."
    else:
        return f"I heard you say: '{user_input}'. I'm ready for our voice conversation!"


def main():
    """Main function to demonstrate voice capabilities"""
    print("Simple Voice Demo for OpenClaw")
    print("=" * 40)
    print("This demonstrates the voice communication capabilities")
    print("Currently available: Text-to-Speech (TTS)")
    print("Planned: Speech-to-Text (STT) when microphone support is available")
    print()
    
    # Create voice demo instance
    voice_demo = VoiceDemo(simple_responder)
    
    # Demonstrate TTS
    print("Testing TTS (Text-to-Speech)...")
    voice_demo.speak("Hello! Voice communication is now available. I can speak to you using text-to-speech.")
    
    print()
    print("Simulating voice conversation...")
    
    # Simulate some conversation exchanges
    examples = [
        "Hello, how are you?",
        "Can you help me with something?",
        "Tell me about voice communication",
        "Goodbye for now"
    ]
    
    for example in examples:
        print()
        response = voice_demo.chat(example)
    
    print()
    print("=" * 40)
    print("Voice communication demo completed!")
    print()
    print("Next steps to enable full voice communication:")
    print("1. Install PyAudio: pip install pyaudio")
    print("2. Ensure microphone access is enabled")
    print("3. Once microphone is available, real voice input will work")
    print()
    print("Current capabilities:")
    print("- [SUCCESS] Text-to-Speech (pyttsx3) - Working")
    print("- [PENDING] Speech-to-Text (Whisper) - Ready when audio input available") 
    print("- [PENDING] Real-time conversation - Will work when both are connected")


if __name__ == "__main__":
    main()