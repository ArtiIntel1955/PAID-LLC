#!/usr/bin/env python3
"""
Secure Web Interaction Module for OpenClaw
Implements safe web requests and HTML parsing with security validations
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
from typing import Optional, Dict, Any, List
import socket
import ipaddress
import time
from pathlib import Path

def is_safe_url(url: str) -> bool:
    """
    Checks if a URL is safe to request based on various security criteria
    """
    try:
        parsed = urllib.parse.urlparse(url)
        
        # Check if it's a local file URL (dangerous)
        if parsed.scheme in ['file']:
            return False
        
        # Check if it's a potentially dangerous protocol
        if parsed.scheme in ['javascript', 'data', 'vbscript']:
            return False
        
        # Check if hostname is an IP address that might be internal
        if parsed.hostname:
            try:
                ip = ipaddress.ip_address(parsed.hostname)
                # Block private/local IP ranges to prevent SSRF
                if ip.is_private or ip.is_loopback or ip.is_link_local:
                    return False
            except ValueError:
                # Not an IP address, continue with hostname checks
                pass
        
        return True
    except Exception:
        return False

def validate_domain(domain: str) -> bool:
    """
    Validates that a domain is safe for requests
    """
    # Block common internal/unsafe domains
    unsafe_domains = [
        'localhost',
        '127.0.0.1',
        'internal',
        'local',
        'docker',
        'kubernetes',
        'kubernetes.default.svc.cluster.local'
    ]
    
    # Check if domain is in unsafe list
    if domain.lower() in unsafe_domains:
        return False
    
    # Check if domain looks like an internal IP
    try:
        ip = ipaddress.ip_address(domain)
        if ip.is_private or ip.is_loopback:
            return False
    except ValueError:
        # Not an IP address, continue
        pass
    
    return True

def secure_request(url: str, method: str = 'GET', timeout: int = 30, **kwargs) -> Optional[requests.Response]:
    """
    Makes a secure HTTP request with safety validations
    """
    # Validate URL
    if not is_safe_url(url):
        print(f"Unsafe URL blocked: {url}")
        return None
    
    try:
        parsed = urllib.parse.urlparse(url)
        if not validate_domain(parsed.hostname or ""):
            print(f"Unsafe domain blocked: {parsed.hostname}")
            return None
        
        # Make the request with security limits
        response = requests.request(
            method=method,
            url=url,
            timeout=timeout,
            **kwargs
        )
        
        # Verify response is reasonable
        if len(response.content) > 50 * 1024 * 1024:  # 50MB limit
            print("Response too large (over 50MB), request blocked")
            return None
        
        return response
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error during request: {str(e)}")
        return None

def safe_html_parse(html_content: str, parser: str = 'lxml') -> Optional[BeautifulSoup]:
    """
    Safely parses HTML content with security considerations
    """
    try:
        # Check content size
        if len(html_content.encode('utf-8')) > 50 * 1024 * 1024:  # 50MB
            print("HTML content too large for safe parsing")
            return None
        
        # Parse with beautiful soup
        soup = BeautifulSoup(html_content, parser)
        
        # Remove potentially dangerous elements
        dangerous_tags = ['script', 'iframe', 'embed', 'object', 'link']
        for tag in dangerous_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        return soup
    
    except Exception as e:
        print(f"Error parsing HTML: {str(e)}")
        return None

def extract_links_safe(soup: BeautifulSoup, base_url: str = "") -> List[str]:
    """
    Safely extracts links from a parsed HTML document
    """
    links = []
    try:
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Resolve relative URLs
            absolute_url = urllib.parse.urljoin(base_url, href)
            if is_safe_url(absolute_url):
                links.append(absolute_url)
    except Exception as e:
        print(f"Error extracting links: {str(e)}")
    
    return links

def extract_images_safe(soup: BeautifulSoup, base_url: str = "") -> List[str]:
    """
    Safely extracts image URLs from a parsed HTML document
    """
    images = []
    try:
        for img in soup.find_all('img', src=True):
            src = img['src']
            # Resolve relative URLs
            absolute_url = urllib.parse.urljoin(base_url, src)
            if is_safe_url(absolute_url):
                images.append(absolute_url)
    except Exception as e:
        print(f"Error extracting images: {str(e)}")
    
    return images

def scrape_page_metadata(url: str) -> Optional[Dict[str, Any]]:
    """
    Safely scrapes metadata from a webpage
    """
    response = secure_request(url, timeout=30)
    if not response or response.status_code != 200:
        return None
    
    soup = safe_html_parse(response.text, 'lxml')
    if not soup:
        return None
    
    try:
        # Extract metadata
        metadata = {
            'url': url,
            'status_code': response.status_code,
            'headers': dict(list(response.headers.items())[:10]),  # Limit headers
            'title': '',
            'description': '',
            'keywords': '',
            'links_count': 0,
            'images_count': 0,
            'content_length': len(response.text)
        }
        
        # Get title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()[:500]  # Limit length
        
        # Get meta description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            metadata['description'] = desc_tag.get('content', '')[:1000]  # Limit length
        
        # Get meta keywords
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag:
            metadata['keywords'] = keywords_tag.get('content', '')[:1000]  # Limit length
        
        # Count links and images
        links = soup.find_all('a', href=True)
        metadata['links_count'] = len(links)
        
        images = soup.find_all('img')
        metadata['images_count'] = len(images)
        
        return metadata
    
    except Exception as e:
        print(f"Error extracting metadata: {str(e)}")
        return None

def fetch_and_parse_rss(url: str, max_items: int = 10) -> Optional[List[Dict[str, str]]]:
    """
    Safely fetches and parses an RSS feed
    """
    response = secure_request(url, timeout=30)
    if not response or response.status_code != 200:
        return None
    
    soup = safe_html_parse(response.text, 'xml')
    if not soup:
        # Try with html parser if xml fails
        soup = safe_html_parse(response.text, 'lxml')
        if not soup:
            return None
    
    try:
        items = []
        rss_items = soup.find_all('item')[:max_items]
        
        for item in rss_items:
            title = item.find('title')
            link = item.find('link')
            description = item.find('description')
            pub_date = item.find('pubDate')
            
            item_data = {
                'title': title.get_text().strip() if title else '',
                'link': link.get_text().strip() if link else '',
                'description': BeautifulSoup(description.get_text(), 'lxml').get_text() if description else '',
                'pub_date': pub_date.get_text().strip() if pub_date else ''
            }
            
            items.append(item_data)
        
        return items
    
    except Exception as e:
        print(f"Error parsing RSS feed: {str(e)}")
        return None

def download_file_safe(url: str, destination: str, max_size: int = 50 * 1024 * 1024) -> bool:  # 50MB default
    """
    Safely downloads a file with size limits
    """
    response = secure_request(url, timeout=60, stream=True)
    if not response or response.status_code != 200:
        return False
    
    try:
        # Check content length if available
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > max_size:
            print(f"File too large: {int(content_length)} bytes (max {max_size})")
            return False
        
        # Stream download with size check
        downloaded_size = 0
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                downloaded_size += len(chunk)
                if downloaded_size > max_size:
                    print(f"Download exceeded size limit: {downloaded_size} bytes")
                    return False
                f.write(chunk)
        
        return True
    
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return False

def main():
    """
    Example usage of the secure web interaction module
    """
    print("Secure Web Interaction Module for OpenClaw")
    print("Provides safe web requests and HTML parsing with security validations")
    
    # Example usage (commented out since no specific URL is provided)
    # url = "https://example.com"
    # metadata = scrape_page_metadata(url)
    # if metadata:
    #     print(f"Title: {metadata['title']}")
    #     print(f"Description: {metadata['description']}")

if __name__ == "__main__":
    main()