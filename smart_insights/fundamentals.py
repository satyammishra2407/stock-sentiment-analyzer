# smart_insights/fundamentals.py
import streamlit as st
import yfinance as yf
import math

@st.cache_data(ttl=60)
def fetch_fundamentals(symbol):
    """Fetch live fundamentals using yfinance, with safe fallbacks.
    Returns a dict with keys: market_cap, pe, pb, eps, roe, dividend_yield
    """
    try:
        ticker_symbol = symbol if '.' in symbol else f"{symbol}.NS"
        t = yf.Ticker(ticker_symbol)

        info = getattr(t, 'info', None) or {}
        shares_outstanding = info.get('sharesOutstanding')
        market_cap = info.get('marketCap')
        trailing_pe = info.get('trailingPE')
        price_to_book = info.get('priceToBook')
        trailing_eps = info.get('trailingEps')
        return_on_equity = info.get('returnOnEquity')
        dividend_yield = info.get('dividendYield')

        # Fallbacks using fast_info
        fast = getattr(t, 'fast_info', None)
        if (market_cap is None) and fast:
            last_price = fast.get('last_price') or fast.get('lastPrice')
            if last_price and shares_outstanding:
                market_cap = float(last_price) * float(shares_outstanding)

        # Normalize/format
        data = {
            'market_cap': market_cap if isinstance(market_cap, (int, float)) else None,
            'pe': trailing_pe if isinstance(trailing_pe, (int, float)) else None,
            'pb': price_to_book if isinstance(price_to_book, (int, float)) else None,
            'eps': trailing_eps if isinstance(trailing_eps, (int, float)) else None,
            'roe': (return_on_equity * 100.0) if isinstance(return_on_equity, (int, float)) else None,
            'dividend_yield': (dividend_yield * 100.0) if isinstance(dividend_yield, (int, float)) else None,
        }
        return data
    except Exception:
        return {
            'market_cap': None,
            'pe': None,
            'pb': None,
            'eps': None,
            'roe': None,
            'dividend_yield': None,
        }

def format_inr(value):
    try:
        if value is None or not isinstance(value, (int, float)) or math.isnan(value):
            return "N/A"
        # Convert to Indian Rupee units (Cr/La/Th if needed). Keep compact: T, B, M style for simplicity
        abs_v = abs(value)
        if abs_v >= 1_000_000_000_000:
            return f"₹{value/1_000_000_000_000:.2f}T"
        if abs_v >= 1_000_000_000:
            return f"₹{value/1_000_000_000:.2f}B"
        if abs_v >= 1_000_000:
            return f"₹{value/1_000_000:.2f}M"
        return f"₹{value:,.0f}"
    except Exception:
        return "N/A"

def format_number(value, suffix=""):
    try:
        if value is None or not isinstance(value, (int, float)) or math.isnan(value):
            return "N/A"
        return f"{value:.2f}{suffix}"
    except Exception:
        return "N/A"

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("📊 Fundamentals")
    
    if not company:
        st.warning("Please select a company from sidebar")
        return
    
    # Fetch live fundamentals
    with st.spinner("Fetching live fundamentals..."):
        fundamentals = fetch_fundamentals(company)

    # Display in 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Market Cap", format_inr(fundamentals.get('market_cap')))
        st.metric("P/E Ratio", format_number(fundamentals.get('pe')))

    with col2:
        st.metric("P/B Ratio", format_number(fundamentals.get('pb')))
        st.metric("EPS", format_inr(fundamentals.get('eps')) if fundamentals.get('eps') is not None and abs(fundamentals.get('eps')) > 1000 else format_number(fundamentals.get('eps'), suffix="" if fundamentals.get('eps') is None else ""))

    with col3:
        st.metric("ROE", format_number(fundamentals.get('roe'), suffix="%"))
        st.metric("Dividend Yield", format_number(fundamentals.get('dividend_yield'), suffix="%"))

    # Notes / fallback info
    if all(v is None for v in fundamentals.values()):
        st.warning("Live fundamentals not available for this symbol right now.")