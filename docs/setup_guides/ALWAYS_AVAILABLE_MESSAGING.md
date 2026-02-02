# Always Available Messaging Setup

## Overview
To enable messaging at any time during the day, your computer needs to remain accessible to receive and process messages. Here are your options:

## Option 1: Adjust Sleep Settings (Recommended for desktop)
1. Open Control Panel > Power Options
2. Select "High Performance" or "Balanced" power plan
3. Click "Change plan settings" 
4. Set "Put the computer to sleep" to "Never" or a very long duration (e.g., 4+ hours)
5. This keeps your computer running so OpenClaw can respond immediately

## Option 2: Enable Wake on Network Activity
1. Open Device Manager
2. Expand "Network Adapters"
3. Right-click your network adapter
4. Go to Properties > Advanced tab
5. Look for "Wake on Magic Packet", "Wake on Pattern Match", or similar
6. Set to "Enabled"
7. Also check Power Management tab and ensure "Allow this device to wake the computer" is checked

## Option 3: Scheduled Wake Times
Instead of keeping the computer on 24/7, schedule it to wake during your typical active hours:
1. In Task Scheduler, create additional wake tasks for times you typically message
2. Create wake tasks at intervals (e.g., every 2 hours during the day)
3. Use "shutdown /h" command to return to hibernation when not needed

## Option 4: Cloud/Remote Solution (Best for reliability)
For true 24/7 availability:
- Run OpenClaw on a cloud server (AWS, Azure, etc.)
- Use a Raspberry Pi or similar always-on device
- Host on a virtual private server (VPS)

## Current Behavior
With the current setup:
- You can send messages anytime, but they'll be processed when the computer wakes up
- The daily digest will run at 9:00 AM as scheduled
- Response delays occur when the computer is sleeping

## Recommendation
For a desktop PC, Option 1 (adjusting sleep settings) is simplest. For a laptop, you might prefer Option 3 (scheduled wake times) to balance availability with power consumption.