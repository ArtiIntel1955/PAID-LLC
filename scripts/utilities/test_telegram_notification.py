#!/usr/bin/env python3
"""
Test script to send a Telegram notification using OpenClaw's messaging system.
This script is designed to work within the OpenClaw environment.
"""

import json
import datetime
import subprocess
import sys
import os

def send_test_message():
    """Send a test message to Telegram using OpenClaw's message tool"""
    message = f"Test notification from OpenClaw system\nTime: {datetime.datetime.now()}\nThis confirms your Telegram notifications are working!"
    
    try:
        # Use the OpenClaw message tool to send the message
        # This should work since we're within the OpenClaw environment
        result = subprocess.run([
            sys.executable, '-c',
            f'''
import sys
sys.path.insert(0, r"C:\\Users\\MyAIE\\AppData\\Roaming\\npm\\node_modules\\openclaw")
from openclaw.core.tools.message import message_tool
result = message_tool({{
    "action": "send",
    "channel": "telegram",
    "to": 8273779429,
    "message": """{message}"""
}})
print(result)
            '''
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Test message sent successfully!")
            print(result.stdout)
        else:
            print("❌ Failed to send test message")
            print("Error:", result.stderr)
            
    except Exception as e:
        print(f"Error sending test message: {e}")

def send_status_update_via_api():
    """Alternative method to send status update using OpenClaw's API"""
    # Since we're having trouble with the direct import, let's try using OpenClaw's gateway API
    try:
        import requests
        import json
        
        # Get the OpenClaw gateway token and URL from environment or config
        gateway_token = "7c3c42cf4e8afa06ef4968f0df1e33057b718353a1ec2df3"  # From openclaw.json
        gateway_url = "http://localhost:18789"  # From openclaw.json
        
        # Prepare the message
        status_data = {
            "version": "2026.1.29",
            "uptime": "Active since January 30, 2026",
            "model_used": "qwen-portal/coder-model",
            "tokens_processed": {"in": 389, "out": 207},
            "active_sessions": 1,
            "recent_activities": [
                "Created PAID LLC business website",
                "Set up daily AI news digest",
                "Configured Telegram messaging"
            ]
        }
        
        formatted_message = f"""OpenClaw Status Update
_{datetime.datetime.now().strftime('%B %d, %Y - %H:%M:%S')}_*

*Version:* {status_data['version']}
*Status:* Active
*Model:* {status_data['model_used']}
*Uptime:* {status_data['uptime']}
*Tokens:* {status_data['tokens_processed']['in']} in / {status_data['tokens_processed']['out']} out
*Active Sessions:* {status_data['active_sessions']}

*Recent Activities:*
""" + "\n".join([f"- {activity}" for activity in status_data['recent_activities']])

        # Send the message using OpenClaw's API
        headers = {
            'Authorization': f'Bearer {gateway_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "action": "send",
            "channel": "telegram",
            "to": 8273779429,
            "message": formatted_message
        }
        
        response = requests.post(f"{gateway_url}/api/message", headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ Status update sent successfully via API!")
        else:
            print(f"❌ Failed to send status update via API: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error sending status update via API: {e}")

if __name__ == "__main__":
    print("Testing Telegram notifications...")
    send_test_message()
    print("\nTrying alternative method...")
    send_status_update_via_api()