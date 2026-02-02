#!/usr/bin/env python3
"""
Script to check for and send pending Telegram messages.
This script is designed to be run within OpenClaw's environment where the message tool is available.
"""

import os
from pathlib import Path

def check_and_send_pending_messages():
    """Check for pending Telegram messages and send them."""
    # Define the paths for the pending message files in the workspace root
    # Get the workspace root (assuming it's where this script is located)
    workspace_root = Path.cwd()  # Use current working directory which should be workspace root
    message_file = workspace_root / "pending_telegram_message.txt"
    type_file = workspace_root / "message_type.txt"
    
    # Check if both files exist
    if message_file.exists() and type_file.exists():
        try:
            # Read the message content
            with open(message_file, 'r', encoding='utf-8') as f:
                message = f.read().strip()
            
            # Read the message type
            with open(type_file, 'r', encoding='utf-8') as f:
                message_type = f.read().strip()
            
            # Import and use OpenClaw's message tool
            from openclaw.core.tools.message import message_tool
            
            # Send the message via Telegram
            result = message_tool({
                "action": "send",
                "channel": "telegram",
                "to": 8273779429,  # Your configured chat ID
                "message": message
            })
            
            if result and result.get("ok"):
                print(f"✅ {message_type} message sent successfully to Telegram!")
                
                # Clean up the files after successful sending
                message_file.unlink()
                type_file.unlink()
                
                return True
            else:
                print(f"❌ Failed to send {message_type} message to Telegram: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing pending message: {e}")
            return False
    else:
        print("No pending messages to send")
        return False

if __name__ == "__main__":
    check_and_send_pending_messages()