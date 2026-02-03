#!/usr/bin/env python3
"""
NASA API Integration for Scientific Data Processing
Provides access to astronomy, Earth observation, and space mission data
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional


class NasaAPI:
    """
    NASA API Integration Class
    Access to astronomy, Earth observation, and space mission data
    """
    
    def __init__(self, api_key: str = "DEMO_KEY"):
        """
        Initialize NASA API client
        api_key: NASA API key (get from https://api.nasa.gov/)
        """
        self.api_key = api_key
        self.base_url = "https://api.nasa.gov"
        
    def get_apod(self, date: Optional[str] = None) -> Dict:
        """
        Get Astronomy Picture of the Day
        date: Optional date in YYYY-MM-DD format (default: today)
        """
        endpoint = "/planetary/apod"
        params = {"api_key": self.api_key}
        if date:
            params["date"] = date
            
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_mars_photos(self, sol: int = 1000, camera: Optional[str] = None) -> Dict:
        """
        Get Mars rover photos from a specific Martian sol (day)
        sol: Martian sol (default: 1000)
        camera: Camera name (FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES)
        """
        endpoint = "/mars-photos/api/v1/rovers/curiosity/photos"
        params = {
            "sol": sol,
            "api_key": self.api_key
        }
        if camera:
            params["camera"] = camera
            
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_neo_feed(self, start_date: str, end_date: Optional[str] = None) -> Dict:
        """
        Get Near Earth Object feed
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format (default: start_date + 7 days)
        """
        endpoint = "/neo/rest/v1/feed"
        params = {
            "start_date": start_date,
            "api_key": self.api_key
        }
        if end_date:
            params["end_date"] = end_date
            
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_earth_imagery(self, lat: float, lon: float, dim: Optional[float] = None, 
                         date: Optional[str] = None, catalog: Optional[str] = None) -> Dict:
        """
        Get Earth imagery for a location
        lat: Latitude
        lon: Longitude
        dim: Dimension of image (0.025 for 25km, default: automatic)
        date: Date in YYYY-MM-DD format (default: latest)
        catalog: Catalog ID for specific image collection
        """
        endpoint = "/planetary/earth/imagery"
        params = {
            "lat": lat,
            "lon": lon,
            "api_key": self.api_key
        }
        if dim:
            params["dim"] = dim
        if date:
            params["date"] = date
        if catalog:
            params["catalog"] = catalog
            
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()


def get_astronomy_fact() -> str:
    """
    Get an interesting astronomy fact using NASA APIs
    """
    nasa = NasaAPI()
    
    try:
        # Get APOD for today
        apod = nasa.get_apod()
        
        title = apod.get('title', 'Astronomy Picture of the Day')
        explanation = apod.get('explanation', 'No explanation available.')
        
        if len(explanation) > 200:
            explanation = explanation[:200] + "..."
        
        return f"🔭 {title}\n\n{explanation}"
        
    except Exception as e:
        return f"Could not retrieve astronomy data: {str(e)}"


def get_mars_rover_images(sol: int = 1000) -> str:
    """
    Get recent Mars rover images
    """
    nasa = NasaAPI()
    
    try:
        photos = nasa.get_mars_photos(sol=sol)
        total_photos = photos.get('photos', [])
        
        if total_photos:
            # Get the first few images
            image_descriptions = []
            for photo in total_photos[:3]:  # First 3 photos
                img_url = photo.get('img_src', 'No image URL')
                earth_date = photo.get('earth_date', 'Unknown date')
                camera = photo.get('camera', {}).get('name', 'Unknown camera')
                
                image_descriptions.append(f"📸 {camera} - {earth_date}\n{img_url}")
            
            return f"rovers on Mars - Sol {sol}:\n\n" + "\n\n".join(image_descriptions)
        else:
            return f"No Mars rover images available for sol {sol}"
            
    except Exception as e:
        return f"Could not retrieve Mars rover images: {str(e)}"


def get_nearby_asteroids(start_date: str = None) -> str:
    """
    Get information about nearby asteroids
    """
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    
    nasa = NasaAPI()
    
    try:
        neo_data = nasa.get_neo_feed(start_date=start_date)
        
        near_earth_objects = neo_data.get('near_earth_objects', {})
        today_neos = near_earth_objects.get(start_date, [])
        
        if today_neos:
            asteroid_info = []
            for neo in today_neos[:3]:  # First 3 asteroids
                name = neo.get('name', 'Unknown')
                diameter_min = neo.get('estimated_diameter', {}).get('meters', {}).get('estimated_diameter_min', 0)
                diameter_max = neo.get('estimated_diameter', {}).get('meters', {}).get('estimated_diameter_max', 0)
                hazardous = "⚠️ HAZARDOUS" if neo.get('is_potentially_hazardous_asteroid', False) else "✅ SAFE"
                
                asteroid_info.append(f"☄️ {name}\n   Diameter: {diameter_min:.0f}-{diameter_max:.0f}m\n   Status: {hazardous}")
            
            return f"Asteroids approaching Earth on {start_date}:\n\n" + "\n\n".join(asteroid_info)
        else:
            return f"No nearby asteroids detected for {start_date}"
            
    except Exception as e:
        return f"Could not retrieve asteroid data: {str(e)}"


def main():
    """
    Main function to demonstrate NASA API capabilities
    """
    print("NASA API Integration Demo")
    print("=" * 40)
    
    # Get astronomy fact
    print("\n1. Astronomy Fact:")
    print(get_astronomy_fact())
    
    # Get Mars rover images
    print("\n2. Mars Rover Images:")
    print(get_mars_rover_images())
    
    # Get nearby asteroids
    print("\n3. Nearby Asteroids:")
    print(get_nearby_asteroids())


if __name__ == "__main__":
    main()