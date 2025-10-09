# expert_analysis/main.py
import streamlit as st
from .news_service import get_stock_news
from .sentiment_analyzer import analyze_news_sentiment
from .ui_components import create_news_card, show_sentiment_summary

def show_page(company=None, bearer_tokens=None, max_requests=None):
    """Main expert analysis page - Grow app style (News Only)"""
    
    st.subheader("📰 Live News & Sentiment Analysis")
    company = (company or "").upper()
    
    if not company:
        st.info("Select a company from the sidebar.")
        return
    
    # Fetch live news
    with st.spinner(f"📡 Fetching latest news for {company}..."):
        news_articles = get_stock_news(company)
    
    # Show news section
    st.header(f"📢 Latest News for {company}")
    
    if not news_articles:
        st.info("📭 No recent news found for this stock")
        st.write("This might be a small-cap stock or not frequently covered by media")
    else:
        # Display news cards
        for i, article in enumerate(news_articles):
            create_news_card(article, i)
    
    # Sentiment analysis (only if news available)
    if news_articles:
        sentiment_data = analyze_news_sentiment(news_articles)
        show_sentiment_summary(sentiment_data, company)
        