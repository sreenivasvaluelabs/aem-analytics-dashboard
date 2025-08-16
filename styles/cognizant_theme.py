import streamlit as st

def apply_cognizant_styling():
    """Apply Cognizant-inspired custom styling to the Streamlit app."""
    
    st.markdown("""
    <style>
    /* Import Cognizant-style fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(90deg, #0066CC 0%, #004499 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #004499 0%, #0066CC 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F5F7FA;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 6px;
        color: #666;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #0066CC 0%, #004499 100%);
        color: white !important;
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #F8FBFF 0%, #E6F2FF 100%);
        border: 1px solid #E0E7FF;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="metric-container"] > div > div > div[data-testid="metric-value"] {
        color: #0066CC;
        font-weight: 600;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div > div {
        background: #F8FBFF;
        border: 2px dashed #0066CC;
        border-radius: 8px;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(90deg, #D4EDDA 0%, #C3E6CB 100%);
        border: 1px solid #28A745;
        border-radius: 6px;
    }
    
    .stError {
        background: linear-gradient(90deg, #F8D7DA 0%, #F5C6CB 100%);
        border: 1px solid #DC3545;
        border-radius: 6px;
    }
    
    .stWarning {
        background: linear-gradient(90deg, #FFF3CD 0%, #FFEAA7 100%);
        border: 1px solid #FFC107;
        border-radius: 6px;
    }
    
    .stInfo {
        background: linear-gradient(90deg, #D1ECF1 0%, #B8E2E8 100%);
        border: 1px solid #17A2B8;
        border-radius: 6px;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #E0E7FF;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Selectbox and input styling */
    .stSelectbox > div > div {
        background: white;
        border: 1px solid #E0E7FF;
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input {
        border: 1px solid #E0E7FF;
        border-radius: 6px;
        padding: 0.5rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0066CC;
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #F8FBFF 0%, #F0F7FF 100%);
    }
    
    /* Custom card styling */
    .cognizant-card {
        background: white;
        border: 1px solid #E0E7FF;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Header gradient styling */
    .cognizant-header {
        background: linear-gradient(90deg, #0066CC 0%, #004499 100%);
        color: white;
        padding: 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0;
    }
    
    /* Animation for loading states */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .cognizant-header {
            padding: 1rem;
        }
        
        .cognizant-header h1 {
            font-size: 1.8rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_professional_header(title: str, subtitle: str = ""):
    """Create a professional header with Cognizant styling."""
    header_html = f"""
    <div class="cognizant-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 600;">{title}</h1>
        {f'<p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; color: #E6F2FF;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def create_info_card(content: str, card_type: str = "info"):
    """Create an information card with professional styling."""
    
    card_styles = {
        "info": "background: #F5F7FA; border-left: 4px solid #0066CC;",
        "success": "background: #F8F9FA; border-left: 4px solid #28A745;",
        "warning": "background: #FFF9E6; border-left: 4px solid #FFC107;",
        "error": "background: #FFF5F5; border-left: 4px solid #DC3545;"
    }
    
    style = card_styles.get(card_type, card_styles["info"])
    
    card_html = f"""
    <div style="{style} padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
        {content}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
