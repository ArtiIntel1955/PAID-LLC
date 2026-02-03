#!/usr/bin/env python3
"""
Setup script for Voice Communication System
Installs required dependencies for voice functionality
"""

import subprocess
import sys


def install_package(package_name: str) -> bool:
    """
    Install a Python package using pip
    """
    try:
        print(f"[INFO] Installing {package_name}...")
        result = subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"[SUCCESS] {package_name} installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to install {package_name}")
        return False


def main():
    print("Setting up Voice Communication System for OpenClaw...")
    print("=" * 60)
    
    # Install required packages
    required_packages = [
        "pyaudio",           # For audio I/O
        "numpy",             # For numerical operations
        "soundfile",         # For audio file handling
        "speech-recognition", # For speech recognition
        "pyttsx3",           # For text-to-speech
        "pygame",            # For audio playback
        "websockets",        # For WebSocket server (if using voice server)
        "openai-whisper"     # For local speech recognition
    ]
    
    print("\nInstalling required packages...")
    successful_installs = 0
    
    for package in required_packages:
        if install_package(package):
            successful_installs += 1
        print()  # Empty line for readability
    
    print("=" * 60)
    print(f"Setup completed! Successfully installed {successful_installs}/{len(required_packages)} packages.")
    
    if successful_installs == len(required_packages):
        print("\n🎉 Voice Communication System setup completed successfully!")
        print("\nYou can now use voice communication with OpenClaw!")
        print("\nTo start a voice conversation:")
        print("  python -c \"from scripts.voice.voice_conversation import VoiceConversationManager, simple_ai_responder; vm = VoiceConversationManager(); vm.start_conversation(simple_ai_responder)\"")
        print("\nTo start the voice server:")
        print("  python scripts/voice/voice_server.py")
    else:
        print(f"\n⚠️  Some packages failed to install. {len(required_packages) - successful_installs} packages may be missing.")
        print("Please install them manually using: pip install <package_name>")
    
    print("\nNote: On some systems, you may need to install additional system dependencies")
    print("for PyAudio to work properly (like PortAudio on Linux/macOS).")


if __name__ == "__main__":
    main()