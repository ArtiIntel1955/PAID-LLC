import requests
import json
from datetime import datetime
import os

def get_daily_ai_news():
    """Fetch the latest AI news from multiple sources"""
    
    # Using NewsAPI to get tech/AI related news
    api_key = os.getenv('NEWS_API_KEY', 'YOUR_NEWS_API_KEY')
    
    # Primary: Using NewsAPI to get tech/AI related news
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
        
        if data.get('articles') and response.status_code == 200:
            articles = data['articles'][:3]  # Get top 3 articles
            
            news_text = f"🤖 Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\n"
            
            for i, article in enumerate(articles, 1):
                title = article.get('title', 'No Title')
                description = article.get('description', '')[:150] + "..." if article.get('description') else ''
                url = article.get('url', '')
                
                news_text += f"{i}. *{title}*\n"
                news_text += f"_{description}_\n"
                news_text += f"[Read more]({url})\n\n"
                
            return news_text
        else:
            # If the primary API fails or returns no results, try the alternative
            return get_alternative_news()
    except Exception as e:
        # If the primary API fails, try the alternative
        print(f"Primary news source failed: {str(e)}, trying alternative source")
        return get_alternative_news()

def get_alternative_news():
    """Alternative method to get tech news if primary method fails"""
    try:
        # Hacker News API for tech-related stories
        hn_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(hn_url)
        all_story_ids = response.json()
        story_ids = all_story_ids[:5]  # Get first 5 story IDs
        
        news_text = f"🤖 Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        ai_stories_found = []
        for story_id in story_ids:
            if len(ai_stories_found) >= 3:  # We only need 3 AI stories
                break
                
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            item_response = requests.get(item_url)
            item = item_response.json()
            
            if item and item.get('title') and (
                'AI' in item['title'] or 
                'artificial intelligence' in item['title'].lower() or 
                'machine learning' in item['title'].lower() or
                'neural network' in item['title'].lower()
            ):
                ai_stories_found.append(item)
        
        # If we found AI-related stories, display them
        if ai_stories_found:
            for i, item in enumerate(ai_stories_found, 1):
                title = item.get('title', 'No Title')
                url = item.get('url', '')
                
                news_text += f"{i}. *{title}*\n"
                if url:
                    news_text += f"[Read more]({url})\n\n"
                else:
                    news_text += "\n"
        else:
            # If no AI stories were found, show general tech stories
            news_text = f"🤖 Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\nNo specific AI stories found today, but here are some top tech news items:\n\n"
            for i in range(min(3, len(story_ids))):
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_ids[i]}.json"
                item_response = requests.get(item_url)
                item = item_response.json()
                
                title = item.get('title', 'No Title')
                url = item.get('url', '')
                
                news_text += f"{i+1}. *{title}*\n"
                if url:
                    news_text += f"[Read more]({url})\n\n"
                else:
                    news_text += "\n"
        
        return news_text
    
    except Exception as e:
        print(f"Error with alternative news source: {str(e)}")
        return f"🤖 Daily AI News Update - {datetime.now().strftime('%B %d, %Y')}\n\nError fetching news from alternative source: {str(e)}"

if __name__ == "__main__":
    print(get_daily_ai_news())