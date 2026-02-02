#!/usr/bin/env python3
"""
Handler for Telegram messages that can be called from within OpenClaw's environment
"""

import os
import sys
from pathlib import Path

def handle_pending_telegram_messages():
    """Check for and send any pending Telegram messages"""
    workspace_dir = Path(__file__).parent
    message_file = workspace_dir / "pending_telegram_message.txt"
    type_file = workspace_dir / "message_type.txt"
    
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
                
                return True, f"{message_type} message sent successfully"
            else:
                error_msg = f"Failed to send {message_type} message to Telegram: {result}"
                print(error_msg)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error sending {message_type} message to Telegram: {e}"
            print(error_msg)
            return False, error_msg
    
    return False, "No pending messages"

# This function can be called from within OpenClaw's environment
def run_handler():
    success, message = handle_pending_telegram_messages()
    return success, message

if __name__ == "__main__":
    success, message = handle_pending_telegram_messages()
    print(f"Handler result: {message}")