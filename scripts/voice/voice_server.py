#!/usr/bin/env python3
"""
Voice Server for OpenClaw Voice Communications
Implements WebSocket server for real-time voice streaming
"""

import asyncio
import websockets
import json
import base64
import numpy as np
from typing import Dict, Optional
from .audio_utils import AudioUtils
from .stt_engine import STTEngine
from .tts_engine import TTSEngine
import threading
import queue


class VoiceServer:
    """WebSocket server for real-time voice communication"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.stt_engine = STTEngine(engine_type="whisper")
        self.tts_engine = TTSEngine(engine_type="pyttsx3")
        self.ai_callback = None
        
        # Audio processing queues
        self.audio_processing_queue = queue.Queue()
        self.response_queue = queue.Queue()
    
    async def register_client(self, websocket):
        """Register a new client"""
        self.connected_clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.connected_clients)}")
    
    async def unregister_client(self, websocket):
        """Unregister a client"""
        self.connected_clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(self.connected_clients)}")
    
    async def handle_client(self, websocket, path):
        """Handle messages from a client"""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    async def handle_message(self, websocket, message):
        """Handle incoming message from client"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'audio_chunk':
                # Process audio chunk
                audio_data = base64.b64decode(data['audio'])
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                
                # Add to processing queue
                self.audio_processing_queue.put((websocket, audio_array))
                
                # Process in background thread
                processing_thread = threading.Thread(target=self.process_audio_chunk)
                processing_thread.daemon = True
                processing_thread.start()
                
                await websocket.send(json.dumps({
                    'type': 'ack',
                    'message': 'Audio received'
                }))
            
            elif message_type == 'text_input':
                # Handle text input (fallback option)
                text = data['text']
                
                # Process through AI callback if available
                if self.ai_callback:
                    response = self.ai_callback(text)
                    
                    # Convert to speech if TTS is available
                    try:
                        # Generate audio from text
                        import tempfile
                        import os
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                            success = self.tts_engine.save_to_file(text, tmp_file.name, language='en')
                            if success:
                                # Read audio file and send back
                                with open(tmp_file.name, 'rb') as f:
                                    audio_bytes = f.read()
                                
                                await websocket.send(json.dumps({
                                    'type': 'tts_response',
                                    'audio': base64.b64encode(audio_bytes).decode('utf-8'),
                                    'text': response
                                }))
                                
                                # Clean up
                                os.unlink(tmp_file.name)
                    except:
                        # If TTS fails, send text response
                        await websocket.send(json.dumps({
                            'type': 'text_response',
                            'text': response
                        }))
                else:
                    await websocket.send(json.dumps({
                        'type': 'text_response',
                        'text': f"I received: {text}. Voice server is working!"
                    }))
            
            elif message_type == 'ping':
                await websocket.send(json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp')
                }))
        
        except Exception as e:
            print(f"Error handling message: {str(e)}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    def process_audio_chunk(self):
        """Process audio chunk in background thread"""
        try:
            if not self.audio_processing_queue.empty():
                websocket, audio_array = self.audio_processing_queue.get()
                
                # Transcribe audio
                text = self.stt_engine.transcribe_audio(audio_array)
                
                if text:
                    print(f"Transcribed: {text}")
                    
                    # Process through AI callback if available
                    if self.ai_callback:
                        response = self.ai_callback(text)
                        
                        # Convert response to speech
                        import tempfile
                        import os
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                            success = self.tts_engine.save_to_file(response, tmp_file.name, language='en')
                            if success:
                                # Read audio file and send back
                                with open(tmp_file.name, 'rb') as f:
                                    audio_bytes = f.read()
                                
                                # Send response back to client
                                asyncio.run_coroutine_threadsafe(
                                    self.send_to_client(websocket, {
                                        'type': 'tts_response',
                                        'audio': base64.b64encode(audio_bytes).decode('utf-8'),
                                        'text': response,
                                        'transcribed_text': text
                                    }),
                                    loop=asyncio.get_event_loop()
                                )
                                
                                # Clean up
                                os.unlink(tmp_file.name)
                    else:
                        # Send text response if no AI callback
                        asyncio.run_coroutine_threadsafe(
                            self.send_to_client(websocket, {
                                'type': 'text_response',
                                'text': text
                            }),
                            loop=asyncio.get_event_loop()
                        )
        except Exception as e:
            print(f"Error processing audio chunk: {str(e)}")
    
    async def send_to_client(self, websocket, data):
        """Send data to a specific client"""
        if websocket in self.connected_clients:  # Check if client is still connected
            try:
                await websocket.send(json.dumps(data))
            except websockets.exceptions.ConnectionClosed:
                pass  # Client disconnected
    
    async def broadcast(self, data):
        """Broadcast data to all connected clients"""
        if self.connected_clients:  # Check if there are any connected clients
            # Remove disconnected clients
            disconnected_clients = set()
            for client in self.connected_clients:
                try:
                    await client.send(json.dumps(data))
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.add(client)
            
            # Remove disconnected clients from the set
            self.connected_clients -= disconnected_clients
    
    def set_ai_callback(self, callback_func):
        """Set the AI callback function"""
        self.ai_callback = callback_func
    
    def start_server(self):
        """Start the WebSocket server"""
        print(f"Starting voice server on {self.host}:{self.port}")
        
        # Set up the event loop for the server
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        start_server = websockets.serve(self.handle_client, self.host, self.port)
        server = loop.run_until_complete(start_server)
        
        try:
            print(f"Voice server running on ws://{self.host}:{self.port}")
            loop.run_forever()
        except KeyboardInterrupt:
            print("Shutting down voice server...")
            server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()


def example_ai_callback(text: str) -> str:
    """Example AI callback function"""
    # This would normally connect to OpenClaw's processing
    if "hello" in text.lower() or "hi" in text.lower():
        return "Hello! I'm your AI assistant. How can I help you today?"
    elif "how are you" in text.lower():
        return "I'm doing well, thank you for asking! How can I assist you?"
    elif "bye" in text.lower():
        return "Goodbye! Feel free to start another conversation anytime."
    else:
        return f"I heard you say: '{text}'. How else can I help you?"


if __name__ == "__main__":
    # Test the voice server
    print("Initializing voice server...")
    
    server = VoiceServer(host="localhost", port=8765)
    server.set_ai_callback(example_ai_callback)
    
    print("Voice server initialized. Starting server...")
    print("Connect to ws://localhost:8765 from a WebSocket client")
    
    try:
        server.start_server()
    except Exception as e:
        print(f"Server error: {str(e)}")