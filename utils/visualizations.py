import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, Any, List

class DashboardVisualizations:
    """Handles creation of dashboard visualizations."""
    
    def __init__(self):
        self.cognizant_colors = {
            'primary': '#0066CC',
            'secondary': '#004499',
            'accent': '#00A0E6',
            'success': '#28A745',
            'warning': '#FFC107',
            'danger': '#DC3545',
            'light': '#F5F7FA',
            'dark': '#333333'
        }
        
        self.color_palette = [
            '#0066CC', '#00A0E6', '#004499', '#28A745', 
            '#FFC107', '#DC3545', '#6C757D', '#17A2B8'
        ]
    
    def create_dashboard(self, data: Dict[str, Any]):
        """
        Create comprehensive dashboard with multiple visualizations.
        
        Args:
            data: Dictionary containing processed data from all sheets
        """
        try:
            # Get the first sheet with data
            main_sheet = self.get_main_data_sheet(data)
            
            if main_sheet is None:
                st.error("No valid data found for dashboard creation.")
                return
            
            df = pd.DataFrame(data[main_sheet])
            
            if df.empty:
                st.error("Selected data sheet is empty.")
                return
            
            # Create KPI metrics
            self.create_kpi_metrics(df)
            
            # Create visualizations in columns
            col1, col2 = st.columns(2)
            
            with col1:
                self.create_trend_analysis(df)
                self.create_category_distribution(df)
            
            with col2:
                self.create_comparison_chart(df)
                self.create_pipeline_status(df)
            
            # Create full-width charts
            self.create_time_series_analysis(df)
            self.create_correlation_matrix(df)
            
        except Exception as e:
            st.error(f"Error creating dashboard: {str(e)}")
    
    def get_main_data_sheet(self, data: Dict[str, Any]) -> str:
        """
        Identify the main data sheet to use for dashboard.
        
        Args:
            data: Dictionary containing all sheet data
            
        Returns:
            Name of the main data sheet
        """
        # Priority order for sheet selection
        priority_sheets = ['sheet1', 'data', 'main', 'dashboard', 'summary']
        
        # First, try priority sheets
        for sheet_name in priority_sheets:
            for actual_sheet in data.keys():
                if sheet_name in actual_sheet.lower():
                    return actual_sheet
        
        # Otherwise, return the first sheet with data
        for sheet_name, sheet_data in data.items():
            if isinstance(sheet_data, list) and len(sheet_data) > 0:
                return sheet_name
        
        return None
    
    def create_kpi_metrics(self, df: pd.DataFrame):
        """Create KPI metrics row."""
        st.markdown("### 📊 Key Performance Indicators")
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) >= 4:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_records = len(df)
                st.metric("Total Records", f"{total_records:,}")
            
            with col2:
                if numeric_cols:
                    avg_value = df[numeric_cols[0]].mean()
                    st.metric(f"Avg {numeric_cols[0]}", f"{avg_value:.2f}")
                else:
                    st.metric("Data Quality", "100%")
            
            with col3:
                if len(numeric_cols) > 1:
                    max_value = df[numeric_cols[1]].max()
                    st.metric(f"Max {numeric_cols[1]}", f"{max_value:.2f}")
                else:
                    st.metric("Columns", len(df.columns))
            
            with col4:
                if len(numeric_cols) > 2:
                    sum_value = df[numeric_cols[2]].sum()
                    st.metric(f"Total {numeric_cols[2]}", f"{sum_value:.2f}")
                else:
                    st.metric("Coverage", "Active")
        
        else:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", f"{len(df):,}")
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Data Quality", "Ready")
            with col4:
                st.metric("Status", "Active")
    
    def create_trend_analysis(self, df: pd.DataFrame):
        """Create trend analysis chart."""
        st.markdown("#### 📈 Trend Analysis")
        
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_cols:
                # Use the first numeric column for trend analysis
                col_name = numeric_cols[0]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(len(df))),
                    y=df[col_name],
                    mode='lines+markers',
                    name=col_name,
                    line=dict(color=self.cognizant_colors['primary'], width=2),
                    marker=dict(size=6, color=self.cognizant_colors['accent'])
                ))
                
                fig.update_layout(
                    title=f"Trend Analysis - {col_name}",
                    xaxis_title="Record Index",
                    yaxis_title=col_name,
                    showlegend=True,
                    height=300,
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric data available for trend analysis.")
                
        except Exception as e:
            st.error(f"Error creating trend analysis: {str(e)}")
    
    def create_category_distribution(self, df: pd.DataFrame):
        """Create category distribution pie chart."""
        st.markdown("#### 🥧 Category Distribution")
        
        try:
            categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
            
            if categorical_cols:
                # Use the first categorical column
                col_name = categorical_cols[0]
                value_counts = df[col_name].value_counts().head(10)  # Top 10 categories
                
                fig = go.Figure(data=[go.Pie(
                    labels=value_counts.index,
                    values=value_counts.values,
                    hole=0.4,
                    marker_colors=self.color_palette
                )])
                
                fig.update_layout(
                    title=f"Distribution - {col_name}",
                    showlegend=True,
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No categorical data available for distribution analysis.")
                
        except Exception as e:
            st.error(f"Error creating category distribution: {str(e)}")
    
    def create_comparison_chart(self, df: pd.DataFrame):
        """Create comparison bar chart."""
        st.markdown("#### 📊 Comparison Analysis")
        
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
            
            if numeric_cols and categorical_cols:
                # Group by first categorical column and aggregate first numeric column
                group_col = categorical_cols[0]
                value_col = numeric_cols[0]
                
                grouped_data = df.groupby(group_col)[value_col].sum().sort_values(ascending=False).head(10)
                
                fig = go.Figure([go.Bar(
                    x=grouped_data.index,
                    y=grouped_data.values,
                    marker_color=self.cognizant_colors['primary'],
                    name=f"{value_col} by {group_col}"
                )])
                
                fig.update_layout(
                    title=f"{value_col} by {group_col}",
                    xaxis_title=group_col,
                    yaxis_title=value_col,
                    height=300,
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Insufficient data for comparison analysis.")
                
        except Exception as e:
            st.error(f"Error creating comparison chart: {str(e)}")
    
    def create_pipeline_status(self, df: pd.DataFrame):
        """Create pipeline status visualization."""
        st.markdown("#### 🔄 Pipeline Status")
        
        try:
            # Look for columns that might indicate pipeline stages
            pipeline_keywords = ['status', 'stage', 'phase', 'state', 'pipeline']
            pipeline_col = None
            
            for col in df.columns:
                if any(keyword in col.lower() for keyword in pipeline_keywords):
                    pipeline_col = col
                    break
            
            if pipeline_col:
                status_counts = df[pipeline_col].value_counts()
                
                fig = go.Figure([go.Bar(
                    x=status_counts.values,
                    y=status_counts.index,
                    orientation='h',
                    marker_color=self.color_palette[:len(status_counts)],
                    name="Pipeline Status"
                )])
                
                fig.update_layout(
                    title=f"Pipeline Status - {pipeline_col}",
                    xaxis_title="Count",
                    yaxis_title="Status",
                    height=300,
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Create a generic status chart based on data availability
                self.create_generic_status_chart(df)
                
        except Exception as e:
            st.error(f"Error creating pipeline status: {str(e)}")
    
    def create_generic_status_chart(self, df: pd.DataFrame):
        """Create a generic status chart when no pipeline column is found."""
        try:
            # Use the first categorical column
            categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
            
            if categorical_cols:
                col_name = categorical_cols[0]
                value_counts = df[col_name].value_counts().head(5)
                
                fig = go.Figure([go.Bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    marker_color=self.cognizant_colors['accent'],
                    name=f"Status - {col_name}"
                )])
                
                fig.update_layout(
                    title=f"Status Overview - {col_name}",
                    xaxis_title=col_name,
                    yaxis_title="Count",
                    height=300,
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No suitable data for pipeline status visualization.")
                
        except Exception as e:
            st.error(f"Error creating generic status chart: {str(e)}")
    
    def create_time_series_analysis(self, df: pd.DataFrame):
        """Create time series analysis if date columns exist."""
        st.markdown("#### ⏰ Time Series Analysis")
        
        try:
            # Look for date columns
            date_cols = []
            for col in df.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    date_cols.append(col)
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if date_cols and numeric_cols:
                date_col = date_cols[0]
                value_col = numeric_cols[0]
                
                # Try to convert to datetime
                try:
                    df[date_col] = pd.to_datetime(df[date_col])
                    df_sorted = df.sort_values(date_col)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df_sorted[date_col],
                        y=df_sorted[value_col],
                        mode='lines+markers',
                        name=f"{value_col} over time",
                        line=dict(color=self.cognizant_colors['primary'], width=2)
                    ))
                    
                    fig.update_layout(
                        title=f"Time Series - {value_col} over {date_col}",
                        xaxis_title=date_col,
                        yaxis_title=value_col,
                        height=400,
                        plot_bgcolor='white',
                        paper_bgcolor='white'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except:
                    st.info("Date column format not suitable for time series analysis.")
            else:
                st.info("No suitable date/time columns found for time series analysis.")
                
        except Exception as e:
            st.error(f"Error creating time series analysis: {str(e)}")
    
    def create_correlation_matrix(self, df: pd.DataFrame):
        """Create correlation matrix for numeric columns."""
        st.markdown("#### 🔗 Correlation Matrix")
        
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmid=0,
                    text=corr_matrix.round(2).values,
                    texttemplate='%{text}',
                    textfont={'size': 10},
                    hoverongaps=False
                ))
                
                fig.update_layout(
                    title="Correlation Matrix - Numeric Variables",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 numeric columns for correlation analysis.")
                
        except Exception as e:
            st.error(f"Error creating correlation matrix: {str(e)}")
