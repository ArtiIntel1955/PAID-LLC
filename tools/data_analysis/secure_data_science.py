#!/usr/bin/env python3
"""
Secure Data Science Tools for OpenClaw
Implements safe data science operations with security validations
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, Dict, Any, Tuple, Union
import tempfile
import os
from pathlib import Path

def validate_dataframe(df: pd.DataFrame, max_rows: int = 100000, max_cols: int = 100) -> bool:
    """
    Validates a DataFrame for safe processing
    """
    if not isinstance(df, pd.DataFrame):
        print("Input is not a pandas DataFrame")
        return False
    
    if df.shape[0] > max_rows:
        print(f"DataFrame has {df.shape[0]} rows, exceeding limit of {max_rows}")
        return False
    
    if df.shape[1] > max_cols:
        print(f"DataFrame has {df.shape[1]} columns, exceeding limit of {max_cols}")
        return False
    
    # Check for excessive memory usage
    memory_usage = df.memory_usage(deep=True).sum()
    if memory_usage > 500 * 1024 * 1024:  # 500MB limit
        print(f"DataFrame memory usage {memory_usage / (1024*1024):.2f}MB exceeds limit of 500MB")
        return False
    
    return True

def secure_descriptive_stats(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """
    Computes secure descriptive statistics
    """
    if not validate_dataframe(df):
        return None
    
    try:
        stats = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'numeric_summary': {},
            'categorical_summary': {}
        }
        
        # Get numeric columns for statistical summary
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 0:
            stats['numeric_summary'] = df[numeric_cols].describe().to_dict()
        
        # Get categorical columns for value counts (first few)
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        for col in categorical_cols[:5]:  # Only first 5 categorical columns
            unique_vals = df[col].nunique()
            if unique_vals <= 100:  # Only summarize columns with reasonable number of unique values
                stats['categorical_summary'][col] = df[col].value_counts().head(20).to_dict()
        
        return stats
    except Exception as e:
        print(f"Error computing descriptive statistics: {str(e)}")
        return None

def secure_correlation_analysis(df: pd.DataFrame, method: str = 'pearson') -> Optional[pd.DataFrame]:
    """
    Performs secure correlation analysis
    """
    if not validate_dataframe(df):
        return None
    
    try:
        # Only compute correlation for numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            print("Need at least 2 numeric columns for correlation analysis")
            return None
        
        # Limit to reasonable number of columns
        if numeric_df.shape[1] > 50:
            print(f"Too many numeric columns ({numeric_df.shape[1]}) for correlation analysis")
            return None
        
        correlation_matrix = numeric_df.corr(method=method)
        return correlation_matrix
    except Exception as e:
        print(f"Error in correlation analysis: {str(e)}")
        return None

def secure_regression_analysis(df: pd.DataFrame, target_col: str) -> Optional[Dict[str, Any]]:
    """
    Performs secure regression analysis
    """
    if not validate_dataframe(df):
        return None
    
    try:
        if target_col not in df.columns:
            print(f"Target column '{target_col}' not found in DataFrame")
            return None
        
        # Separate features and target
        X = df.select_dtypes(include=[np.number]).drop(columns=[target_col], errors='ignore')
        y = df[target_col]
        
        if X.shape[1] == 0:
            print("No numeric features found for regression")
            return None
        
        if not pd.api.types.is_numeric_dtype(y):
            print(f"Target column '{target_col}' is not numeric")
            return None
        
        # Remove rows with NaN in target
        mask = ~y.isna()
        X = X[mask]
        y = y[mask]
        
        if X.empty or y.empty:
            print("No valid data after cleaning")
            return None
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        
        # Feature importance (coefficients)
        feature_importance = dict(zip(X.columns, abs(model.coef_)))
        
        results = {
            'model_type': 'Linear Regression',
            'mse': mse,
            'feature_importance': feature_importance,
            'intercept': model.intercept_,
            'n_features': X.shape[1],
            'n_samples': X.shape[0]
        }
        
        return results
    except Exception as e:
        print(f"Error in regression analysis: {str(e)}")
        return None

def secure_classification_analysis(df: pd.DataFrame, target_col: str) -> Optional[Dict[str, Any]]:
    """
    Performs secure classification analysis
    """
    if not validate_dataframe(df):
        return None
    
    try:
        if target_col not in df.columns:
            print(f"Target column '{target_col}' not found in DataFrame")
            return None
        
        # Separate features and target
        feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if target_col in feature_cols:
            feature_cols.remove(target_col)
        
        X = df[feature_cols]
        y = df[target_col]
        
        if len(feature_cols) == 0:
            print("No numeric features found for classification")
            return None
        
        # Encode target if it's not numeric
        label_encoder = None
        if not pd.api.types.is_numeric_dtype(y):
            label_encoder = LabelEncoder()
            y_encoded = label_encoder.fit_transform(y)
        else:
            y_encoded = y
        
        # Remove rows with NaN
        mask = ~(X.isna().any(axis=1) | pd.isna(y_encoded))
        X_clean = X[mask]
        y_clean = y_encoded[mask]
        
        if X_clean.empty or y_clean.size == 0:
            print("No valid data after cleaning")
            return None
        
        # Check if we have enough classes
        unique_classes = len(np.unique(y_clean))
        if unique_classes < 2:
            print("Need at least 2 classes for classification")
            return None
        
        if unique_classes > 50:
            print("Too many classes for classification")
            return None
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = dict(zip(feature_cols, model.feature_importances_))
        
        results = {
            'model_type': 'Random Forest Classification',
            'accuracy': accuracy,
            'n_classes': unique_classes,
            'feature_importance': feature_importance,
            'n_features': len(feature_cols),
            'n_samples': X_clean.shape[0]
        }
        
        return results
    except Exception as e:
        print(f"Error in classification analysis: {str(e)}")
        return None

def secure_visualization(df: pd.DataFrame, plot_type: str, x_col: str, y_col: str = None, 
                        output_path: str = None, width: int = 800, height: int = 600) -> Optional[str]:
    """
    Creates secure visualizations
    """
    if not validate_dataframe(df):
        return None
    
    try:
        if x_col not in df.columns:
            print(f"Column '{x_col}' not found in DataFrame")
            return None
        
        if y_col and y_col not in df.columns:
            print(f"Column '{y_col}' not found in DataFrame")
            return None
        
        # Create temporary file if no output path provided
        if output_path is None:
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, f"plot_{plot_type}.html")
        
        # Prepare data
        if y_col:
            plot_data = df[[x_col, y_col]].dropna()
            x_data = plot_data[x_col]
            y_data = plot_data[y_col]
        else:
            plot_data = df[[x_col]].dropna()
            x_data = plot_data[x_col]
            y_data = None
        
        # Create plot based on type
        if plot_type == 'scatter':
            if y_data is None:
                print("Scatter plot requires both x and y columns")
                return None
            fig = px.scatter(x=x_data, y=y_data, title=f"Scatter Plot: {x_col} vs {y_col}")
        elif plot_type == 'line':
            if y_data is None:
                print("Line plot requires both x and y columns")
                return None
            fig = px.line(x=x_data, y=y_data, title=f"Line Plot: {x_col} vs {y_col}")
        elif plot_type == 'bar':
            if y_data is None:
                # Bar chart of value counts
                value_counts = x_data.value_counts().head(20)  # Limit to top 20
                fig = px.bar(x=value_counts.index, y=value_counts.values, 
                           title=f"Bar Chart: Value Counts of {x_col}")
            else:
                fig = px.bar(x=x_data, y=y_data, title=f"Bar Chart: {x_col} vs {y_col}")
        elif plot_type == 'histogram':
            fig = px.histogram(x=x_data, title=f"Histogram: Distribution of {x_col}")
        elif plot_type == 'box':
            if y_data is None:
                fig = px.box(y=x_data, title=f"Box Plot: Distribution of {x_col}")
            else:
                fig = px.box(x=x_data, y=y_data, title=f"Box Plot: {x_col} vs {y_col}")
        else:
            print(f"Unsupported plot type: {plot_type}")
            return None
        
        # Set dimensions
        fig.update_layout(width=width, height=height)
        
        # Save plot
        fig.write_html(output_path)
        
        return output_path
    except Exception as e:
        print(f"Error creating visualization: {str(e)}")
        return None

def secure_feature_engineering(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Performs secure feature engineering
    """
    if not validate_dataframe(df):
        return None
    
    try:
        engineered_df = df.copy()
        
        # Identify numeric columns for feature engineering
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Create polynomial features for numeric columns (only if reasonable number)
        if len(numeric_cols) <= 10:
            for col in numeric_cols:
                # Add squared term if it makes sense (not too large values)
                if df[col].max() < 1000 and df[col].min() > -1000:
                    engineered_df[f'{col}_squared'] = df[col] ** 2
        
        # Create interaction features for pairs of columns (limit to first few)
        if len(numeric_cols) >= 2:
            for i, col1 in enumerate(numeric_cols[:3]):  # Limit to first 3
                for j, col2 in enumerate(numeric_cols[i+1:4]):  # Limit to next 3
                    # Only create if not too computationally intensive
                    if df[col1].max() * df[col2].max() < 1e6:  # Avoid huge values
                        engineered_df[f'{col1}_{col2}_interaction'] = df[col1] * df[col2]
        
        # Identify datetime columns and create time-based features
        for col in df.columns:
            if df[col].dtype == 'object':  # Potential datetime string
                try:
                    # Try to convert to datetime
                    dt_series = pd.to_datetime(df[col], errors='coerce')
                    if not dt_series.isna().all():
                        # Create time-based features
                        engineered_df[f'{col}_year'] = dt_series.dt.year
                        engineered_df[f'{col}_month'] = dt_series.dt.month
                        engineered_df[f'{col}_day'] = dt_series.dt.day
                        engineered_df[f'{col}_weekday'] = dt_series.dt.weekday
                except:
                    continue  # Skip if not a datetime column
        
        # Ensure we don't exceed column limits
        if engineered_df.shape[1] > 100:
            print(f"Feature engineering resulted in {engineered_df.shape[1]} columns, exceeding limit")
            return df  # Return original dataframe
        
        return engineered_df
    except Exception as e:
        print(f"Error in feature engineering: {str(e)}")
        return df  # Return original dataframe on error

def secure_data_export(df: pd.DataFrame, output_path: str, format_type: str = 'csv', 
                      max_rows: int = 100000) -> bool:
    """
    Securely exports DataFrame to file
    """
    if not validate_dataframe(df, max_rows=max_rows):
        return False
    
    try:
        output_path = Path(output_path)
        
        if format_type.lower() == 'csv':
            df.to_csv(output_path, index=False)
        elif format_type.lower() == 'excel' or format_type.lower() == 'xlsx':
            df.to_excel(output_path, index=False)
        elif format_type.lower() == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif format_type.lower() == 'parquet':
            df.to_parquet(output_path, index=False)
        else:
            print(f"Unsupported export format: {format_type}")
            return False
        
        return True
    except Exception as e:
        print(f"Error exporting data: {str(e)}")
        return False

def main():
    """
    Example usage of the secure data science tools
    """
    print("Secure Data Science Tools for OpenClaw")
    print("Provides safe data science operations with security validations")
    
    # Example usage would require a DataFrame
    # df = pd.read_csv("example.csv")  # This would be provided by user
    # stats = secure_descriptive_stats(df)
    # print(f"Descriptive stats: {stats}")

if __name__ == "__main__":
    main()