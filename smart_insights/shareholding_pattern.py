# smart_insights/shareholding_pattern.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import requests
import re

@st.cache_data(ttl=300)
def fetch_shareholding_breakdown(symbol):
    """Best-effort shareholding using yfinance info/holders.
    Priority order:
    1) info.heldPercentInsiders / info.heldPercentInstitutions
    2) major_holders table (insiders/institutions rows)
    3) institutional_holders + mutualfund_holders summed
    Returns dict percentages in [0,100].
    """
    try:
        ticker_symbol = symbol if '.' in symbol else f"{symbol}.NS"
        t = yf.Ticker(ticker_symbol)
        info = getattr(t, 'info', None) or {}

        def normalize_pct(val):
            try:
                if val is None:
                    return None
                f = float(val)
                if 0 < f <= 1:  # fraction
                    return f * 100.0
                if 0 <= f <= 100:  # already percentage
                    return f
                return None
            except Exception:
                return None

        insiders_pct = normalize_pct(info.get('heldPercentInsiders'))
        institutions_pct = normalize_pct(info.get('heldPercentInstitutions'))

        # Fallback 2: major_holders table
        if insiders_pct is None or institutions_pct is None:
            mh = getattr(t, 'major_holders', None)
            if isinstance(mh, pd.DataFrame) and not mh.empty:
                for i in range(len(mh)):
                    # Column 1 often numeric, column 2 label
                    try:
                        val_raw = mh.iloc[i, 0]
                        label = str(mh.iloc[i, 1]).lower()
                        val_pct = normalize_pct(str(val_raw).replace('%', '').strip())
                    except Exception:
                        continue
                    if val_pct is None:
                        continue
                    if ('insider' in label or 'promoter' in label) and insiders_pct is None:
                        insiders_pct = val_pct
                    if 'institution' in label and institutions_pct is None:
                        institutions_pct = val_pct

        # Fallback 3: sum of institutional holders and mutual funds
        if institutions_pct is None:
            total_inst = 0.0
            found = False
            ih = getattr(t, 'institutional_holders', None)
            if isinstance(ih, pd.DataFrame) and not ih.empty:
                col = None
                for c in ih.columns:
                    if 'Percent' in str(c):
                        col = c
                        break
                if col:
                    for v in ih[col].dropna().tolist():
                        nv = normalize_pct(v)
                        if nv is not None:
                            total_inst += nv
                            found = True
            mf = getattr(t, 'mutualfund_holders', None)
            if isinstance(mf, pd.DataFrame) and not mf.empty:
                col = None
                for c in mf.columns:
                    if 'Percent' in str(c):
                        col = c
                        break
                if col:
                    for v in mf[col].dropna().tolist():
                        nv = normalize_pct(v)
                        if nv is not None:
                            total_inst += nv
                            found = True
            institutions_pct = total_inst if found else None

        # Clamp and compute public
        insiders_pct = max(0.0, min(100.0, insiders_pct)) if insiders_pct is not None else None
        institutions_pct = max(0.0, min(100.0, institutions_pct)) if institutions_pct is not None else None
        public_pct = None
        if insiders_pct is not None and institutions_pct is not None:
            public_pct = max(0.0, 100.0 - insiders_pct - institutions_pct)

        return {
            'Promoters': insiders_pct,
            'Institutions': institutions_pct,
            'Public': public_pct
        }
    except Exception:
        return {'Promoters': None, 'Institutions': None, 'Public': None}

