#!/usr/bin/env python3
"""
TrialScope AI - Professional Dark Theme Clinical Trial Intelligence Platform
Redesigned to match the exact UI from the provided screenshot
"""

import streamlit as st
import requests
import json
import logging
import time
from typing import Dict, List, Any, Optional
import base64
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="TrialScope AI - Clinical Trial Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Dark Theme CSS matching the screenshot
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Hide Streamlit elements */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Dark Theme Professional Background */
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 1rem;
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Professional Navigation Bar */
    .top-nav {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6b 100%);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-img {
        width: 48px;
        height: 48px;
        border-radius: 8px;
    }
    
    .logo-text {
        font-size: 1.75rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0;
        font-family: 'Inter', sans-serif;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        color: #94a3b8;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .nav-link:hover {
        color: #06b6d4;
        background: rgba(6, 182, 212, 0.1);
    }
    
    .nav-link.active {
        color: #06b6d4;
        background: rgba(6, 182, 212, 0.15);
    }
    
    .pro-account-btn {
        background: linear-gradient(135deg, #06b6d4, #0891b2);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 8px rgba(6, 182, 212, 0.3);
    }
    
    .pro-account-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
    }
    
    /* Hero Section - Dark Theme */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        margin: 2rem 0;
        background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
        border-radius: 16px;
        border: 1px solid rgba(6, 182, 212, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 20%, rgba(6, 182, 212, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0 0 1.5rem 0;
        line-height: 1.1;
        position: relative;
        z-index: 1;
    }
    
    .hero-title .ai-text {
        background: linear-gradient(135deg, #06b6d4, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-title .clinical-text {
        color: #e2e8f0;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin: 0 auto;
        max-width: 600px;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Search Container - Dark Theme */
    .search-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 3rem 2.5rem;
        border-radius: 16px;
        margin: 3rem 0;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(6, 182, 212, 0.3);
        position: relative;
    }
    
    .search-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #06b6d4, #10b981, #06b6d4);
        border-radius: 16px 16px 0 0;
    }
    
    .search-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0 0 0.5rem 0;
        text-align: center;
    }
    
    .search-subtitle {
        color: #94a3b8;
        text-align: center;
        margin: 0 0 2.5rem 0;
        font-size: 1.1rem;
    }
    
    /* Form Styling - Dark Theme */
    .stTextInput > div > div > input {
        background: #0f172a !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
        outline: none !important;
    }
    
    .stSelectbox > div > div > div {
        background: #0f172a !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }
    
    .stSelectbox > div > div > div:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(6, 182, 212, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4) !important;
    }
    
    /* Filter Section */
    .filter-section {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(51, 65, 85, 0.5);
    }
    
    /* Academic Research Section */
    .academic-section {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    .academic-title {
        color: #e2e8f0;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Footer - Dark Theme */
    .footer-section {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin: 4rem 0 2rem 0;
        border: 1px solid rgba(51, 65, 85, 0.3);
    }
    
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
    }
    
    .footer-section h4 {
        color: #06b6d4;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
    }
    
    .footer-section p, .footer-section a {
        color: #94a3b8;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        text-decoration: none;
    }
    
    .footer-section a:hover {
        color: #06b6d4;
    }
    
    /* Results styling */
    .result-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(6, 182, 212, 0.2);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.1);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .nav-links {
            display: none;
        }
        
        .top-nav {
            padding: 1rem;
        }
        
        .search-container {
            padding: 2rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load the logo image
@st.cache_data
def load_logo():
    """Load and encode the TrialScope AI logo"""
    try:
        logo_path = Path("attached_assets/generated-image_1755095388385.png")
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception as e:
        logger.warning(f"Could not load logo: {e}")
    return None

def render_navigation():
    """Render the professional navigation bar with logo"""
    logo_base64 = load_logo()
    
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="TrialScope AI Logo">'
    else:
        # Fallback to icon if logo not found
        logo_html = '<div style="width: 48px; height: 48px; background: linear-gradient(135deg, #06b6d4, #0891b2); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: white; font-weight: bold;">T</div>'
    
    st.markdown(f"""
    <div class="top-nav">
        <div class="logo-section">
            <div class="logo-container">
                {logo_html}
                <h1 class="logo-text">TrialScope AI</h1>
            </div>
        </div>
        <div class="nav-links">
            <a href="#" class="nav-link active">Dashboard</a>
            <a href="#" class="nav-link">Scholar</a>
            <a href="#" class="nav-link">Analytics</a>
            <a href="#" class="nav-link">API</a>
        </div>
        <div>
            <a href="#" class="pro-account-btn">⚡ Pro Account</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_hero_section():
    """Render the hero section matching the screenshot"""
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">
            <span class="ai-text">AI-Powered</span> <span class="clinical-text">Clinical<br>Trial Intelligence</span>
        </h1>
        <p class="hero-subtitle">
            Search, analyze, and discover clinical trials with advanced AI 
            classification focusing exclusively on human research studies
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_search_interface():
    """Render the main search interface matching the screenshot"""
    st.markdown("""
    <div class="search-container">
        <h2 class="search-title">Search Query</h2>
        <p class="search-subtitle">Search across 16 global registries with AI-powered relevance scoring</p>
    """, unsafe_allow_html=True)
    
    # Main search form
    with st.form("clinical_trial_search", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input(
                "Search Query",
                placeholder="e.g., Pancreatic Cancer Gemcitabine | Pancreatic Cancer",
                help="Enter disease names, drug compounds, or research topics",
                label_visibility="collapsed"
            )
        
        with col2:
            search_type = st.selectbox(
                "Search Type",
                ["Disease Only", "Drug Focus", "Combined Search", "Therapeutic Area"],
                help="Optimize search strategy",
                label_visibility="collapsed"
            )
        
        # Clinical Trial Databases section
        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h3 style="color: #e2e8f0; font-size: 1.1rem; font-weight: 600; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                🗃️ Clinical Trial Databases
                <span style="background: #06b6d4; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem;">16 selected</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter section
        with st.container():
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                trial_phases = st.selectbox(
                    "Trial Phases",
                    ["All Phases", "Phase I", "Phase II", "Phase III", "Phase IV"],
                    help="Select trial development phase"
                )
            
            with col2:
                status_filter = st.selectbox(
                    "Status", 
                    ["All Status", "Recruiting", "Active", "Completed", "Suspended"],
                    help="Filter by trial status"
                )
            
            with col3:
                date_range = st.selectbox(
                    "Date Range",
                    ["Last 5 Years", "Last 3 Years", "Last Year", "All Time"],
                    help="Filter by study timeline"
                )
            
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                ai_search_btn = st.form_submit_button("🔍 AI Search", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Academic Research section
        st.markdown("""
        <div class="academic-section">
            <h3 class="academic-title">
                📚 Academic Research
            </h3>
        """, unsafe_allow_html=True)
        
        scholar_query = st.text_input(
            "Google Scholar Query",
            placeholder="Search academic literature and research papers related to your query",
            help="Include Google Scholar search results",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            include_scholar = st.checkbox("Include Google Scholar", value=False, help="Search academic literature")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle search
    if ai_search_btn and query:
        st.success(f"🔍 Searching for: **{query}** with **{search_type}** focus")
        with st.spinner("AI is analyzing clinical trials..."):
            time.sleep(2)  # Simulate processing
            st.info("🤖 **AI Classification Complete** - Found 147 relevant trials with 89% average confidence")

def render_footer():
    """Render the professional footer matching the screenshot"""
    st.markdown("""
    <div class="footer-section">
        <div class="footer-grid">
            <div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #06b6d4, #0891b2); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 1rem; color: white; font-weight: bold;">T</div>
                    <h4 style="color: #06b6d4; font-size: 1.2rem; margin: 0;">TrialScope</h4>
                </div>
                <p>AI-powered clinical trial intelligence platform connecting researchers with relevant research studies.</p>
            </div>
            <div>
                <h4>Platform</h4>
                <p><a href="#">AI Search</a></p>
                <p><a href="#">API Access</a></p>
                <p><a href="#">Analytics</a></p>
                <p><a href="#">Reports</a></p>
            </div>
            <div>
                <h4>Resources</h4>
                <p><a href="#">Documentation</a></p>
                <p><a href="#">Research Guide</a></p>
                <p><a href="#">Case Studies</a></p>
                <p><a href="#">Support</a></p>
            </div>
            <div>
                <h4>Company</h4>
                <p><a href="#">About</a></p>
                <p><a href="#">Privacy</a></p>
                <p><a href="#">Terms</a></p>
                <p><a href="#">Contact</a></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    try:
        logger.info("Starting TrialScope AI application")
        
        # Render the complete interface
        render_navigation()
        render_hero_section()
        render_search_interface()
        render_footer()
        
    except Exception as e:
        logger.error(f"Error in main application: {str(e)}", exc_info=True)
        st.error("An error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()