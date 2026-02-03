#!/usr/bin/env python3
"""Test script for network security monitor functionality"""

import subprocess
import sys

def test_basic_functions():
    """Test basic functionality of the security monitor"""
    print("Testing Network Security Monitor...")
    
    # Test if we can import and initialize basic components
    try:
        import network_security_monitor
        print("[SUCCESS] Module imported successfully")
    except ImportError as e:
        print(f"[ERROR] Module import failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error importing module: {e}")
        return False
    
    # Test if we can create an instance
    try:
        monitor = network_security_monitor.NetworkSecurityMonitor()
        print("[SUCCESS] Monitor instance created successfully")
    except Exception as e:
        print(f"[ERROR] Failed to create monitor instance: {e}")
        return False
    
    # Test basic status reporting
    try:
        status = monitor.get_security_status()
        print(f"[SUCCESS] Status report generated, {len(status.get('toggles', {}))} security features detected")
        print(f"[SUCCESS] Risk score calculated: {status.get('overall_risk_score', 'N/A')}/100")
    except Exception as e:
        print(f"[ERROR] Failed to generate status report: {e}")
        return False
    
    # Test report generation
    try:
        report = monitor.generate_report()
        print("[SUCCESS] Security report generated successfully")
        print(f"   Report length: {len(report)} characters")
    except Exception as e:
        print(f"[ERROR] Failed to generate report: {e}")
        return False
    
    print("\n[SUCCESS] All basic tests passed!")
    print("The Network Security Monitor is ready for use.")
    print("\nTo start the interactive monitor, run:")
    print("  python network_security_monitor.py")
    print("\nThe system includes:")
    print("  - Real-time security monitoring")
    print("  - Toggle controls for all security features")
    print("  - Risk scoring and alerts")
    print("  - Comprehensive reporting")
    
    return True

if __name__ == "__main__":
    success = test_basic_functions()
    if not success:
        sys.exit(1)