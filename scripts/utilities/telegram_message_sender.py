#!/usr/bin/env python3
"""
Script to monitor for pending Telegram messages and send them using OpenClaw's messaging system.
This should be run within OpenClaw's environment where the message tool is available.
"""

import os
import time
import threading
from pathlib import Path

def send_pending_telegram_message():
    """Check for and send any pending Telegram messages"""
    message_file = Path("pending_telegram_message.txt")
    type_file = Path("message_type.txt")
    
    if message_file.exists() and type_file.exists():
        try:
            # Read the message
            with open(message_file, 'r', encoding='utf-8') as f:
                message = f.read().strip()
            
            # Read the message type
            with open(type_file, 'r', encoding='utf-8') as f:
                message_type = f.read().strip()
            
            # Send the message via OpenClaw's messaging system
            from openclaw.core.tools.message import message_tool
            
            result = message_tool({
                "action": "send",
                "channel": "telegram",
                "to": 8273779429,  # Your chat ID
                "message": message
            })
            
            if result and result.get("ok"):
                print(f"✅ {message_type} message sent successfully to Telegram!")
                
                # Clean up the files after successful sending
                message_file.unlink(missing_ok=True)
                type_file.unlink(missing_ok=True)
                
                return True
            else:
                print(f"❌ Failed to send {message_type} message to Telegram: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending {message_type} message to Telegram: {e}")
            return False
    
    return False

def monitor_for_messages(interval=10):
    """Monitor for pending messages at regular intervals"""
    print(f"Starting Telegram message monitor (checking every {interval} seconds)")
    
    while True:
        sent = send_pending_telegram_message()
        if sent:
            print("Message sent, continuing to monitor...")
        
        time.sleep(interval)

if __name__ == "__main__":
    # Send any pending message immediately when run
    send_pending_telegram_message()
    
    # Optionally, start monitoring loop
    # Uncomment the next line if you want to run continuous monitoring
    # monitor_for_messages(10)