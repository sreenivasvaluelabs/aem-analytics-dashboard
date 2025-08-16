import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_processor import DataProcessor
from utils.visualizations import DashboardVisualizations
from styles.cognizant_theme import apply_cognizant_styling

# Configure page settings
st.set_page_config(
    page_title="Cognizant Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styling
apply_cognizant_styling()

# Initialize session state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'json_data' not in st.session_state:
    st.session_state.json_data = None
if 'last_upload_time' not in st.session_state:
    st.session_state.last_upload_time = None

# Initialize data processor
data_processor = DataProcessor()
dashboard_viz = DashboardVisualizations()

def main():
    # Header with Cognizant branding
    st.markdown("""
    <div style="background: linear-gradient(90deg, #0066CC 0%, #004499 100%); padding: 1.5rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 600;">
            📊 Cognizant Analytics Dashboard
        </h1>
        <p style="color: #E6F2FF; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            Professional Data Analytics for Demand/Supply/TAG Pipeline Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📁 Upload File", "📊 Dashboard", "📋 Data Table"])
    
    with tab1:
        upload_tab()
    
    with tab2:
        dashboard_tab()
    
    with tab3:
        data_table_tab()

def upload_tab():
    st.header("📁 File Upload & Data Processing")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background: #F5F7FA; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #0066CC;">
            <h4 style="margin-top: 0; color: #0066CC;">📋 Upload Instructions</h4>
            <ul style="margin-bottom: 0;">
                <li>Upload Excel files (.xlsx, .xls) containing your data</li>
                <li>Data will be automatically converted to JSON format</li>
                <li>Focus on <strong>Demand</strong>, <strong>Supply</strong>, and <strong>TAG Pipeline</strong> metrics</li>
                <li>All sheets in the Excel file will be processed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls'],
            help="Upload your Excel file containing Demand/Supply/TAG Pipeline data"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("Processing Excel file..."):
                    # Process the uploaded file
                    processed_data = data_processor.process_excel_file(uploaded_file)
                    
                    if processed_data:
                        st.session_state.uploaded_data = processed_data
                        st.session_state.json_data = json.dumps(processed_data, indent=2, default=str)
                        st.session_state.last_upload_time = datetime.now()
                        
                        st.success("✅ File uploaded and processed successfully!")
                        
                        # Show file details
                        st.markdown("### 📊 File Summary")
                        total_records = sum([len(sheet_data) for sheet_data in processed_data.values() if isinstance(sheet_data, list)])
                        st.metric("Total Records", total_records)
                        st.metric("Sheets Processed", len(processed_data))
                        
                        # Show sheet names
                        sheet_names = list(processed_data.keys())
                        st.write(f"**Sheets found:** {', '.join(sheet_names)}")
                        
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.error("Please ensure your Excel file is not corrupted and contains valid data.")
    
    with col2:
        if st.session_state.uploaded_data:
            st.markdown("### 📊 Current Data Status")
            st.success("Data loaded successfully")
            if st.session_state.last_upload_time:
                st.write(f"**Last updated:** {st.session_state.last_upload_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Show JSON preview
            if st.button("👁️ Preview JSON Data"):
                with st.expander("JSON Data Preview", expanded=True):
                    st.json(st.session_state.uploaded_data)
        else:
            st.info("No data uploaded yet")

def dashboard_tab():
    st.header("📊 Analytics Dashboard")
    
    if st.session_state.uploaded_data is None:
        st.warning("⚠️ Please upload an Excel file in the 'Upload File' tab to view the dashboard.")
        return
    
    # Auto-refresh functionality
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    with col2:
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
    
    if auto_refresh:
        st.rerun()
    
    # Dashboard metrics
    st.markdown("### 📈 Key Performance Indicators")
    
    try:
        # Generate visualizations based on uploaded data
        dashboard_viz.create_dashboard(st.session_state.uploaded_data)
        
    except Exception as e:
        st.error(f"❌ Error generating dashboard: {str(e)}")
        st.error("Please ensure your data contains the required columns for analysis.")

def data_table_tab():
    st.header("📋 Data Table & Analysis")
    
    if st.session_state.uploaded_data is None:
        st.warning("⚠️ Please upload an Excel file in the 'Upload File' tab to view the data table.")
        return
    
    # Sheet selector
    sheet_names = list(st.session_state.uploaded_data.keys())
    selected_sheet = st.selectbox("Select Sheet to View", sheet_names)
    
    if selected_sheet and selected_sheet in st.session_state.uploaded_data:
        sheet_data = st.session_state.uploaded_data[selected_sheet]
        
        if isinstance(sheet_data, list) and len(sheet_data) > 0:
            df = pd.DataFrame(sheet_data)
            
            # Search and filter controls
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                search_term = st.text_input("🔍 Search in data", placeholder="Enter search term...")
            
            with col2:
                # Column filter
                available_columns = df.columns.tolist()
                selected_columns = st.multiselect(
                    "📋 Select Columns", 
                    available_columns, 
                    default=available_columns[:10] if len(available_columns) > 10 else available_columns
                )
            
            with col3:
                # Row limit
                row_limit = st.number_input("📊 Rows to display", min_value=10, max_value=len(df), value=min(100, len(df)))
            
            # Apply filters
            filtered_df = df.copy()
            
            # Apply search filter
            if search_term:
                mask = filtered_df.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
                filtered_df = filtered_df[mask]
            
            # Apply column filter
            if selected_columns:
                filtered_df = filtered_df[selected_columns]
            
            # Apply row limit
            filtered_df = filtered_df.head(row_limit)
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Filtered Rows", len(filtered_df))
            with col3:
                st.metric("Total Columns", len(df.columns))
            with col4:
                st.metric("Selected Columns", len(selected_columns) if selected_columns else 0)
            
            # Display the filtered dataframe
            st.markdown("### 📊 Data Preview")
            if len(filtered_df) > 0:
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    hide_index=False
                )
                
                # Download options
                col1, col2 = st.columns(2)
                with col1:
                    csv_data = filtered_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download as CSV",
                        csv_data,
                        f"{selected_sheet}_filtered_data.csv",
                        "text/csv"
                    )
                
                with col2:
                    json_data = filtered_df.to_json(orient='records', indent=2)
                    st.download_button(
                        "💾 Download as JSON",
                        json_data,
                        f"{selected_sheet}_filtered_data.json",
                        "application/json"
                    )
            else:
                st.info("No data matches your search criteria.")
        
        else:
            st.error("Selected sheet contains no valid data.")

if __name__ == "__main__":
    main()
