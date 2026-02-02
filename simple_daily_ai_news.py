import requests
import json
from datetime import datetime
import os

def get_daily_ai_news():
    """Fetch the latest AI news from multiple sources"""
    
    # Using NewsAPI to get tech/AI related news
    api_key = os.getenv('NEWS_API_KEY', 'YOUR_NEWS_API_KEY')
    
    # Alternative: Using a free tech news API
    try:
        # TechCrunch API endpoint for technology news
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'artificial intelligence OR AI OR machine learning',
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 5,
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('articles'):
            articles = data['articles'][:3]  # Get top 3 articles
            
            news_text = f"Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\n"
            
            for i, article in enumerate(articles, 1):
                title = article.get('title', 'No Title')
                description = article.get('description', '')[:150] + "..." if article.get('description') else ''
                url = article.get('url', '')
                
                news_text += f"{i}. {title}\n"
                news_text += f"{description}\n"
                news_text += f"Read more: {url}\n\n"
                
            return news_text
        else:
            return f"Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\nFailed to fetch news. Please check the API configuration."
    
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return f"Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\nError fetching news: {str(e)}"

def get_alternative_news():
    """Alternative method to get tech news if primary method fails"""
    try:
        # Hacker News API for tech-related stories
        hn_url = "https://hacker-news.firebaseio.com/v0/topstories.json?limitToFirst=5&print=pretty"
        response = requests.get(hn_url)
        story_ids = response.json()[:3]
        
        news_text = f"Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        for i, story_id in enumerate(story_ids, 1):
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
            item_response = requests.get(item_url)
            item = item_response.json()
            
            if item and item.get('title') and ('AI' in item['title'] or 'artificial intelligence' in item['title'].lower() or 'machine learning' in item['title'].lower()):
                title = item.get('title', 'No Title')
                url = item.get('url', '')
                
                news_text += f"{i}. {title}\n"
                if url:
                    news_text += f"Read more: {url}\n\n"
                else:
                    news_text += "\n"
        
        if len(news_text) < 100:  # If we didn't get any relevant AI stories
            news_text = f"Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\nNo specific AI stories found today, but here are some top tech news items:\n\n"
            for i, story_id in enumerate(story_ids, 1):
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
                item_response = requests.get(item_url)
                item = item_response.json()
                
                title = item.get('title', 'No Title')
                url = item.get('url', '')
                
                news_text += f"{i}. {title}\n"
                if url:
                    news_text += f"Read more: {url}\n\n"
                else:
                    news_text += "\n"
        
        return news_text
    except Exception as e:
        print(f"Error with alternative news source: {str(e)}")
        return f"Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\nError fetching news from alternative source: {str(e)}"

if __name__ == "__main__":
    # When run directly, just print the news
    news = get_daily_ai_news()
    print(news)