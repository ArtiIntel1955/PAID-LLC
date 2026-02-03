#!/usr/bin/env python3
"""
Secure PDF Reader for OpenClaw
Implements safe PDF processing with security validations
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import pdfplumber
import psutil  # For system monitoring during processing

def validate_pdf_file(file_path: str) -> Dict[str, Any]:
    """
    Validates a PDF file for security before processing
    """
    result = {
        'is_valid': True,
        'errors': [],
        'size_mb': 0,
        'page_count': 0
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
        if not file_path.lower().endswith('.pdf'):
            result['is_valid'] = False
            result['errors'].append("File is not a PDF")
        
        # Attempt to open PDF to check if it's a valid PDF
        try:
            with pdfplumber.open(file_path, pages=[1]) as pdf:
                result['page_count'] = len(pdf.pages)
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Invalid PDF format: {str(e)}")
        
        # Check system resources before processing large files
        memory_percent = psutil.virtual_memory().percent
        if memory_percent > 80:
            result['is_valid'] = False
            result['errors'].append(f"System memory usage too high ({memory_percent}%)")
        
    except Exception as e:
        result['is_valid'] = False
        result['errors'].append(f"Validation error: {str(e)}")
    
    return result

def extract_text_from_pdf_secure(file_path: str, max_pages: int = 20) -> Optional[str]:
    """
    Securely extracts text from a PDF with safety limits
    """
    # Validate the file first
    validation_result = validate_pdf_file(file_path)
    
    if not validation_result['is_valid']:
        print(f"PDF validation failed: {'; '.join(validation_result['errors'])}")
        return None
    
    if validation_result['page_count'] > max_pages:
        print(f"PDF has {validation_result['page_count']} pages, exceeding limit of {max_pages}")
        return None
    
    try:
        # Extract text with security limits
        extracted_text = ""
        with pdfplumber.open(file_path, pages=list(range(1, min(max_pages + 1, validation_result['page_count'] + 1)))) as pdf:
            for page_num, page in enumerate(pdf.pages):
                if page_num >= max_pages:
                    break
                
                text = page.extract_text()
                if text:
                    extracted_text += f"\n--- Page {page_num + 1} ---\n{text}\n"
        
        return extracted_text.strip()
    
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_tables_from_pdf_secure(file_path: str, max_pages: int = 10) -> Optional[list]:
    """
    Securely extracts tables from a PDF with safety limits
    """
    # Validate the file first
    validation_result = validate_pdf_file(file_path)
    
    if not validation_result['is_valid']:
        print(f"PDF validation failed: {'; '.join(validation_result['errors'])}")
        return None
    
    if validation_result['page_count'] > max_pages:
        print(f"PDF has {validation_result['page_count']} pages, exceeding limit of {max_pages}")
        return None
    
    try:
        tables_data = []
        with pdfplumber.open(file_path, pages=list(range(1, min(max_pages + 1, validation_result['page_count'] + 1)))) as pdf:
            for page_num, page in enumerate(pdf.pages):
                if page_num >= max_pages:
                    break
                
                tables = page.extract_tables()
                if tables:
                    for table_idx, table in enumerate(tables):
                        tables_data.append({
                            'page': page_num + 1,
                            'table_index': table_idx + 1,
                            'data': table
                        })
        
        return tables_data
    
    except Exception as e:
        print(f"Error extracting tables from PDF: {str(e)}")
        return None

def main():
    """
    Example usage of the secure PDF reader
    """
    print("Secure PDF Reader for OpenClaw")
    print("Validates and extracts content from PDFs with security measures")
    
    # Example usage (commented out since no file is provided)
    # file_path = "example.pdf"
    # text_content = extract_text_from_pdf_secure(file_path)
    # if text_content:
    #     print(f"Extracted {len(text_content)} characters from PDF")

if __name__ == "__main__":
    main()