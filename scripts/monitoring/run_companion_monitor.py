#!/usr/bin/env python3
"""
Wrapper script to run the companion monitor and send it via Telegram
"""

import subprocess
import sys
import os
from datetime import datetime

def run_companion_monitor_and_send():
    """Run the companion monitor script and send results via Telegram"""
    
    # Run the companion monitor script
    result = subprocess.run([
        sys.executable, 
        'openclaw_companion_monitor_final.py'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        error_msg = f"❌ Error running companion monitor:\n{result.stderr}"
        print(error_msg)
        # Send error message to Telegram
        from openclaw.core.tools.message import message_tool
        message_tool({
            "action": "send",
            "channel": "telegram",
            "to": 8273779429,
            "message": error_msg
        })
        return False
    
    # Look for the special marker in the output
    output_lines = result.stdout.strip().split('\n')
    
    if "STATUS_UPDATE_READY" in output_lines:
        # Find the index of STATUS_UPDATE_READY and get the message that follows
        idx = output_lines.index("STATUS_UPDATE_READY")
        if idx + 1 < len(output_lines):
            status_message = output_lines[idx + 1]
            
            # Send the status update via Telegram
            from openclaw.core.tools.message import message_tool
            message_tool({
                "action": "send",
                "channel": "telegram",
                "to": 8273779429,
                "message": status_message
            })
            
            print("✅ Status update sent to Telegram successfully!")
            return True
        else:
            print("❌ Status message not found after STATUS_UPDATE_READY marker")
            return False
    else:
        print("❌ STATUS_UPDATE_READY marker not found in output")
        return False

if __name__ == "__main__":
    print(f"Running companion monitor at {datetime.now()}")
    run_companion_monitor_and_send()