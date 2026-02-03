#!/usr/bin/env python3
"""
Simple test script to verify that all installed tools are working properly
"""

def test_pandas_numpy():
    """Test pandas and numpy installation"""
    try:
        import pandas as pd
        import numpy as np
        
        # Simple test with both libraries
        arr = np.array([1, 2, 3, 4, 5])
        df = pd.DataFrame({'numbers': arr, 'squares': arr**2})
        
        print("SUCCESS: Pandas and NumPy working correctly")
        print(f"Sample DataFrame:\n{df.head()}")
        return True
    except ImportError as e:
        print(f"ERROR: Pandas/NumPy test failed: {e}")
        return False

def test_pillow():
    """Test Pillow installation"""
    try:
        from PIL import Image
        import io
        
        # Create a simple test image in memory
        img = Image.new('RGB', (10, 10), color='red')
        
        # Verify we can perform basic operations
        width, height = img.size
        mode = img.mode
        
        print("SUCCESS: Pillow working correctly")
        print(f"Test image: {width}x{height}, mode: {mode}")
        return True
    except ImportError as e:
        print(f"ERROR: Pillow test failed: {e}")
        return False

def test_psutil():
    """Test psutil installation"""
    try:
        import psutil
        
        # Get basic system info
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        boot_time = psutil.boot_time()
        
        print("SUCCESS: Psutil working correctly")
        print(f"CPU: {cpu_percent}%, Memory: {memory_percent}%")
        return True
    except ImportError as e:
        print(f"ERROR: Psutil test failed: {e}")
        return False

def test_pdfplumber():
    """Test pdfplumber installation"""
    try:
        import pdfplumber
        import os
        
        # Check if we can import the module (we can't test with a real file without one)
        print("SUCCESS: Pdfplumber module imported successfully")
        print("Note: Requires a PDF file to test extraction functionality")
        return True
    except ImportError as e:
        print(f"ERROR: Pdfplumber test failed: {e}")
        return False

def main():
    print("Testing installed tools for OpenClaw...")
    print("="*50)
    
    results = []
    
    print("Testing core libraries:")
    results.append(test_pandas_numpy())
    results.append(test_pillow())
    results.append(test_psutil())
    results.append(test_pdfplumber())
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed! Tools are ready for use.")
        return True
    else:
        print("Some tests failed. Please check the installation.")
        return False

if __name__ == "__main__":
    main()