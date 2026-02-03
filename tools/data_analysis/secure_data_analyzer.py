#!/usr/bin/env python3
"""
Secure Data Analyzer for OpenClaw
Implements safe data analysis with security validations
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List
import tempfile

def validate_data_file(file_path: str, file_types: List[str] = ['.csv', '.xlsx', '.xls']) -> Dict[str, Any]:
    """
    Validates a data file for security before processing
    """
    result = {
        'is_valid': True,
        'errors': [],
        'size_mb': 0,
        'rows': 0,
        'columns': 0,
        'file_type': None
    }
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            result['is_valid'] = False
            result['errors'].append("File does not exist")
            return result
        
        # Check file size (limit to 100MB)
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        result['size_mb'] = round(size_mb, 2)
        
        if size_mb > 100:
            result['is_valid'] = False
            result['errors'].append(f"File too large: {size_mb:.2f}MB (max 100MB)")
        
        # Check file extension
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in file_types:
            result['is_valid'] = False
            result['errors'].append(f"Invalid file extension: {file_ext}. Valid: {', '.join(file_types)}")
        else:
            result['file_type'] = file_ext
        
    except Exception as e:
        result['is_valid'] = False
        result['errors'].append(f"Validation error: {str(e)}")
    
    return result

def read_csv_secure(file_path: str, max_rows: int = 50000) -> Optional[pd.DataFrame]:
    """
    Securely reads a CSV file with safety limits
    """
    validation_result = validate_data_file(file_path, ['.csv'])
    
    if not validation_result['is_valid']:
        print(f"CSV validation failed: {'; '.join(validation_result['errors'])}")
        return None
    
    try:
        # Read CSV with security limits
        df = pd.read_csv(
            file_path,
            nrows=max_rows,  # Limit rows to prevent memory exhaustion
            low_memory=False  # Prevent mixed type inference issues
        )
        
        # Additional security checks
        if len(df) > max_rows:
            print(f"CSV has {len(df)} rows, exceeding limit of {max_rows}")
            return df.head(max_rows)  # Return only the first max_rows
        
        return df
    
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return None

def read_excel_secure(file_path: str, max_rows: int = 50000, sheet_name: str = 0) -> Optional[pd.DataFrame]:
    """
    Securely reads an Excel file with safety limits
    """
    validation_result = validate_data_file(file_path, ['.xlsx', '.xls'])
    
    if not validation_result['is_valid']:
        print(f"Excel validation failed: {'; '.join(validation_result['errors'])}")
        return None
    
    try:
        # Read Excel with security limits
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            nrows=max_rows,  # Limit rows to prevent memory exhaustion
            engine=None  # Let pandas auto-detect
        )
        
        # Additional security checks
        if len(df) > max_rows:
            print(f"Excel sheet has {len(df)} rows, exceeding limit of {max_rows}")
            return df.head(max_rows)  # Return only the first max_rows
        
        return df
    
    except Exception as e:
        print(f"Error reading Excel: {str(e)}")
        return None

def analyze_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs basic analysis on a DataFrame
    """
    if df.empty:
        return {"error": "DataFrame is empty"}
    
    analysis = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
        "numeric_summary": {},
        "categorical_summary": {}
    }
    
    # Get numeric columns for statistical summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()
    
    # Get categorical columns for value counts (first few)
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols[:5]:  # Only first 5 categorical columns
        analysis["categorical_summary"][col] = df[col].value_counts().head(10).to_dict()
    
    return analysis

def safe_data_operations(df: pd.DataFrame, operation: str, **kwargs) -> Optional[pd.DataFrame]:
    """
    Performs safe data operations on a DataFrame
    """
    try:
        if operation == "filter":
            # Safe filtering operation
            column = kwargs.get('column')
            condition = kwargs.get('condition')  # 'gt', 'lt', 'eq', 'contains', etc.
            value = kwargs.get('value')
            
            if not column or condition is None or value is None:
                print("Missing required parameters for filter operation")
                return None
            
            if condition == 'gt':
                return df[df[column] > value]
            elif condition == 'lt':
                return df[df[column] < value]
            elif condition == 'eq':
                return df[df[column] == value]
            elif condition == 'contains':
                if df[column].dtype == 'object':
                    return df[df[column].astype(str).str.contains(str(value), na=False)]
                else:
                    print("Contains operation only works on text columns")
                    return None
            else:
                print(f"Unsupported condition: {condition}")
                return None
        
        elif operation == "sort":
            column = kwargs.get('column')
            ascending = kwargs.get('ascending', True)
            
            if not column:
                print("Missing required column for sort operation")
                return None
            
            return df.sort_values(by=column, ascending=ascending)
        
        elif operation == "groupby":
            by_column = kwargs.get('by')
            agg_func = kwargs.get('agg', 'count')
            
            if not by_column:
                print("Missing required 'by' column for groupby operation")
                return None
            
            return df.groupby(by_column).agg(agg_func)
        
        else:
            print(f"Unsupported operation: {operation}")
            return None
    
    except Exception as e:
        print(f"Error performing operation '{operation}': {str(e)}")
        return None

def export_dataframe_secure(df: pd.DataFrame, output_path: str, max_rows: int = 100000) -> bool:
    """
    Securely exports a DataFrame to a file with limits
    """
    try:
        # Check if DataFrame is too large
        if len(df) > max_rows:
            print(f"DataFrame has {len(df)} rows, exceeding export limit of {max_rows}. Truncating...")
            df = df.head(max_rows)
        
        file_ext = Path(output_path).suffix.lower()
        
        if file_ext == '.csv':
            df.to_csv(output_path, index=False)
        elif file_ext in ['.xlsx', '.xls']:
            df.to_excel(output_path, index=False)
        else:
            print(f"Unsupported export format: {file_ext}")
            return False
        
        return True
    
    except Exception as e:
        print(f"Error exporting DataFrame: {str(e)}")
        return False

def main():
    """
    Example usage of the secure data analyzer
    """
    print("Secure Data Analyzer for OpenClaw")
    print("Validates and analyzes data files with security measures")
    
    # Example usage (commented out since no file is provided)
    # file_path = "example.csv"
    # df = read_csv_secure(file_path)
    # if df is not None:
    #     analysis = analyze_dataframe(df)
    #     print(f"Data analysis: {analysis}")

if __name__ == "__main__":
    main()