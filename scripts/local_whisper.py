#!/usr/bin/env python3
"""
Local Whisper Speech-to-Text for OpenClaw
Uses local Whisper installation for free speech recognition
"""

import sys
import subprocess
import os
import json
from pathlib import Path


def transcribe_audio_local(audio_file_path: str, model: str = "base") -> dict:
    """
    Transcribe audio file using local Whisper (CLI or library)
    """
    try:
        # Verify the audio file exists
        if not os.path.exists(audio_file_path):
            return {
                'error': f'Audio file does not exist: {audio_file_path}',
                'success': False
            }
        
        # First try the CLI version
        try:
            result = subprocess.run(['whisper', '--help'], capture_output=True, text=True)
            if result.returncode == 0:
                # CLI is available, use it
                output_file = f"{audio_file_path.rsplit('.', 1)[0]}.txt"
                cmd = [
                    'whisper',
                    audio_file_path,
                    '--model', model,
                    '--output_format', 'txt',
                    '--output_dir', os.path.dirname(output_file)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Read the transcribed text
                    with open(output_file, 'r', encoding='utf-8') as f:
                        transcription = f.read()
                    
                    return {
                        'success': True,
                        'transcription': transcription.strip(),
                        'output_file': output_file,
                        'model_used': model,
                        'audio_file': audio_file_path
                    }
                else:
                    return {
                        'error': f'Whisper CLI transcription failed: {result.stderr}',
                        'success': False
                    }
        except FileNotFoundError:
            # CLI not available, try library approach
            pass
        
        # If CLI fails, try using the library directly
        try:
            import whisper
            model_instance = whisper.load_model(model)
            result = model_instance.transcribe(audio_file_path)
            
            return {
                'success': True,
                'transcription': result['text'].strip(),
                'model_used': model,
                'audio_file': audio_file_path
            }
        except ImportError:
            return {
                'error': 'Neither Whisper CLI nor Whisper library is available. Install with: pip install openai-whisper',
                'success': False
            }
        except Exception as e:
            return {
                'error': f'Whisper transcription failed: {str(e)}',
                'success': False
            }
    
    except Exception as e:
        return {
            'error': f'Error during transcription: {str(e)}',
            'success': False
        }


def transcribe_with_timestamps(audio_file_path: str, model: str = "base") -> dict:
    """
    Transcribe audio with timestamps using local Whisper
    """
    try:
        if not os.path.exists(audio_file_path):
            return {
                'error': f'Audio file does not exist: {audio_file_path}',
                'success': False
            }
        
        # Run Whisper with VTT output for timestamps
        base_name = audio_file_path.rsplit('.', 1)[0]
        cmd = [
            'whisper',
            audio_file_path,
            '--model', model,
            '--output_format', 'vtt',  # VTT includes timestamps
            '--output_dir', os.path.dirname(base_name)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            vtt_file = f"{base_name}.vtt"
            if os.path.exists(vtt_file):
                with open(vtt_file, 'r', encoding='utf-8') as f:
                    vtt_content = f.read()
                
                return {
                    'success': True,
                    'vtt_content': vtt_content,
                    'output_file': vtt_file,
                    'model_used': model,
                    'audio_file': audio_file_path
                }
            else:
                return {
                    'error': 'Output file was not created',
                    'success': False
                }
        else:
            return {
                'error': f'Whisper transcription failed: {result.stderr}',
                'success': False
            }
    
    except Exception as e:
        return {
            'error': f'Error during transcription: {str(e)}',
            'success': False
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python local_whisper.py <audio_file_path> [model]")
        print("Models: tiny, base, small, medium, large (default: base)")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    result = transcribe_audio_local(audio_file, model)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()