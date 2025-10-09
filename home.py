# home.py - COMPACT WITH BULL VS BEAR IMAGE
import streamlit as st
import pandas as pd
from datetime import datetime

def show_page(company=None, bearer_tokens=None, max_requests=None):
    # Custom CSS for compact styling
    st.markdown("""
    <style>
    /* Compact Hero Section */
    .hero-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .hero-text {
        flex: 1;
        padding-right: 20px;
    }
    .hero-text h1 {
        font-size: 2.2rem;
        margin-bottom: 5px;
        font-weight: 700;
    }
    .hero-text p {
        font-size: 1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    .hero-image {
        flex: 0 0 150px;
        text-align: center;
    }
    .hero-image img {
        width: 120px;
        height: 120px;
        border-radius: 10px;
        object-fit: cover;
        border: 3px solid rgba(255,255,255,0.3);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .animated-card {
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Compact Cards */
    .compact-card {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 12px;
    }
    
    .market-status {
        background: rgba(0,208,156,0.15);
        padding: 6px 12px;
        border-radius: 6px;
        border: 1px solid rgba(0,208,156,0.3);
        font-size: 0.85rem;
        text-align: center;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 15px 0;
    }
    
    .feature-item {
        background: rgba(255,255,255,0.03);
        padding: 12px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .feature-item:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(0,208,156,0.3);
        transform: translateY(-2px);
    }
    
    .step-card {
        text-align: center;
        padding: 12px;
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.08);
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    # HERO SECTION WITH IMAGE
    st.markdown("""
    <div class="hero-container">
        <div class="hero-text">
            <h1>Stock Sentiment Analyzer</h1>
            <p>AI-Powered Investment Companion</p>
        </div>
        <div class="hero-image">
            <img src="https://img.freepik.com/premium-photo/bull-vs-bear-symbols-stock-market-trends-fierce-market-battle-red-green-charts_136403-42657.jpg?w=900" 
                 alt="Bull vs Bear Stock Market">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # COMPACT STATUS BAR
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        current_time = datetime.now().strftime("%d %b %Y | %I:%M %p")
        st.markdown(f'<div class="market-status">🕐 {current_time}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="market-status pulse-animation">🟢 LIVE</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="market-status">🔑 {max_requests}</div>', unsafe_allow_html=True)
    
    with col4:
        if company:
            st.markdown(f'<div class="market-status">🎯 {company}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # COMPACT MARKET SNAPSHOT
    st.subheader("🌍 Market Snapshot")
    
    tab1, tab2 = st.tabs(["🇮🇳 Indian Markets", "🌎 Global Markets"])

    with tab1:
        st.markdown('<div class="animated-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nifty 50", "22,475", "+125.30")
        with col2:
            st.metric("Sensex", "74,125", "+350.45")
        with col3:
            st.metric("Bank Nifty", "48,231", "+85.75")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="animated-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("S&P 500", "5,235", "+25.45")
        with col2:
            st.metric("Dow Jones", "39,125", "+150.30")
        with col3:
            st.metric("Nasdaq", "16,385", "+85.75")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # COMPACT FEATURE GRID
    st.subheader("🚀 Analysis Tools")
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-item animated-card">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">📈</div>
            <h4 style="margin: 5px 0; font-size: 1rem;">Live Dashboard</h4>
            <p style="margin: 0; font-size: 0.8rem;">Real-time charts & metrics</p>
        </div>
        <div class="feature-item animated-card" style="animation-delay: 0.1s">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🐦</div>
            <h4 style="margin: 5px 0; font-size: 1rem;">Twitter Sentiment</h4>
            <p style="margin: 0; font-size: 0.8rem;">Public opinion analysis</p>
        </div>
        <div class="feature-item animated-card" style="animation-delay: 0.2s">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">📰</div>
            <h4 style="margin: 5px 0; font-size: 1rem;">Expert Analysis</h4>
            <p style="margin: 0; font-size: 0.8rem;">News & broker insights</p>
        </div>
        <div class="feature-item animated-card" style="animation-delay: 0.3s">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">💡</div>
            <h4 style="margin: 5px 0; font-size: 1rem;">Smart Insights</h4>
            <p style="margin: 0; font-size: 0.8rem;">Fundamentals & patterns</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # COMPACT QUICK START
    st.subheader("🎯 Get Started")
    
    steps_col1, steps_col2, steps_col3 = st.columns(3)
    
    with steps_col1:
        st.markdown("""
        <div class="step-card animated-card">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🔍</div>
            <h4 style="margin: 5px 0; font-size: 0.9rem;">Enter Symbol</h4>
            <p style="margin: 0; font-size: 0.75rem;">Type stock symbol</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div class="step-card animated-card" style="animation-delay: 0.1s">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">📊</div>
            <h4 style="margin: 5px 0; font-size: 0.9rem;">Choose Tool</h4>
            <p style="margin: 0; font-size: 0.75rem;">Select analysis type</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col3:
        st.markdown("""
        <div class="step-card animated-card" style="animation-delay: 0.2s">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">💡</div>
            <h4 style="margin: 5px 0; font-size: 0.9rem;">Get Insights</h4>
            <p style="margin: 0; font-size: 0.75rem;">Receive analysis</p>
        </div>
        """, unsafe_allow_html=True)

    # CURRENT SELECTION
    if company:
        st.markdown("---")
        st.success(f"**Currently analyzing:** **{company}** - Select tools from sidebar to explore!")

    # COMPACT FOOTER
    st.markdown("""
    <div style="text-align: center; padding: 15px; margin-top: 20px;">
        <p style="color: #666; font-size: 0.75rem;">Built with ❤️ using Streamlit • Real-time Data • AI Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# Agar directly run kiya jaaye toh
if __name__ == "__main__":
    show_page()