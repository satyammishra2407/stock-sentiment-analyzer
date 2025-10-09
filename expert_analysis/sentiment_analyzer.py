# expert_analysis/sentiment_analyzer.py
from textblob import TextBlob
import pandas as pd
import plotly.graph_objects as go

def analyze_news_sentiment(news_articles):
    """Analyze sentiment for news articles"""
    if not news_articles:
        return {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
    
    sentiments = []
    
    for article in news_articles:
        title = article.get('title', '')
        description = article.get('description', '')
        content = f"{title}. {description}"
        
        # Sentiment analysis
        sentiment = classify_sentiment(content)
        sentiments.append(sentiment)
    
    # Count sentiments
    sentiment_counts = pd.Series(sentiments).value_counts()
    
    return {
        "positive": sentiment_counts.get("Positive", 0),
        "negative": sentiment_counts.get("Negative", 0),
        "neutral": sentiment_counts.get("Neutral", 0),
        "total": len(news_articles)
    }

def classify_sentiment(text):
    """Classify text sentiment"""
    try:
        polarity = TextBlob(text).sentiment.polarity
        
        # Adjusted thresholds for financial news
        if polarity > 0.15:
            return "Positive"
        elif polarity < -0.15:
            return "Negative"
        else:
            return "Neutral"
    except:
        return "Neutral"

def create_sentiment_piechart(sentiment_data):
    """Create pie chart for sentiment distribution"""
    labels = ['Positive', 'Negative', 'Neutral']
    values = [
        sentiment_data['positive'],
        sentiment_data['negative'], 
        sentiment_data['neutral']
    ]
    
    colors = ['#00d09c', '#ff4b4b', '#ffb800']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker_colors=colors,
        textinfo='label+percent',
        hoverinfo='label+value+percent'
    )])
    
    fig.update_layout(
        height=300,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return fig