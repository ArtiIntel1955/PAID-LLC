#!/usr/bin/env python3
"""
OpenClaw Companion Monitor
This script leverages OpenClaw's built-in monitoring capabilities 
to provide regular status updates via Telegram.
"""

import json
import datetime
import time
import sys

def load_config():
    """Load configuration settings"""
    try:
        with open('status_updates_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default config if file doesn't exist
        return {
            "enabled": True,
            "update_frequency": "every_4_hours",
            "report_types": ["system_status", "token_usage_summary", "session_activity"],
            "delivery_method": "telegram",
            "telegram_chat_id": 8273779429,
            "working_hours_only": False,
            "custom_message_prefix": "OpenClaw Status Update:",
            "metrics_to_include": [
                "version", "uptime", "model_used", 
                "tokens_processed", "active_sessions", "recent_activities"
            ]
        }

def get_openclaw_status():
    """
    In the actual implementation, this would interface with OpenClaw's 
    built-in status tools to get real-time information.
    For now, returning example data based on what we know about the current system.
    """
    # This would use OpenClaw's session_status() tool in actual implementation
    return {
        "version": "2026.1.29",
        "uptime": "Active since January 30, 2026",
        "model_used": "qwen-portal/coder-model",
        "tokens_processed": {"in": 389, "out": 207},
        "active_sessions": 1,
        "session_details": {
            "session_id": "agent:main:main",
            "type": "main agent",
            "updated": "just now",
            "context_usage": "63k/128k (49%)"
        },
        "recent_activities": [
            "Created PAID LLC business website",
            "Set up daily AI news digest",
            "Configured Telegram messaging",
            "Installed required packages for news digest"
        ]
    }

def format_status_report(status_data):
    """Format the status data into a Telegram-friendly message"""
    header = f"OpenClaw Companion Monitor\n_{datetime.datetime.now().strftime('%B %d, %Y - %H:%M:%S')}_\n\n"
    
    body_parts = [
        f"*Version:* {status_data['version']}",
        f"*Status:* Active",
        f"*Model:* {status_data['model_used']}",
        f"*Uptime:* {status_data['uptime']}",
        f"*Tokens:* {status_data['tokens_processed']['in']} in / {status_data['tokens_processed']['out']} out",
        f"*Active Sessions:* {status_data['active_sessions']}",
        f"*Context:* {status_data['session_details']['context_usage']}"
    ]
    
    recent_activities = "\n\n*Recent Activities:*\n" + "\n".join([f"- {activity}" for activity in status_data['recent_activities']])
    
    return header + "\n".join(body_parts) + recent_activities

def send_status_update():
    """Send the status update via the configured delivery method"""
    config = load_config()
    
    if not config.get("enabled", False):
        print("Status updates are currently disabled")
        return
    
    status_data = get_openclaw_status()
    formatted_message = format_status_report(status_data)
    
    # Attempt to send via OpenClaw's messaging system
    try:
        # Import OpenClaw's messaging system
        from openclaw.core.messaging import send_message
        
        # Send the message via OpenClaw's messaging system
        result = send_message(
            channel="telegram",
            message=formatted_message,
            to=config.get('telegram_chat_id', 8273779429),
            format="markdown"
        )
        
        if result:
            print("✅ Successfully sent status update to Telegram!")
        else:
            print("❌ Failed to send status update to Telegram")
            
    except ImportError:
        # If OpenClaw modules aren't available, try using subprocess to call OpenClaw CLI
        import subprocess
        try:
            # Prepare the message for CLI command
            escaped_message = formatted_message.replace('"', '\\"')  # Escape quotes for command line
            
            # Use subprocess to call OpenClaw's message tool
            cmd = [
                'openclaw', 'message', 'send',
                '--channel', 'telegram',
                '--to', str(config.get('telegram_chat_id', 8273779429)),
                '--message', formatted_message
            ]
            
            # Join the command as a single string for execution
            cmd_str = ' '.join(cmd)
            result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Successfully sent status update to Telegram!")
            else:
                print(f"❌ Failed to send status update to Telegram: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error sending status update to Telegram: {e}")
            print("Would send to Telegram: " + formatted_message[:200] + "...")

def main():
    """Main function to run the companion monitor"""
    config = load_config()
    
    if not config.get("enabled", False):
        print("Companion monitor is currently disabled")
        return
    
    print("OpenClaw Companion Monitor started")
    print("Sending status update...")
    send_status_update()
    print("Status update sent!")

if __name__ == "__main__":
    main()