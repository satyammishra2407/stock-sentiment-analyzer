# utils.py
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_stock_data(stock_name):
    """Return a small dict with live price info (uses yfinance)."""
    try:
        ticker_symbol = stock_name if '.' in stock_name else f"{stock_name}.NS"
        stock = yf.Ticker(ticker_symbol)
        info = stock.info or {}
        current_price = info.get('currentPrice', info.get('regularMarketPrice', None))
        previous_close = info.get('previousClose', None)
        if current_price is None or previous_close is None:
            return None
        change = round(current_price - previous_close, 2)
        change_percent = round((change / previous_close) * 100, 2) if previous_close else 0
        return {
            'current_price': current_price,
            'previous_close': previous_close,
            'change': change,
            'change_percent': change_percent,
            'currency': info.get('currency', '₹')
        }
    except Exception:
        return None

def get_expert_analysis(company_name):
    """Mock expert analysis — replace with real API/web-scrape if needed."""
    analysis_data = {
        "INFY": {
            "recommendations": [
                {"broker": "Goldman Sachs", "rating": "Buy", "target": "₹2,100", "change": "+5%"},
                {"broker": "Morgan Stanley", "rating": "Hold", "target": "₹1,850", "change": "0%"},
            ],
            "news": [
                "Infosys wins $500M digital transformation deal.",
                "Company announces special dividend."
            ],
            "insights": [
                "Digital revenue growth remains strong.",
                "North America continues to recover."
            ]
        }
        # add other tickers...
    }
    default = {
        "recommendations": [{"broker": "Goldman Sachs", "rating": "Buy", "target": "₹2,000", "change":"+5%"}],
        "news": ["Strong quarterly results expected."],
        "insights": ["Sector tailwinds supporting growth"]
    }
    return analysis_data.get(company_name, default)

def save_sentiment_plot(counts, filename="sentiment_graph.png", title="Sentiment"):
    """Save bar chart for sentiment counts using matplotlib."""
    plt.close("all")
    fig, ax = plt.subplots(figsize=(6,3))
    counts = counts.sort_values(ascending=False)
    counts.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Count")
    ax.set_xlabel("")
    ax.set_xticklabels([str(x) for x in counts.index], rotation=0)
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return os.path.abspath(filename)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)