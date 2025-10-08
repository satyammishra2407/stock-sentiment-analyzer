# smart_insights/about_company.py
import streamlit as st

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("🏢 About Company")
    
    if not company:
        st.warning("Please select a company from sidebar")
        return
    
    # Simple company descriptions only
    company_data = {
        "TCS": "Tata Consultancy Services - India's largest IT company providing software and consulting services globally.",
        "INFY": "Infosys Limited - Global leader in digital services and consulting, enabling clients in 50+ countries.",
        "RELIANCE": "Reliance Industries - India's largest private sector company with businesses in energy, retail and telecom.",
        "HDFCBANK": "HDFC Bank - Leading private sector bank in India with strong digital banking services.",
        "SBIN": "State Bank of India - India's largest public sector bank with extensive branch network nationwide.",
        "WIPRO": "Wipro Limited - Global IT services company known for digital transformation and consulting.",
        "HINDUNILVR": "Hindustan Unilever - India's largest FMCG company with popular household brands.",
        "ITC": "ITC Limited - Diversified company with businesses in FMCG, hotels, paperboards and agri-business.",
        "BAJFINANCE": "Bajaj Finance - Leading non-banking financial company in India offering various loans.",
        "BHARTIARTL": "Bharti Airtel - One of India's largest telecommunications services companies.",
    }
    
    if company in company_data:
        st.success(f"**{company}**")
        st.write(company_data[company])
    else:
        st.error(f"Company '{company}' not found")
        st.info("Try: TCS, INFY, RELIANCE, HDFCBANK, SBIN, WIPRO")