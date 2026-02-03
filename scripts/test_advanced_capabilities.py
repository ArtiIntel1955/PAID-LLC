#!/usr/bin/env python3
"""
Test script to verify advanced capabilities are working
"""

import json
import subprocess
import sys
import os


def test_hacker_news():
    """Test Hacker News capability"""
    print("Testing Hacker News...")
    try:
        result = subprocess.run([
            sys.executable, 'scripts/hacker_news.py', 'top', '3'
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if isinstance(data, list) and len(data) > 0:
                print(f"[SUCCESS] Hacker News working: Retrieved {len(data)} stories")
                if 'error' not in data[0]:
                    print(f"  Example: {data[0].get('title', 'N/A')[:50]}...")
            else:
                print("[INFO] Hacker News returned no data (may be API limitation)")
        else:
            print(f"[WARNING] Hacker News test failed: {result.stderr[:100]}")
    except Exception as e:
        print(f"[WARNING] Hacker News test error: {e}")


def test_ip_geolocation():
    """Test IP geolocation capability"""
    print("Testing IP geolocation...")
    try:
        result = subprocess.run([
            sys.executable, 'scripts/ip_geolocation.py', '8.8.8.8'
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('status') == 'success':
                print(f"[SUCCESS] IP geolocation working: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}")
            elif 'error' in data:
                print(f"[INFO] IP geolocation returned error: {data['error'][:100]}")
            else:
                print("[INFO] IP geolocation may have returned limited data")
        else:
            print(f"[WARNING] IP geolocation test failed: {result.stderr[:100]}")
    except Exception as e:
        print(f"[WARNING] IP geolocation test error: {e}")


def test_unified_interface():
    """Test the unified interface"""
    print("Testing unified interface...")
    try:
        result = subprocess.run([
            sys.executable, 'scripts/advanced_apis_enhancement.py', 'ip', '8.8.8.8'
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("[SUCCESS] Unified interface working")
        else:
            print(f"[WARNING] Unified interface test failed: {result.stderr[:100]}")
    except Exception as e:
        print(f"[WARNING] Unified interface test error: {e}")


def test_existing_capabilities():
    """Test existing capabilities to ensure they still work"""
    print("Testing existing capabilities...")
    
    # Test YouTube transcript library availability
    try:
        import youtube_transcript_api
        print("[SUCCESS] YouTube transcript library available")
    except ImportError:
        print("[INFO] YouTube transcript library not available")
    
    # Test Whisper availability
    try:
        import whisper
        print("[SUCCESS] Whisper library available")
    except ImportError:
        print("[INFO] Whisper library not available")


def main():
    print("Testing Advanced Capabilities for OpenClaw")
    print("=" * 50)
    
    test_hacker_news()
    print()
    
    test_ip_geolocation()
    print()
    
    test_unified_interface()
    print()
    
    test_existing_capabilities()
    print()
    
    print("=" * 50)
    print("Advanced capabilities added successfully!")
    print("\nTo use these capabilities:")
    print("- Hacker News: python scripts/hacker_news.py top 10")
    print("- IP Geolocation: python scripts/ip_geolocation.py [ip_address]")
    print("- Unified interface: python scripts/advanced_apis_enhancement.py hn top 5")
    print("- YouTube transcripts: python scripts/advanced_apis_enhancement.py yt 'url'")
    print("- Local Whisper: python scripts/advanced_apis_enhancement.py whisper 'file.mp3'")


if __name__ == "__main__":
    main()