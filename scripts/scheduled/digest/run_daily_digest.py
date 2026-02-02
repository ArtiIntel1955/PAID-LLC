#!/usr/bin/env python3
"""
Wrapper script to run the daily digest and send it via Telegram
"""

import subprocess
import sys
import os
from datetime import datetime

def run_daily_digest_and_send():
    """Run the daily digest script and send results via Telegram"""
    
    # Run the daily digest script
    result = subprocess.run([
        sys.executable, 
        'daily_news_digest_final.py'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        error_msg = f"❌ Error running daily digest:\n{result.stderr}"
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
    
    if "DIGEST_READY" in output_lines:
        # Find the index of DIGEST_READY and get the message that follows
        idx = output_lines.index("DIGEST_READY")
        if idx + 1 < len(output_lines):
            digest_message = output_lines[idx + 1]
            
            # Send the digest via Telegram
            from openclaw.core.tools.message import message_tool
            message_tool({
                "action": "send",
                "channel": "telegram",
                "to": 8273779429,
                "message": digest_message
            })
            
            print("✅ Daily digest sent to Telegram successfully!")
            return True
        else:
            print("❌ Digest message not found after DIGEST_READY marker")
            return False
    else:
        print("❌ DIGEST_READY marker not found in output")
        return False

if __name__ == "__main__":
    print(f"Running daily digest at {datetime.now()}")
    run_daily_digest_and_send()