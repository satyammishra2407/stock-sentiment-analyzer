# home.py
import streamlit as st

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.title("🏠 Stock Analysis Hub")
    st.write("Modular dashboard — use the sidebar to navigate.")
    st.markdown("""
    **Pages:**\n
    - Live Dashboard: live price + metrics\n
    - Twitter Sentiment: fetch tweets + sentiment\n
    - Expert Analysis: mock broker recommendations\n
    - Smart Insights: AI style quick insights
    """)
    if company:
        st.info(f"Current company set: **{company}**")
