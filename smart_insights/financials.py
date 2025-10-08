# smart_insights/financials.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("💰 Financials")
    
    if not company:
        st.warning("Please select a company from sidebar")
        return
    
    st.success(f"✅ Analyzing {company} Financials")
    
    # Mock financial data
    financial_data = {
        "TCS": {
            "revenue": {
                "2021": 167311, "2022": 195772, "2023": 245315, "2024": 258286, "2025": 285000
            },
            "profit": {
                "2021": 38501, "2022": 45297, "2023": 56328, "2024": 59215, "2025": 65000
            },
            "net_worth": {
                "2021": 98542, "2022": 115678, "2023": 142563, "2024": 158742, "2025": 175000
            }
        },
        "INFY": {
            "revenue": {
                "2021": 125731, "2022": 142563, "2023": 168542, "2024": 185215, "2025": 205000
            },
            "profit": {
                "2021": 24512, "2022": 28542, "2023": 35214, "2024": 38521, "2025": 42500
            },
            "net_worth": {
                "2021": 78542, "2022": 89542, "2023": 105214, "2024": 118542, "2025": 132000
            }
        },
        "RELIANCE": {
            "revenue": {
                "2021": 456789, "2022": 542163, "2023": 625418, "2024": 685214, "2025": 750000
            },
            "profit": {
                "2021": 45218, "2022": 51245, "2023": 58214, "2024": 62548, "2025": 68500
            },
            "net_worth": {
                "2021": 325478, "2022": 385214, "2023": 452148, "2024": 512478, "2025": 575000
            }
        }
    }
    
    # Default data
    default_data = {
        "revenue": {"2021": 100000, "2022": 120000, "2023": 140000, "2024": 160000, "2025": 180000},
        "profit": {"2021": 20000, "2022": 25000, "2023": 30000, "2024": 35000, "2025": 40000},
        "net_worth": {"2021": 80000, "2022": 100000, "2023": 120000, "2024": 140000, "2025": 160000}
    }
    
    data = financial_data.get(company, default_data)
    
    # Yearly Bar Chart
    years = list(data["revenue"].keys())
    revenue_values = list(data["revenue"].values())
    profit_values = list(data["profit"].values())
    net_worth_values = list(data["net_worth"].values())
    
    fig_yearly = go.Figure()
    
    fig_yearly.add_trace(go.Bar(
        name='Revenue',
        x=years,
        y=revenue_values,
        marker_color='#00D09C'
    ))
    
    fig_yearly.add_trace(go.Bar(
        name='Profit',
        x=years,
        y=profit_values,
        marker_color='#0088FE'
    ))
    
    fig_yearly.add_trace(go.Bar(
        name='Net Worth',
        x=years,
        y=net_worth_values,
        marker_color='#FFBB28'
    ))
    
    fig_yearly.update_layout(
        title=f"{company} - Yearly Financials (in ₹ Cr)",
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_yearly, use_container_width=True)
    
    # Yearly Data Table
    st.subheader("Yearly Financial Data")
    yearly_df = pd.DataFrame({
        'Year': years,
        'Revenue (₹ Cr)': revenue_values,
        'Profit (₹ Cr)': profit_values,
        'Net Worth (₹ Cr)': net_worth_values
    })
    st.dataframe(yearly_df, use_container_width=True)
    
    # Financial Metrics Summary
    st.subheader("📋 Financial Summary")
    
    latest_year = list(data["revenue"].keys())[-1]
    prev_year = list(data["revenue"].keys())[-2]
    
    revenue_growth = ((data["revenue"][latest_year] - data["revenue"][prev_year]) / data["revenue"][prev_year]) * 100
    profit_growth = ((data["profit"][latest_year] - data["profit"][prev_year]) / data["profit"][prev_year]) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Latest Revenue", 
            f"₹{data['revenue'][latest_year]:,} Cr",
            f"{revenue_growth:+.1f}%"
        )
    
    with col2:
        st.metric(
            "Latest Profit", 
            f"₹{data['profit'][latest_year]:,} Cr", 
            f"{profit_growth:+.1f}%"
        )
    
    with col3:
        st.metric("Net Worth", f"₹{data['net_worth'][latest_year]:,} Cr")
    
    with col4:
        profit_margin = (data["profit"][latest_year] / data["revenue"][latest_year]) * 100
        st.metric("Profit Margin", f"{profit_margin:.1f}%")