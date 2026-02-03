#!/usr/bin/env python3
"""
Secure Image Processor for OpenClaw
Implements safe image processing with security validations
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from PIL import Image
import tempfile

def validate_image_file(file_path: str) -> Dict[str, Any]:
    """
    Validates an image file for security before processing
    """
    result = {
        'is_valid': True,
        'errors': [],
        'size_mb': 0,
        'dimensions': (0, 0),
        'format': None
    }
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            result['is_valid'] = False
            result['errors'].append("File does not exist")
            return result
        
        # Check file size (limit to 50MB)
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        result['size_mb'] = round(size_mb, 2)
        
        if size_mb > 50:
            result['is_valid'] = False
            result['errors'].append(f"File too large: {size_mb:.2f}MB (max 50MB)")
        
        # Check file extension
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in valid_extensions:
            result['is_valid'] = False
            result['errors'].append(f"Invalid file extension: {file_ext}. Valid: {', '.join(valid_extensions)}")
        
        # Attempt to open image to check if it's a valid image
        try:
            with Image.open(file_path) as img:
                result['dimensions'] = img.size
                result['format'] = img.format
                # Check dimensions (limit to 100MP to prevent decompression bombs)
                pixel_count = img.size[0] * img.size[1]
                if pixel_count > 100_000_000:  # 100 megapixels
                    result['is_valid'] = False
                    result['errors'].append(f"Image too large: {pixel_count:,} pixels (max 100,000,000)")
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Invalid image format: {str(e)}")
        
    except Exception as e:
        result['is_valid'] = False
        result['errors'].append(f"Validation error: {str(e)}")
    
    return result

def resize_image_secure(input_path: str, output_path: str, max_size: Tuple[int, int] = (1920, 1080)) -> bool:
    """
    Securely resizes an image with safety limits
    """
    # Validate the input file first
    validation_result = validate_image_file(input_path)
    
    if not validation_result['is_valid']:
        print(f"Image validation failed: {'; '.join(validation_result['errors'])}")
        return False
    
    try:
        with Image.open(input_path) as img:
            # Preserve EXIF data if it exists
            exif_data = img.info.get('exif')
            
            # Calculate new size preserving aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save the resized image
            if img.mode in ('RGBA', 'LA', 'P') and img.mode != 'RGB':
                # Convert to RGB if necessary to avoid transparency issues
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background to paste the image on
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                else:
                    img = img.convert('RGB')
            
            if exif_data:
                img.save(output_path, exif=exif_data)
            else:
                img.save(output_path)
        
        return True
    
    except Exception as e:
        print(f"Error resizing image: {str(e)}")
        return False

def get_image_info(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Gets information about an image file securely
    """
    validation_result = validate_image_file(file_path)
    
    if not validation_result['is_valid']:
        print(f"Image validation failed: {'; '.join(validation_result['errors'])}")
        return None
    
    try:
        with Image.open(file_path) as img:
            info = {
                'path': file_path,
                'size_mb': validation_result['size_mb'],
                'dimensions': validation_result['dimensions'],
                'format': validation_result['format'],
                'mode': img.mode,
                'width': img.width,
                'height': img.height
            }
            
            # Add additional info if available
            if hasattr(img, '_getexif') and img._getexif():
                exif = img._getexif()
                if exif:
                    info['exif'] = dict(list(exif.items())[:10])  # Limit EXIF data
            
            return info
    
    except Exception as e:
        print(f"Error getting image info: {str(e)}")
        return None

def crop_image_secure(input_path: str, output_path: str, box: Tuple[int, int, int, int]) -> bool:
    """
    Securely crops an image with bounds checking
    """
    validation_result = validate_image_file(input_path)
    
    if not validation_result['is_valid']:
        print(f"Image validation failed: {'; '.join(validation_result['errors'])}")
        return False
    
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            
            # Validate crop box coordinates
            left, top, right, bottom = box
            if left < 0 or top < 0 or right > width or bottom > height or left >= right or top >= bottom:
                print(f"Crop box coordinates invalid: {box} for image size {width}x{height}")
                return False
            
            # Perform the crop
            cropped_img = img.crop(box)
            
            # Save the cropped image
            cropped_img.save(output_path)
        
        return True
    
    except Exception as e:
        print(f"Error cropping image: {str(e)}")
        return False

def convert_image_format_secure(input_path: str, output_path: str, output_format: str = 'JPEG') -> bool:
    """
    Securely converts an image to a different format
    """
    validation_result = validate_image_file(input_path)
    
    if not validation_result['is_valid']:
        print(f"Image validation failed: {'; '.join(validation_result['errors'])}")
        return False
    
    try:
        with Image.open(input_path) as img:
            # Handle transparency for formats that don't support it
            if output_format.upper() in ['JPEG', 'JPG'] and img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background for JPEG conversion
                if img.mode == 'P':
                    img = img.convert('RGBA')
                
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA', 'P'):
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                else:
                    background.paste(img)
                img = background
            elif img.mode == 'P' and output_format.upper() not in ['PNG', 'TIFF']:
                # Convert palette mode to RGB for formats that don't support it
                img = img.convert('RGB')
            
            # Save in the requested format
            img.save(output_path, format=output_format)
        
        return True
    
    except Exception as e:
        print(f"Error converting image format: {str(e)}")
        return False

def main():
    """
    Example usage of the secure image processor
    """
    print("Secure Image Processor for OpenClaw")
    print("Validates and processes images with security measures")
    
    # Example usage (commented out since no file is provided)
    # file_path = "example.jpg"
    # info = get_image_info(file_path)
    # if info:
    #     print(f"Image info: {info}")

if __name__ == "__main__":
    main()