@st.cache_data(ttl=300)
def fetch_shareholding_from_nse(symbol):
    """Fetch detailed shareholding from NSE's public API and aggregate into
    Promoters, Domestic Institutions, Foreign Institutions, Retail.
    Returns dict percentages in [0,100] or None values if unavailable.
    """
    try:
        sym = symbol.replace('.NS', '').replace('.BSE', '').upper()
        s = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.nseindia.com/',
        }
        s.get('https://www.nseindia.com', headers=headers, timeout=10)
        url = f"https://www.nseindia.com/api/corporates-share-holdings?index=equities&symbol={sym}"
        resp = s.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return {'Promoters': None, 'Domestic Institutions': None, 'Foreign Institutions': None, 'Retail': None}
        payload = resp.json()
        rows = payload.get('data') or payload.get('shareHolding') or payload
        if not isinstance(rows, list):
            return {'Promoters': None, 'Domestic Institutions': None, 'Foreign Institutions': None, 'Retail': None}

        def pct_from_row(row):
            # try multiple keys
            for k in ('percentage', 'percent', 'percShare', 'pct'): 
                v = row.get(k)
                if v is not None:
                    try:
                        return float(str(v).replace('%', '').strip())
                    except Exception:
                        continue
            return None

        prom = 0.0
        fii = 0.0
        dii = 0.0
        retail = 0.0
        total_inst = 0.0

        # Keyword sets (broad coverage of NSE labels)
        fii_patterns = r'foreign\s*(institution|portfolio|fii|fpi)|qfi'
        dii_patterns = r'mutual\s*fund|insurance|bank|financial\s*institution|nbfc|uti|alternate\s*investment|aif|pension|development\s*financial|venture\s*capital'
        promoters_patterns = r'promoter'
        # Anything not promoter/FII/DII is public (retail/non-institution)
        total_patterns = r'total|summary'

        for r in rows:
            cat_raw = ' '.join([str(r.get(k, '')) for k in ('category', 'categoryName', 'cat', 'subCategory', 'subCategoryDesc')])
            cat = cat_raw.lower()
            pct = pct_from_row(r)
            if pct is None:
                continue
            # Skip totals rows to avoid double counting
            if re.search(total_patterns, cat):
                # track total institutions if present for display only
                if 'institution' in cat:
                    total_inst += pct
                continue
            if re.search(promoters_patterns, cat):
                prom += pct; continue
            if re.search(fii_patterns, cat):
                fii += pct; continue
            if re.search(dii_patterns, cat):
                dii += pct; continue
            # Treat every other category as public (non-institution)
            retail += pct

        # If everything is zero, treat as unavailable
        if prom == fii == dii == retail == 0.0:
            return {'Promoters': None, 'Domestic Institutions': None, 'Foreign Institutions': None, 'Retail': None}

        # Make consistent buckets
        prom = max(0.0, min(100.0, prom))
        fii = max(0.0, min(100.0, fii))
        dii = max(0.0, min(100.0, dii))
        # Retail is whatever remains after Promoters + Institutions
        retail = max(0.0, 100.0 - (prom + fii + dii))
        total = prom + fii + dii + retail
        if 99.0 <= total <= 101.0 and total != 100.0:
            # tiny rounding fix
            scale = 100.0 / total
            prom *= scale; fii *= scale; dii *= scale; retail *= scale
        total_inst = fii + dii if total_inst == 0 else total_inst

        return {'Promoters': prom, 'Domestic Institutions': dii, 'Foreign Institutions': fii, 'Institutions (Total)': (total_inst if total_inst > 0 else fii + dii), 'Retail': retail}
    except Exception:
        return {'Promoters': None, 'Domestic Institutions': None, 'Foreign Institutions': None, 'Retail': None}

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("📈 Shareholding Pattern")
    
    if not company:
        st.warning("Please select a company from sidebar")
        return
    
    st.success(f"✅ Analyzing {company} Shareholding Pattern")

    # Prefer NSE detailed data; fall back to Yahoo-derived buckets
    detailed = fetch_shareholding_from_nse(company)
    promoters = detailed.get('Promoters') if isinstance(detailed, dict) else None
    if promoters is None:
        yahoo_simple = fetch_shareholding_breakdown(company)
        promoters = yahoo_simple.get('Promoters') if isinstance(yahoo_simple, dict) else None
    if promoters is None:
        st.warning("Live promoter holding not available right now. Showing placeholder.")
        promoters = 0.0
    # Public is the rest
    promoters = max(0.0, min(100.0, float(promoters)))
    public = max(0.0, 100.0 - promoters)
    breakdown = {"Promoters": promoters, "Public": public}
    
    # Pie Chart for latest quarter
    st.subheader("Current Shareholding Pattern (approx.)")
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Promoters", "Public"],
        values=[breakdown["Promoters"], breakdown["Public"]],
        hole=0.4,
        marker_colors=['#FF6B6B', '#45B7D1']
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
    df = pd.DataFrame([breakdown])
    st.dataframe(df, use_container_width=True)