# Cognizant Analytics Dashboard

## Overview

This is a Streamlit-based analytics dashboard designed for Cognizant's demand/supply/TAG pipeline analysis. The application provides a professional interface for uploading Excel files, processing data, and generating interactive visualizations with Cognizant's corporate branding and styling.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **Layout**: Wide layout with collapsible sidebar and tabbed interface
- **Styling**: Custom CSS implementation with Cognizant brand colors and typography
- **Components**: Three main tabs for file upload, dashboard visualization, and data table view

### Data Processing Layer
- **File Handling**: Excel file processing using pandas and openpyxl
- **Data Transformation**: Conversion from Excel sheets to JSON-compatible dictionary format
- **Data Cleaning**: Automated dataframe cleaning and preparation utilities
- **Multi-sheet Support**: Processes all sheets within uploaded Excel files

### Visualization Engine
- **Charting Library**: Plotly Express and Plotly Graph Objects for interactive visualizations
- **Dashboard Components**: KPI metrics, charts, and data tables
- **Color Scheme**: Consistent Cognizant brand color palette across all visualizations
- **Responsive Design**: Adaptive layouts for different screen sizes

### Session Management
- **State Persistence**: Streamlit session state for maintaining uploaded data between interactions
- **File Tracking**: Upload timestamp tracking and data caching
- **Memory Management**: Efficient handling of large Excel files and datasets

### Styling System
- **Theme Implementation**: Centralized styling module with Cognizant corporate identity
- **Custom Components**: Branded buttons, tabs, and layout elements
- **Typography**: Inter font family integration for professional appearance
- **Responsive Elements**: Hover effects and smooth transitions

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file reading and processing
- **plotly**: Interactive visualization creation

### Styling and Fonts
- **Google Fonts**: Inter font family for typography
- **CSS**: Custom styling implementation

### File Processing
- **json**: Data serialization and storage
- **datetime**: Timestamp management
- **os**: File system operations

### Data Visualization
- **numpy**: Numerical computations for chart data
- **plotly.express**: High-level plotting interface
- **plotly.graph_objects**: Low-level plotting components
- **plotly.subplots**: Multi-panel visualization support