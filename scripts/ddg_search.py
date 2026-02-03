#!/usr/bin/env python3
"""
DuckDuckGo Search Tool for OpenClaw
Provides free web search capability using DuckDuckGo
"""

import sys
import json
import urllib.parse
import requests
from typing import Dict, List, Optional


def search_ddg(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search DuckDuckGo using the Instant Answer API
    """
    try:
        # DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        # Add the main answer if available
        if data.get('AbstractText'):
            results.append({
                'title': data.get('Heading', 'DuckDuckGo Result'),
                'body': data['AbstractText'],
                'url': data.get('AbstractURL', ''),
                'source': 'DuckDuckGo'
            })
        
        # Add related topics
        for topic in data.get('RelatedTopics', [])[:max_results-1]:
            if 'FirstURL' in topic and 'Text' in topic:
                results.append({
                    'title': topic.get('Name', 'Related Topic'),
                    'body': topic['Text'],
                    'url': topic['FirstURL'],
                    'source': 'DuckDuckGo'
                })
        
        # If we don't have enough results, try the web search
        if len(results) < max_results:
            # Use DuckDuckGo Lite for additional results
            search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw Assistant)'
            }
            # Note: This is a simplified implementation
            # In a real scenario, we'd need to parse the HTML response
        
        return results[:max_results]
    
    except Exception as e:
        print(f"Error searching DuckDuckGo: {str(e)}", file=sys.stderr)
        return []


def search_ddg_lite(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Alternative DuckDuckGo search using lite version
    """
    try:
        # Use the lite version of DuckDuckGo
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw Assistant)'
        }
        search_url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}&kl=us-en"
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # This is a simplified approach - in production we would parse the HTML
        # For now, we'll use the API approach which is more reliable
        return search_ddg(query, max_results)
        
    except Exception as e:
        print(f"Error with DDG Lite: {str(e)}", file=sys.stderr)
        return []


def main():
    if len(sys.argv) < 2:
        print("Usage: python ddg_search.py <query> [max_results]")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    results = search_ddg(query, max_results)
    
    if results:
        print(json.dumps(results, indent=2))
    else:
        print(json.dumps([]))


if __name__ == "__main__":
    main()