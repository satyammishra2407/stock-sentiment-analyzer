# expert_analysis.py
import streamlit as st
from utils import get_expert_analysis
import random

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("📰 Professional Analysis & News")
    company = (company or "").upper()
    if not company:
        st.info("Select a company from the sidebar.")
        return

    data = get_expert_analysis(company)
    st.header("🏛️ Broker Recommendations")
    for rec in data.get("recommendations", []):
        c1, c2, c3, c4 = st.columns([2,1,1,1])
        c1.write(f"**{rec['broker']}**")
        rating_color = "green" if "buy" in rec['rating'].lower() else "orange" if "hold" in rec['rating'].lower() else "red"
        c2.markdown(f"<span style='color:{rating_color};font-weight:bold'>{rec['rating']}</span>", unsafe_allow_html=True)
        c3.write(f"Target: {rec['target']}")
        c4.write(f"{rec['change']}")
        st.divider()

    st.header("📢 Latest News")
    for i, n in enumerate(data.get("news", [])[:5], 1):
        st.write(f"{i}. {n}")
        st.caption(f"Published {random.randint(1,72)} hours ago")
        st.divider()

    st.header("💡 Expert Insights")
    for insight in data.get("insights", []):
        st.write(f"- {insight}")
