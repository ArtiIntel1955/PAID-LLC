# Telegram AI & OpenClaw News Digest Setup

## Overview
This system will send you a daily digest of AI news and OpenClaw updates via Telegram. The digest runs automatically each day and can be easily enabled/disabled as needed.

## Prerequisites
- Telegram bot set up and configured with OpenClaw
- Python installed on your system (already confirmed: v24.13.0)

## Setup Instructions

### 1. Enable Telegram Integration (if not already set up)
Make sure your Telegram bot is properly configured in OpenClaw. You'll need:
- Bot token from @BotFather
- Your chat ID for direct messaging

### 2. Configure the News Digest
The system is initially disabled. You can customize the configuration in `news_digest_config.json`:

```json
{
  "enabled": false,  // Change to true to enable
  "sources": [...],  // News sources to monitor
  "delivery_time": "09:00",  // Daily delivery time (24-hour format)
  "max_items": 10  // Maximum news items per digest
}
```

### 3. Enable the Digest
To enable the daily digest:
1. Edit `news_digest_config.json`
2. Change `"enabled": false` to `"enabled": true`
3. Save the file

### 4. Schedule the Task
Use Windows Task Scheduler to run the script daily:

1. Open Task Scheduler
2. Create Basic Task
3. Name: "PAID Daily AI News Digest"
4. Trigger: Daily at your preferred time (default 9:00 AM)
5. Action: Start a program
6. Program: `python`
7. Arguments: `C:\Users\MyAIE\.openclaw\workspace\daily_news_digest.py`
8. Start in: `C:\Users\MyAIE\.openclaw\workspace`

## Control Options

### Enable/Disable
- **Enable**: Set `"enabled": true` in `news_digest_config.json`
- **Disable**: Set `"enabled": false` in `news_digest_config.json`

### Adjust Content
- Modify the `"sources"` array to add/remove news sources
- Change `"max_items"` to show more or fewer articles
- Adjust `"delivery_time"` to change when you receive the digest

### Pause Temporarily
- To pause without changing configuration, disable the scheduled task in Windows Task Scheduler

## Testing
Before enabling daily delivery, you can test the script manually:
```
python daily_news_digest.py
```

This will run the script once and show you what the output would look like.

## Troubleshooting
- If you don't receive messages, check that your Telegram bot is properly configured
- Verify the Python script path in your scheduled task
- Check that `news_digest_config.json` has the correct syntax

## Safety Features
- The system is disabled by default
- Easy on/off switch via configuration file
- Limited number of items to prevent spam
- All settings can be modified without touching code

Note: The current implementation is a framework. Actual news fetching and Telegram delivery will require additional configuration based on your specific Telegram bot settings.