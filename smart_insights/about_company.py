# smart_insights/about_company.py
import streamlit as st
import yfinance as yf

@st.cache_data(ttl=300)
def fetch_company_profile(symbol):
    """Fetch company profile from yfinance with safe fallbacks.
    Returns a dict with keys: name, sector, industry, website, employees, summary
    """
    try:
        ticker_symbol = symbol if '.' in symbol else f"{symbol}.NS"
        t = yf.Ticker(ticker_symbol)
        info = getattr(t, 'info', None) or {}
        profile = {
            'name': info.get('longName') or info.get('shortName') or symbol,
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'website': info.get('website'),
            'employees': info.get('fullTimeEmployees'),
            'summary': info.get('longBusinessSummary')
        }
        return profile
    except Exception:
        return {
            'name': symbol,
            'sector': None,
            'industry': None,
            'website': None,
            'employees': None,
            'summary': None
        }

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("🏢 About Company")
    
    if not company:
        st.warning("Please select a company from sidebar")
        return
    
    with st.spinner("Fetching company profile..."):
        profile = fetch_company_profile(company)

    st.success(profile.get('name') or company)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sector", profile.get('sector') or "N/A")
    with col2:
        st.metric("Industry", profile.get('industry') or "N/A")
    with col3:
        employees = profile.get('employees')
        st.metric("Employees", f"{employees:,}" if isinstance(employees, int) else "N/A")

    if profile.get('website'):
        st.markdown(f"Website: [{profile['website']}]({profile['website']})")

    st.markdown("---")
    st.subheader("Overview")
    st.write(profile.get('summary') or "No description available right now.")