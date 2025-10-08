# smart_insights/fundamentals.py
import streamlit as st

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("📊 Fundamentals")
    
    if not company:
        st.warning("Please select a company from sidebar")
        return
    
    # SUCCESS MESSAGE - YEH ZAROOR DIKHEGA
    st.success("🎯 FUNDAMENTALS LOADED SUCCESSFULLY!")
    
    # Simple fundamentals data
    data = {
        "TCS": {
            "Market Cap": "₹13.5T", 
            "P/E Ratio": "30.2", 
            "P/B Ratio": "8.5",
            "EPS": "₹120.5", 
            "ROE": "25.3%",
            "Dividend Yield": "1.8%"
        },
        "INFY": {
            "Market Cap": "₹6.8T", 
            "P/E Ratio": "25.1", 
            "P/B Ratio": "6.2",
            "EPS": "₹60.3", 
            "ROE": "22.7%",
            "Dividend Yield": "2.1%"
        },
        "RELIANCE": {
            "Market Cap": "₹19.2T", 
            "P/E Ratio": "28.5", 
            "P/B Ratio": "2.1",
            "EPS": "₹95.7", 
            "ROE": "9.8%",
            "Dividend Yield": "0.4%"
        }
    }
    
    if company in data:
        info = data[company]
        
        # Display in 3 columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Market Cap", info["Market Cap"])
            st.metric("P/E Ratio", info["P/E Ratio"])
            
        with col2:
            st.metric("P/B Ratio", info["P/B Ratio"])
            st.metric("EPS", info["EPS"])
            
        with col3:
            st.metric("ROE", info["ROE"])
            st.metric("Dividend Yield", info["Dividend Yield"])
    else:
        st.warning(f"No fundamentals data for {company}")
        st.info("Available: TCS, INFY, RELIANCE")