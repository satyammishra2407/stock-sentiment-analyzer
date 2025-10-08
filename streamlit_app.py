# streamlit_app.py
import importlib
import smart_insights.financials, smart_insights.shareholding_pattern
importlib.reload(smart_insights.financials)
importlib.reload(smart_insights.shareholding_pattern)
import streamlit as st
from dotenv import load_dotenv
import os, sys

# Ensure relative imports work
sys.path.append(os.path.dirname(__file__))

# Load tokens
try:
    BEARER_TOKENS = st.secrets["TWITTER_BEARER_TOKENS"].split(",")
except Exception:
    load_dotenv()
    tokens = os.getenv("TWITTER_BEARER_TOKENS", "")
    BEARER_TOKENS = tokens.split(",") if tokens else []

BEARER_TOKENS = [t.strip() for t in BEARER_TOKENS if t.strip()]
MAX_REQUESTS = len(BEARER_TOKENS)

# Import main pages
import home
import live_dashboard
import twitter_sentiment
import expert_analysis

# Streamlit config
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


# -------- SMART INSIGHTS --------
def show_smart_insights(company=None, bearer_tokens=None, max_requests=None):
    st.header("💡 Smart Insights & Fundamentals")

    if company:
        st.info(f"Currently analyzing: **{company}**")

    # Lazy imports to ensure latest module reload
    from smart_insights import fundamentals, financials, about_company, shareholding_pattern

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Fundamentals",
        "💰 Financials",
        "🏢 About Company",
        "📈 Shareholding Pattern"
    ])

    with tab1:
        st.write("📊 **Fundamentals Section Loaded Successfully**")
        fundamentals.show_page(company=company, bearer_tokens=bearer_tokens, max_requests=max_requests)

    with tab2:
        st.write("💰 **Financials Section Loaded Successfully**")
        financials.show_page(company=company, bearer_tokens=bearer_tokens, max_requests=max_requests)

    with tab3:
        st.write("🏢 **About Company Section Loaded Successfully**")
        about_company.show_page(company=company, bearer_tokens=bearer_tokens, max_requests=max_requests)

    with tab4:
        st.write("📈 **Shareholding Pattern Section Loaded Successfully**")
        shareholding_pattern.show_page(company=company, bearer_tokens=bearer_tokens, max_requests=max_requests)


# -------- ROUTING --------
if page == "🏠 Home":
    home.show_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)

elif page == "📈 Live Dashboard":
    live_dashboard.show_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)

elif page == "🐦 Twitter Sentiment":
    twitter_sentiment.show_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)

elif page == "📰 Expert Analysis":
    expert_analysis.show_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)

elif page == "💡 Smart Insights":
    show_smart_insights(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)
