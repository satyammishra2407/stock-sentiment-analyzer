# smart_insights/financials.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("💰 Financials")
    
    if not company:
        st.warning("Please select a company from sidebar")
        return
    
    st.success(f"✅ Analyzing {company} Financials")

    @st.cache_data(show_spinner=False, ttl=60 * 60)
    def fetch_financials(symbol: str):
        # Try common Indian ticker formats first, then the raw symbol
        candidates = []
        upper_symbol = (symbol or "").upper().strip()
        if upper_symbol and not upper_symbol.endswith(".NS"):
            candidates.append(f"{upper_symbol}.NS")
        if upper_symbol:
            candidates.append(upper_symbol)

        revenue_series = None
        profit_series = None
        equity_series = None
        chosen = None

        for candidate in candidates:
            try:
                t = yf.Ticker(candidate)
                fin = t.financials  # annual income statement
                bs = t.balance_sheet  # annual balance sheet
                if fin is None or fin.empty or bs is None or bs.empty:
                    continue

                # Normalize column years to strings like "2024"
                def normalize_year_index(df: pd.DataFrame) -> list[str]:
                    years: list[str] = []
                    for col in df.columns:
                        try:
                            if isinstance(col, (int, float)):
                                years.append(str(int(col)))
                            elif isinstance(col, str) and col.isdigit():
                                years.append(col)
                            else:
                                dt = pd.to_datetime(col)
                                years.append(str(int(dt.year)))
                        except Exception:
                            years.append(str(col))
                    return years

                years_fin = normalize_year_index(fin)
                years_bs = normalize_year_index(bs)

                # Helper to pick first available label from a list
                def first_available(series_labels: list[str], df: pd.DataFrame):
                    for label in series_labels:
                        if label in df.index:
                            return df.loc[label]
                    return None

                # Possible row labels in yfinance for these metrics
                revenue_labels = [
                    "Total Revenue",
                    "TotalRevenue",
                    "Operating Revenue",
                    "OperatingRevenue",
                    "Revenue",
                    "Sales/Revenue",
                ]
                profit_labels = [
                    "Net Income",
                    "NetIncome",
                    "Net Income Common Stockholders",
                    "NetIncome Common Stockholders",
                    "Net Income Applicable To Common Shares",
                ]
                equity_labels = [
                    "Total Stockholder Equity",
                    "TotalStockholderEquity",
                    "Total Equity Gross Minority Interest",
                    "TotalEquityGrossMinorityInterest",
                    "Stockholders' Equity",
                ]

                revenue_series = first_available(revenue_labels, fin)
                profit_series = first_available(profit_labels, fin)
                equity_series = first_available(equity_labels, bs)

                if revenue_series is None and profit_series is None and equity_series is None:
                    continue

                # Convert to dict of year -> value in crores (₹ Cr)
                def to_crores(series: pd.Series, years: list[str]) -> dict[str, float]:
                    if series is None:
                        return {}
                    values = {}
                    for col, year in zip(series.index, years):
                        try:
                            val = float(series[col])
                            # 1 Crore = 10,000,000
                            values[year] = round(val / 1e7, 2)
                        except Exception:
                            continue
                    return values

                revenue = to_crores(revenue_series, years_fin) if revenue_series is not None else {}
                profit = to_crores(profit_series, years_fin) if profit_series is not None else {}
                net_worth = to_crores(equity_series, years_bs) if equity_series is not None else {}

                # Keep up to latest 5 years, sorted ascending by year
                def trim_latest_five(d: dict[str, float]) -> dict[str, float]:
                    if not d:
                        return {}
                    sorted_years = sorted(d.keys())
                    latest = sorted_years[-5:]
                    return {y: d[y] for y in latest}

                revenue = trim_latest_five(revenue)
                profit = trim_latest_five(profit)
                net_worth = trim_latest_five(net_worth)

                # If at least one metric has data, accept this candidate
                if any([revenue, profit, net_worth]):
                    chosen = candidate
                    return {
                        "symbol": chosen,
                        "revenue": revenue,
                        "profit": profit,
                        "net_worth": net_worth,
                    }
            except Exception:
                continue

        return None

    fetched = fetch_financials(company)
    if not fetched:
        st.warning("Live financial data unavailable for the selected symbol. Showing empty placeholders.")
        data = {"revenue": {}, "profit": {}, "net_worth": {}}
    else:
        data = {"revenue": fetched["revenue"], "profit": fetched["profit"], "net_worth": fetched["net_worth"]}
    
    # Yearly Bar Chart
    # Determine the union of years across all available metrics, keep ascending order, limit to 5 latest
    all_years = set()
    all_years.update(list(data["revenue"].keys()))
    all_years.update(list(data["profit"].keys()))
    all_years.update(list(data["net_worth"].keys()))
    years = sorted(all_years)
    if len(years) > 5:
        years = years[-5:]

    # Build aligned series with None for missing values
    revenue_values = [data["revenue"].get(y, None) for y in years]
    profit_values = [data["profit"].get(y, None) for y in years]
    net_worth_values = [data["net_worth"].get(y, None) for y in years]
    
    fig_yearly = go.Figure()
    
    fig_yearly.add_trace(go.Bar(
        name='Revenue (₹ Cr)',
        x=years,
        y=revenue_values,
        marker_color='#00D09C'
    ))
    
    fig_yearly.add_trace(go.Bar(
        name='Profit (₹ Cr)',
        x=years,
        y=profit_values,
        marker_color='#0088FE'
    ))
    
    fig_yearly.add_trace(go.Bar(
        name='Net Worth (₹ Cr)',
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
    
    # Compute metrics only if we have at least two years of data
    revenue_years = sorted(list(data["revenue"].keys()))
    profit_years = sorted(list(data["profit"].keys()))
    latest_year = revenue_years[-1] if revenue_years else None
    prev_year = revenue_years[-2] if len(revenue_years) >= 2 else None
    
    revenue_growth = None
    profit_growth = None
    if latest_year and prev_year and data["revenue"].get(prev_year):
        try:
            revenue_growth = ((data["revenue"][latest_year] - data["revenue"][prev_year]) / data["revenue"][prev_year]) * 100
        except Exception:
            revenue_growth = None
    if len(profit_years) >= 2:
        try:
            profit_growth = ((data["profit"][profit_years[-1]] - data["profit"][profit_years[-2]]) / data["profit"][profit_years[-2]]) * 100
        except Exception:
            profit_growth = None
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if latest_year and latest_year in data["revenue"]:
            st.metric(
                "Latest Revenue", 
                f"₹{data['revenue'][latest_year]:,} Cr",
                f"{revenue_growth:+.1f}%" if revenue_growth is not None else None
            )
        else:
            st.metric("Latest Revenue", "—", None)
    
    with col2:
        last_profit_year = profit_years[-1] if profit_years else None
        if last_profit_year and last_profit_year in data["profit"]:
            st.metric(
                "Latest Profit", 
                f"₹{data['profit'][last_profit_year]:,} Cr", 
                f"{profit_growth:+.1f}%" if profit_growth is not None else None
            )
        else:
            st.metric("Latest Profit", "—", None)
    
    with col3:
        # Show latest available net worth year
        nw_years = sorted(list(data["net_worth"].keys()))
        last_nw_year = nw_years[-1] if nw_years else None
        if last_nw_year:
            st.metric("Net Worth", f"₹{data['net_worth'][last_nw_year]:,} Cr")
        else:
            st.metric("Net Worth", "—")
    
    with col4:
        if latest_year and latest_year in data["revenue"] and last_profit_year and last_profit_year in data["profit"] and data["revenue"][latest_year]:
            try:
                profit_margin = (data["profit"][last_profit_year] / data["revenue"][latest_year]) * 100
                st.metric("Profit Margin", f"{profit_margin:.1f}%")
            except Exception:
                st.metric("Profit Margin", "—")
        else:
            st.metric("Profit Margin", "—")