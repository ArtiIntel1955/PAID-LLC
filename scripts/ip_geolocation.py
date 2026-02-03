#!/usr/bin/env python3
"""
IP Geolocation Tool for OpenClaw
Provides location information for IP addresses using free services
"""

import sys
import json
import requests
from typing import Dict, Optional


def get_ip_info(ip_address: str = None) -> Dict:
    """
    Get geolocation information for an IP address
    If no IP is provided, gets information for the current IP
    """
    try:
        if ip_address:
            # Validate IP format
            import socket
            try:
                socket.inet_aton(ip_address)
            except socket.error:
                return {'error': f'Invalid IP address: {ip_address}'}
            
            url = f"http://ip-api.com/json/{ip_address}"
        else:
            # If no IP provided, get current IP info
            url = "http://ip-api.com/json/"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'success':
            return {
                'ip': data.get('query', ip_address),
                'status': 'success',
                'country': data.get('country'),
                'countryCode': data.get('countryCode'),
                'region': data.get('regionName'),
                'regionCode': data.get('region'),
                'city': data.get('city'),
                'zip': data.get('zip'),
                'lat': data.get('lat'),
                'lon': data.get('lon'),
                'timezone': data.get('timezone'),
                'isp': data.get('isp'),
                'org': data.get('org'),
                'as': data.get('as'),
                'asname': data.get('asname'),
                'reverse': data.get('reverse'),  # Reverse DNS
                'mobile': data.get('mobile'),  # Mobile carrier
                'proxy': data.get('proxy'),    # Proxy detection
                'hosting': data.get('hosting') # Hosting provider
            }
        else:
            return {
                'ip': ip_address,
                'status': 'error',
                'message': data.get('message', 'Unknown error')
            }
    
    except requests.exceptions.RequestException as e:
        return {'error': f'Request error: {str(e)}'}
    except Exception as e:
        return {'error': f'Error getting IP info: {str(e)}'}


def get_ip_via_ipapi_co(ip_address: str = None) -> Dict:
    """
    Alternative IP geolocation using ipapi.co (free tier)
    """
    try:
        if ip_address:
            url = f"https://ipapi.co/{ip_address}/json/"
        else:
            url = "https://ipapi.co/json/"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'error' not in data:
            return {
                'ip': data.get('ip', ip_address),
                'status': 'success',
                'country': data.get('country_name'),
                'countryCode': data.get('country_code'),
                'region': data.get('region'),
                'regionCode': data.get('region_code'),
                'city': data.get('city'),
                'postal_code': data.get('postal_code'),
                'lat': data.get('latitude'),
                'lon': data.get('longitude'),
                'timezone': data.get('timezone'),
                'currency': data.get('currency'),
                'asn': data.get('asn'),
                'org': data.get('org')
            }
        else:
            return {
                'ip': ip_address,
                'status': 'error',
                'message': data.get('reason', 'Unknown error')
            }
    
    except requests.exceptions.RequestException as e:
        return {'error': f'Request error: {str(e)}'}
    except Exception as e:
        return {'error': f'Error getting IP info from ipapi.co: {str(e)}'}


def get_ip_via_ipinfo(ip_address: str = None) -> Dict:
    """
    Alternative IP geolocation using ipinfo.io (free tier)
    """
    try:
        if ip_address:
            url = f"https://ipinfo.io/{ip_address}/json"
        else:
            url = "https://ipinfo.io/json"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'error' not in data:
            loc = data.get('loc', '').split(',')
            lat = float(loc[0]) if len(loc) > 0 and loc[0] else None
            lon = float(loc[1]) if len(loc) > 1 and loc[1] else None
            
            return {
                'ip': data.get('ip'),
                'status': 'success',
                'hostname': data.get('hostname'),
                'city': data.get('city'),
                'region': data.get('region'),
                'country': data.get('country'),
                'location': data.get('loc'),  # "lat,lon" string
                'lat': lat,
                'lon': lon,
                'org': data.get('org'),
                'postal': data.get('postal'),
                'timezone': data.get('timezone'),
                'asn': data.get('org', '').split()[0] if data.get('org') else None  # ASN from org field
            }
        else:
            return {
                'ip': ip_address,
                'status': 'error',
                'message': data.get('error', {}).get('message', 'Unknown error')
            }
    
    except requests.exceptions.RequestException as e:
        return {'error': f'Request error: {str(e)}'}
    except Exception as e:
        return {'error': f'Error getting IP info from ipinfo.io: {str(e)}'}


def get_my_public_ip() -> str:
    """
    Get the current public IP address
    """
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except:
        # Fallback service
        try:
            response = requests.get("https://ident.me", timeout=10)
            response.raise_for_status()
            return response.text.strip()
        except:
            # Another fallback
            try:
                response = requests.get("https://icanhazip.com", timeout=10)
                response.raise_for_status()
                return response.text.strip()
            except:
                return None


def enhanced_ip_lookup(ip_address: str = None) -> Dict:
    """
    Enhanced IP lookup using multiple services for reliability
    """
    if not ip_address:
        ip_address = get_my_public_ip()
        if not ip_address:
            return {'error': 'Could not determine IP address'}
    
    # Try primary service first
    result = get_ip_info(ip_address)
    
    # If primary fails or is incomplete, try alternatives
    if result.get('status') != 'success' or ('error' in result):
        # Try ipapi.co as backup
        backup_result = get_ip_via_ipapi_co(ip_address)
        if backup_result.get('status') == 'success':
            return backup_result
        
        # Try ipinfo.io as final backup
        final_result = get_ip_via_ipinfo(ip_address)
        if final_result.get('status') == 'success':
            return final_result
        
        # If all services fail, return the original error
        return result
    
    # Add additional information if available
    result['additional_services'] = {}
    
    # Try to get additional data from other services
    backup_result = get_ip_via_ipinfo(ip_address)
    if backup_result.get('status') == 'success':
        result['additional_services']['ipinfo'] = {
            'hostname': backup_result.get('hostname'),
            'org': backup_result.get('org'),
            'postal': backup_result.get('postal')
        }
    
    return result


def main():
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
        if ip_address.lower() == 'myip' or ip_address.lower() == 'current':
            result = enhanced_ip_lookup()
        else:
            result = enhanced_ip_lookup(ip_address)
    else:
        # Get info for current IP
        result = enhanced_ip_lookup()
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()