import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.scheduled.daily_ai_news import get_daily_ai_news, get_alternative_news

async def send_daily_ai_news():
    """
    Function to send daily AI news to Telegram
    This will be called by the OpenClaw cron job
    """
    try:
        # Get the daily AI news
        news_content = get_daily_ai_news()
        
        # If the primary source fails, try the alternative
        if "Error" in news_content or "Failed" in news_content:
            news_content = get_alternative_news()
        
        # Print the news content so OpenClaw can capture it and send via Telegram
        print(f"TELEGRAM_MESSAGE: {news_content}")
        
        return news_content
        
    except Exception as e:
        error_msg = f"Error in daily AI news: {str(e)}"
        print(f"TELEGRAM_MESSAGE: {error_msg}")
        return error_msg

if __name__ == "__main__":
    # When run directly, just print the news
    # Set the console encoding to UTF-8 to handle Unicode characters
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    elif os.name == 'nt':
        os.system('chcp 65001 > nul')
    
    news = get_daily_ai_news()
    print(news.encode('utf-8', errors='replace').decode('utf-8'))