# smart_insights/shareholding_pattern.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("📈 Shareholding Pattern")
    
    if not company:
        st.warning("Please select a company from sidebar")
        return
    
    st.success(f"✅ Analyzing {company} Shareholding Pattern")
    
    # Mock shareholding pattern data
    shareholding_data = {
        "TCS": {
            "Q1 FY25": {
                "Promoters": 72.3, "FII": 15.2, "DII": 8.1, "Public": 4.4
            },
            "Q4 FY24": {
                "Promoters": 72.5, "FII": 15.0, "DII": 8.0, "Public": 4.5
            }
        },
        "INFY": {
            "Q1 FY25": {
                "Promoters": 14.2, "FII": 34.5, "DII": 35.8, "Public": 15.5
            },
            "Q4 FY24": {
                "Promoters": 14.5, "FII": 34.2, "DII": 35.5, "Public": 15.8
            }
        },
        "RELIANCE": {
            "Q1 FY25": {
                "Promoters": 50.4, "FII": 23.8, "DII": 16.2, "Public": 9.6
            },
            "Q4 FY24": {
                "Promoters": 50.6, "FII": 23.5, "DII": 16.4, "Public": 9.5
            }
        }
    }
    
    # Default data
    default_data = {
        "Q1 FY25": {"Promoters": 50.0, "FII": 25.0, "DII": 15.0, "Public": 10.0},
        "Q4 FY24": {"Promoters": 51.0, "FII": 24.5, "DII": 14.5, "Public": 10.0}
    }
    
    data = shareholding_data.get(company, default_data)
    
    # Latest quarter data
    latest_quarter = list(data.keys())[0]
    latest_data = data[latest_quarter]
    
    # Pie Chart for latest quarter
    st.subheader(f"Shareholding Pattern - {latest_quarter}")
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(latest_data.keys()),
        values=list(latest_data.values()),
        hole=0.4,
        marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    )])
    
    fig_pie.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Data Table
    st.subheader("Detailed Shareholding Data (%)")
    
    # Create DataFrame
    table_data = []
    for quarter in data.keys():
        row = {"Quarter": quarter}
        row.update(data[quarter])
        table_data.append(row)
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)