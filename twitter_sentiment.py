# twitter_sentiment.py - UPDATED ATTRACTIVE DESIGN
import streamlit as st
import time
import plotly.graph_objects as go
import plotly.express as px
from app import get_tweets, save_to_csv
import pandas as pd

COOLDOWN_SECONDS = 16 * 60  # 16 minutes

def create_attractive_sentiment_chart(df, keyword):
    """Create attractive sentiment charts like Groww"""
    
    # Count sentiments
    sentiment_counts = df["sentiment"].value_counts()
    
    # Colors - Groww style
    colors = {
        'Positive': '#00d09c',  # Green
        'Negative': '#ff4b4b',  # Red  
        'Neutral': '#ffb800'    # Yellow
    }
    
    # 1. PIE CHART - Main visual
    fig_pie = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        hole=0.5,
        marker_colors=[colors.get(x, '#808080') for x in sentiment_counts.index],
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        textfont=dict(size=14, color='white'),
        marker=dict(line=dict(color='#1e1e1e', width=2))
    )])
    
    fig_pie.update_layout(
        height=350,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title={
            'text': f"💬 Sentiment Distribution - {keyword}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': 'white'}
        }
    )
    
    # 2. BAR CHART - Detailed view
    fig_bar = go.Figure(data=[go.Bar(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        marker_color=[colors.get(x, '#808080') for x in sentiment_counts.index],
        text=sentiment_counts.values,
        textposition='auto',
        marker=dict(
            line=dict(color='#1e1e1e', width=1),
            opacity=0.8
        )
    )])
    
    fig_bar.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            title='Sentiment',
            title_font=dict(size=14, color='white'),
            tickfont=dict(size=12, color='white')
        ),
        yaxis=dict(
            title='Number of Tweets',
            title_font=dict(size=14, color='white'),
            tickfont=dict(size=12, color='white'),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        title={
            'text': "📊 Tweet Count by Sentiment",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        }
    )
    
    return fig_pie, fig_bar

def show_sentiment_metrics(df):
    """Show beautiful sentiment metrics"""
    total_tweets = len(df)
    positive = len(df[df['sentiment'] == 'Positive'])
    negative = len(df[df['sentiment'] == 'Negative']) 
    neutral = len(df[df['sentiment'] == 'Neutral'])
    
    positive_pct = (positive / total_tweets) * 100 if total_tweets > 0 else 0
    negative_pct = (negative / total_tweets) * 100 if total_tweets > 0 else 0
    neutral_pct = (neutral / total_tweets) * 100 if total_tweets > 0 else 0
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Tweets", 
            total_tweets,
            help="Total number of tweets analyzed"
        )
    
    with col2:
        st.metric(
            "Positive 👍", 
            f"{positive} ({positive_pct:.1f}%)",
            delta=f"{positive_pct:.1f}%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Negative 👎", 
            f"{negative} ({negative_pct:.1f}%)",
            delta=f"-{negative_pct:.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Neutral 😐", 
            f"{neutral} ({neutral_pct:.1f}%)",
            delta=f"{neutral_pct:.1f}%"
        )

def show_page(company=None, bearer_tokens=None, max_requests=0):
    st.subheader("🐦 Public Sentiment Analysis")
    
    # Header with description
    st.markdown("""
    <style>
    .sentiment-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
    <div class="sentiment-header">
        <h3>📊 Real-time Twitter Sentiment Analysis</h3>
        <p>Analyze public opinion about stocks from Twitter data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        keyword = st.text_input(
            "🔍 Enter keyword to analyze:", 
            company or "",
            placeholder="e.g., TCS, Infosys, Reliance..."
        )
    
    with col2:
        tweet_limit = st.slider(
            "🔢 Number of tweets", 
            10, 100, 50,
            help="More tweets = better analysis but slower"
        )

    if st.button("🚀 Analyze Sentiment", type="primary", use_container_width=True):
        if not keyword:
            st.warning("Please enter a keyword.")
            return

        # Rate limiting check
        now = time.time()
        last_time = st.session_state.get("last_request_time", 0)
        request_count = st.session_state.get("request_count", 0)

        time_since_last = now - last_time
        if time_since_last < COOLDOWN_SECONDS and request_count >= max_requests and max_requests > 0:
            remaining = int((COOLDOWN_SECONDS - time_since_last) / 60) + 1
            st.warning(f"⚠️ You've used all {max_requests} requests. Wait ~{remaining} minutes.")
            return

        # Fetch tweets
        with st.spinner("🔍 Scanning Twitter for latest conversations..."):
            try:
                tweets = get_tweets(keyword, max_results=tweet_limit, bearer_tokens=bearer_tokens)
            except Exception as e:
                st.error(f"❌ Error fetching tweets: {e}")
                tweets = []

        if not tweets:
            st.info("📭 No tweets found for that keyword. Try a different search term.")
            return

        # Process data
        df = save_to_csv(tweets, f"{keyword}_tweets.csv")

        # Update request count
        st.session_state["request_count"] = st.session_state.get("request_count", 0) + 1
        if st.session_state["request_count"] >= max_requests and max_requests > 0:
            st.session_state["last_request_time"] = time.time()
            st.info("🎯 All tokens used — cooldown started.")

        # Show success
        st.success(f"✅ Successfully analyzed {len(df)} tweets for **{keyword}**")
        
        # 1. SENTIMENT METRICS - Top section
        st.markdown("---")
        st.subheader("📈 Sentiment Overview")
        show_sentiment_metrics(df)
        
        # 2. VISUAL CHARTS - Middle section
        st.markdown("---")
        st.subheader("📊 Sentiment Visualization")
        
        fig_pie, fig_bar = create_attractive_sentiment_chart(df, keyword)
        
        # Display charts in tabs
        tab1, tab2 = st.tabs(["🎯 Pie Chart", "📊 Bar Chart"])
        
        with tab1:
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with tab2:
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # 3. TWEET DATA - Bottom section  
        st.markdown("---")
        st.subheader("💬 Recent Tweets Analysis")
        
        # Show sample tweets with sentiment colors
        for idx, row in df.head(10).iterrows():
            sentiment_color = {
                'Positive': '🟢',
                'Negative': '🔴', 
                'Neutral': '🟡'
            }.get(row['sentiment'], '⚪')
            
            with st.container():
                col1, col2 = st.columns([1, 20])
                with col1:
                    st.write(f"**{sentiment_color}**")
                with col2:
                    st.write(f"{row['text']}")
                    st.caption(f"Sentiment: **{row['sentiment']}**")
                st.divider()
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download Full Analysis CSV", 
            data=csv, 
            file_name=f"{keyword}_sentiment_analysis.csv", 
            mime="text/csv",
            use_container_width=True
        )

    # Sidebar status
    if st.session_state.get("request_count", 0) < max_requests:
        st.sidebar.success(f"📊 Requests available: {max_requests - st.session_state.get('request_count', 0)}/{max_requests}")
    else:
        now = time.time()
        last_time = st.session_state.get("last_request_time", 0)
        if now - last_time < COOLDOWN_SECONDS:
            remaining = int((COOLDOWN_SECONDS - (now - last_time)) / 60) + 1
            st.sidebar.warning(f"⏰ Cooldown: {remaining} minutes left")
        else:
            st.session_state["request_count"] = 0
            st.sidebar.success("✅ Cooldown over! Requests refreshed.")