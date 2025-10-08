# live_dashboard.py
import streamlit as st
from utils import get_stock_data
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def get_stock_history(stock_name, period="1y"):
    """Stock ka historical data laane ke liye"""
    try:
        ticker_symbol = stock_name if '.' in stock_name else f"{stock_name}.NS"
        stock = yf.Ticker(ticker_symbol)
        
        # Period ko yfinance format mei convert karna
        period_map = {
            "1D": "1d", "1W": "1wk", "1M": "1mo", "3M": "3mo",
            "6M": "6mo", "1Y": "1y", "3Y": "3y", "5Y": "5y", "ALL": "max"
        }
        
        hist_data = stock.history(period=period_map.get(period, "1y"))
        return hist_data
    except Exception as e:
        st.error(f"Data lene mei error: {e}")
        return None

def create_stock_chart(hist_data, company, period):
    """Groww jaisa simple line chart banaye - transparent background"""
    if hist_data is None or hist_data.empty:
        return None
    
    # Trend calculate karna - first vs last price
    first_price = hist_data['Close'].iloc[0]
    last_price = hist_data['Close'].iloc[-1]
    
    # Line color trend ke hisaab se
    line_color = '#00d09c' if last_price >= first_price else '#ff4b4b'  # Groww jaisa green/red
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['Close'],
        mode='lines',
        name=f'{company} Price',
        line=dict(color=line_color, width=2.5),
        hovertemplate='<b>Date:</b> %{x|%d %b %Y}<br><b>Price:</b> ₹%{y:.2f}<extra></extra>'
    ))
    
    # Transparent background - Streamlit ke background color ke saath blend hoga
    fig.update_layout(
        title=None,
        xaxis_title='',
        yaxis_title='',
        height=300,
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20),
        plot_bgcolor='rgba(0,0,0,0)',  # Fully transparent
        paper_bgcolor='rgba(0,0,0,0)', # Fully transparent
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            color='white'  # Axis text color
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            side='right',
            color='white'  # Axis text color
        )
    )
    
    return fig

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("📈 Live Stock Dashboard")
    
    if not company:
        st.warning("Sidebar mei company symbol daalo.")
        return

    # Live stock data
    stock_data = get_stock_data(company)
    
    # Header section - Simple version
    if stock_data:
        st.markdown(f"### {company}")
        price_color = "green" if stock_data['change'] >= 0 else "red"
        st.markdown(f"<h2 style='color: {price_color}'>₹{stock_data['current_price']:.2f}</h2>", 
                   unsafe_allow_html=True)
        
        change_icon = "↗️" if stock_data['change'] >= 0 else "↘️"
        change_color = "#00d09c" if stock_data['change'] >= 0 else "#ff4b4b"
        st.markdown(f"<span style='color: {change_color}'>{change_icon} {stock_data['change']:.2f} ({stock_data['change_percent']:.2f}%)</span>", 
                   unsafe_allow_html=True)
    
    st.divider()
    
    # 1. Financial Metrics - SABSE UPAR
    st.subheader("📊 Financial Metrics")
    metrics_cols = st.columns(4)
    
    with metrics_cols[0]:
        st.metric("Revenue", "3.62M", "-137.96%", delta_color="inverse")
    with metrics_cols[1]:
        st.metric("Gross Profit", "1.48M", "-213.4%", delta_color="inverse")
    with metrics_cols[2]:
        st.metric("Net Profit", "0.57M", "-263.16%", delta_color="inverse")
    with metrics_cols[3]:
        st.metric("Sentiment Score", "72%", "+8%")
    
    st.divider()
    
    # 2. Stock Chart - Financial Metrics ke baad
    st.subheader("Stock Chart")
    
    # Session state mein selected period store karo
    if 'selected_period' not in st.session_state:
        st.session_state.selected_period = "1Y"
    
    # Chart display karo - Selected period ke hisaab se
    with st.spinner(f"{st.session_state.selected_period} ka chart load ho raha hai..."):
        hist_data = get_stock_history(company, st.session_state.selected_period)
        
        if hist_data is not None and not hist_data.empty:
            chart_fig = create_stock_chart(hist_data, company, st.session_state.selected_period)
            if chart_fig:
                # Custom CSS for transparent background
                st.markdown("""
                    <style>
                    .stPlotlyChart {
                        background: transparent !important;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
                st.plotly_chart(chart_fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.warning("Chart nahi bana paya")
        else:
            st.warning("Historical data nahi mila")
    
    st.divider()
    
    # 3. NSE Label + Time Period Buttons - NSE ke right side mein
    nse_col1, nse_col2 = st.columns([1, 3])
    
    with nse_col1:
        st.subheader("NSE")
    
    with nse_col2:
        # Time period buttons - NSE ke right side mein
        time_periods = ["1D", "1W", "1M", "3M", "6M", "1Y", "3Y", "5Y", "ALL"]
        
        # Buttons row banaye
        cols = st.columns(len(time_periods))
        
        for i, period in enumerate(time_periods):
            with cols[i]:
                if st.button(period, use_container_width=True, key=f"period_{period}"):
                    st.session_state.selected_period = period
                    st.rerun()
    
    st.divider()
    
    # 4. Chart Statistics - NSE ke niche
    st.subheader("Chart Statistics")
    
    if hist_data is not None and not hist_data.empty:
        current_price = hist_data['Close'].iloc[-1]
        period_high = hist_data['Close'].max()
        period_low = hist_data['Close'].min()
        price_change = current_price - hist_data['Close'].iloc[0]
        percent_change = (price_change / hist_data['Close'].iloc[0]) * 100 if hist_data['Close'].iloc[0] != 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"₹{current_price:.2f}")
        with col2:
            st.metric("Period High", f"₹{period_high:.2f}")
        with col3:
            st.metric("Period Low", f"₹{period_low:.2f}")
    else:
        st.warning("Chart statistics ke liye data nahi mila")
    
    st.divider()
    
    # 5. Performance Summary - SABSE NICHE
    st.subheader("📈 Performance Summary")
    
    # Performance stats agar data available hai toh
    if stock_data:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Today's Change:** ₹{stock_data['change']:.2f} ({stock_data['change_percent']:.2f}%)")
        with col2:
            st.info(f"**Previous Close:** ₹{stock_data['previous_close']:.2f}")
        with col3:
            st.info(f"**Currency:** {stock_data['currency']}")
    
    # Agar historical data hai toh additional performance summary
    if hist_data is not None and not hist_data.empty:
        price_change = hist_data['Close'].iloc[-1] - hist_data['Close'].iloc[0]
        percent_change = (price_change / hist_data['Close'].iloc[0]) * 100 if hist_data['Close'].iloc[0] != 0 else 0
        st.info(f"**{st.session_state.selected_period} Overall Performance:** ₹{price_change:.2f} ({percent_change:.2f}%)")

# Agar stock data nahi mila toh fallback
    if not stock_data:
        st.warning("Stock data nahi mila. INFY, TCS, RELIANCE jaise symbols try karo.")
        return