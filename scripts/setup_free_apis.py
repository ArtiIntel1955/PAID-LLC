#!/usr/bin/env python3
"""
Setup script for Free APIs Enhancement for OpenClaw
Installs required dependencies for DuckDuckGo search, YouTube transcripts, and local Whisper
"""

import subprocess
import sys
import os


def install_package(package_name: str) -> bool:
    """
    Install a Python package using pip
    """
    try:
        print(f"Installing {package_name}...")
        result = subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"[SUCCESS] {package_name} installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to install {package_name}")
        return False


def check_command_exists(command: str) -> bool:
    """
    Check if a command-line tool exists
    """
    try:
        subprocess.check_call(["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def main():
    print("Setting up Free APIs Enhancement for OpenClaw...")
    print("=" * 50)
    
    # Install Python packages
    required_packages = [
        "requests",           # For HTTP requests
        "youtube-transcript-api",  # For YouTube transcripts
        "openai-whisper"     # For local Whisper (will install whisper-ctranslate and other deps)
    ]
    
    print("\nInstalling Python packages...")
    for package in required_packages:
        install_package(package)
    
    print("\nChecking for command-line tools...")
    
    # Check if Whisper CLI is available
    if check_command_exists("whisper"):
        print("✓ Whisper CLI is already available")
    else:
        print("? Whisper CLI not found. Installing with pip...")
        install_package("openai-whisper")
    
    print("\n" + "=" * 50)
    print("Setup completed!")
    print("\nYou can now use these enhanced capabilities:")
    print("- DuckDuckGo search: python scripts/free_apis_enhancement.py search_ddg 'query'")
    print("- Weather lookup: python scripts/free_apis_enhancement.py weather 'location'")
    print("- YouTube transcripts: python scripts/free_apis_enhancement.py youtube_transcript 'video_url'")
    print("- Local Whisper transcription: python scripts/free_apis_enhancement.py whisper 'audio_file'")
    print("\nNote: For Brave Search, use OpenClaw's built-in web_search tool.")


if __name__ == "__main__":
    main()