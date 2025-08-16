import pandas as pd
import json
import streamlit as st
from typing import Dict, Any, Optional
import openpyxl
from io import BytesIO

class DataProcessor:
    """Handles Excel file processing and data conversion operations."""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls']
    
    def process_excel_file(self, uploaded_file) -> Optional[Dict[str, Any]]:
        """
        Process uploaded Excel file and convert to JSON-compatible format.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary containing processed data from all sheets
        """
        try:
            # Read all sheets from Excel file
            excel_data = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl')
            
            processed_data = {}
            
            for sheet_name, df in excel_data.items():
                # Clean the dataframe
                df_cleaned = self.clean_dataframe(df)
                
                if not df_cleaned.empty:
                    # Convert to records format (list of dictionaries)
                    processed_data[sheet_name] = df_cleaned.to_dict('records')
                else:
                    processed_data[sheet_name] = []
            
            return processed_data
            
        except Exception as e:
            st.error(f"Error processing Excel file: {str(e)}")
            return None
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare dataframe for processing.
        
        Args:
            df: Raw pandas DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        try:
            # Remove completely empty rows and columns
            df_cleaned = df.dropna(how='all').dropna(axis=1, how='all')
            
            # Reset index
            df_cleaned = df_cleaned.reset_index(drop=True)
            
            # Convert column names to strings and clean them
            df_cleaned.columns = [str(col).strip() for col in df_cleaned.columns]
            
            # Replace NaN values with empty strings for better JSON compatibility
            df_cleaned = df_cleaned.fillna('')
            
            # Convert datetime columns to string format
            for col in df_cleaned.columns:
                if df_cleaned[col].dtype == 'datetime64[ns]':
                    df_cleaned[col] = df_cleaned[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                elif 'datetime' in str(df_cleaned[col].dtype):
                    df_cleaned[col] = df_cleaned[col].astype(str)
            
            return df_cleaned
            
        except Exception as e:
            st.error(f"Error cleaning dataframe: {str(e)}")
            return pd.DataFrame()
    
    def identify_key_columns(self, df: pd.DataFrame) -> Dict[str, list]:
        """
        Identify columns that might contain Demand, Supply, or TAG Pipeline data.
        
        Args:
            df: pandas DataFrame
            
        Returns:
            Dictionary with categorized column names
        """
        columns = df.columns.tolist()
        
        # Keywords to identify different data categories
        demand_keywords = ['demand', 'requirement', 'need', 'request', 'order']
        supply_keywords = ['supply', 'available', 'stock', 'inventory', 'resource']
        tag_keywords = ['tag', 'pipeline', 'stage', 'phase', 'status', 'progress']
        
        categorized_columns = {
            'demand': [],
            'supply': [],
            'tag_pipeline': [],
            'other': []
        }
        
        for col in columns:
            col_lower = col.lower()
            
            if any(keyword in col_lower for keyword in demand_keywords):
                categorized_columns['demand'].append(col)
            elif any(keyword in col_lower for keyword in supply_keywords):
                categorized_columns['supply'].append(col)
            elif any(keyword in col_lower for keyword in tag_keywords):
                categorized_columns['tag_pipeline'].append(col)
            else:
                categorized_columns['other'].append(col)
        
        return categorized_columns
    
    def get_numeric_columns(self, df: pd.DataFrame) -> list:
        """
        Identify numeric columns in the dataframe.
        
        Args:
            df: pandas DataFrame
            
        Returns:
            List of numeric column names
        """
        return df.select_dtypes(include=['number']).columns.tolist()
    
    def get_categorical_columns(self, df: pd.DataFrame) -> list:
        """
        Identify categorical columns in the dataframe.
        
        Args:
            df: pandas DataFrame
            
        Returns:
            List of categorical column names
        """
        return df.select_dtypes(include=['object', 'string']).columns.tolist()
    
    def calculate_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate summary statistics for the dataframe.
        
        Args:
            df: pandas DataFrame
            
        Returns:
            Dictionary containing summary statistics
        """
        try:
            numeric_cols = self.get_numeric_columns(df)
            categorical_cols = self.get_categorical_columns(df)
            
            summary = {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'numeric_columns': len(numeric_cols),
                'categorical_columns': len(categorical_cols),
                'missing_values': df.isnull().sum().to_dict(),
                'data_types': df.dtypes.astype(str).to_dict()
            }
            
            # Add numeric statistics
            if numeric_cols:
                summary['numeric_stats'] = df[numeric_cols].describe().to_dict()
            
            return summary
            
        except Exception as e:
            st.error(f"Error calculating summary statistics: {str(e)}")
            return {}
