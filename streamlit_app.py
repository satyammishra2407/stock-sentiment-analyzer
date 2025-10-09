# streamlit_app.py - UPDATED FOR MODULAR EXPERT ANALYSIS
import streamlit as st
from dotenv import load_dotenv
import os

# Load tokens
try:
    BEARER_TOKENS = st.secrets["TWITTER_BEARER_TOKENS"].split(",")
except Exception:
    load_dotenv()
    tokens = os.getenv("TWITTER_BEARER_TOKENS", "")
    BEARER_TOKENS = tokens.split(",") if tokens else []

BEARER_TOKENS = [t.strip() for t in BEARER_TOKENS if t.strip()]
MAX_REQUESTS = len(BEARER_TOKENS)

# Import basic pages
import home
import live_dashboard  
import twitter_sentiment

# Import MODULAR expert analysis
from expert_analysis.main import show_page as expert_analysis_page

st.set_page_config(page_title="Stock Analysis Hub", layout="wide", page_icon="📊")

# Sidebar
st.sidebar.title("📊 Stock Analysis Hub")
company = st.sidebar.text_input("🔍 Enter Company Symbol", "TCS").upper()

# Navigation
page = st.sidebar.radio("Navigate to:", [
    "🏠 Home",
    "📈 Live Dashboard", 
    "🐦 Twitter Sentiment",
    "📰 Expert Analysis",
    "💡 Smart Insights"
])

st.sidebar.info(f"🔑 Available tokens: {MAX_REQUESTS}")

# Smart Insights Page 
def show_smart_insights(company=None, bearer_tokens=None, max_requests=None):
    st.header("💡 Smart Insights & Fundamentals")
    
    if company:
        st.info(f"Currently analyzing: **{company}**")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Fundamentals", 
        "💰 Financials", 
        "🏢 About Company", 
        "📈 Shareholding Pattern"
    ])
    
    with tab1:
        try:
            from smart_insights import fundamentals
            fundamentals.show_page(company=company)
        except Exception as e:
            st.error(f"Fundamentals error: {e}")
    
    with tab2:
        try:
            from smart_insights import financials
            financials.show_page(company=company)
        except Exception as e:
            st.error(f"Financials error: {e}")
    
    with tab3:
        try:
            from smart_insights import about_company
            about_company.show_page(company=company)
        except Exception as e:
            st.error(f"About Company error: {e}")
    
    with tab4:
        try:
            from smart_insights import shareholding_pattern
            shareholding_pattern.show_page(company=company)
        except Exception as e:
            st.error(f"Shareholding error: {e}")

# Routing - UPDATED EXPERT ANALYSIS
if page == "🏠 Home":
    home.show_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)
elif page == "📈 Live Dashboard":
    live_dashboard.show_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)
elif page == "🐦 Twitter Sentiment":
    twitter_sentiment.show_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)
elif page == "📰 Expert Analysis":
    expert_analysis_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)
elif page == "💡 Smart Insights":
    show_smart_insights(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)