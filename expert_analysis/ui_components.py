# expert_analysis/ui_components.py
import streamlit as st
from .news_service import format_time

def create_news_card(article, index):
    """Create individual news card with direct source links"""
    title = article.get('title', 'No title')
    source = article.get('source', {}).get('name', 'Unknown')
    published_at = format_time(article.get('publishedAt'))
    url = article.get('url', '#')
    
    # Create card
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write(f"{index + 1}. {title}")
            st.caption(f"📰 {source} • 🕒 {published_at}")
            
        with col2:
            # DIRECT SOURCE LINK BUTTON
            if url and url != '#':
                source_short = source[:10] + "..." if len(source) > 10 else source
                st.markdown(
                    f'<a href="{url}" target="_blank" style="text-decoration: none;">'
                    f'<button style="width:100%; padding: 0.4rem 0.2rem; background: #00d09c; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold;">'
                    f'📖 {source_short}</button></a>', 
                    unsafe_allow_html=True
                )
            else:
                st.button("🔗 No Link", key=f"nolink_{index}", use_container_width=True, disabled=True)
        
        st.divider()

def show_sentiment_summary(sentiment_data, company):
    """Show sentiment summary with pie chart"""
    st.header("📊 News Sentiment Analysis")
    
    if sentiment_data['total'] == 0:
        st.info("No news available for sentiment analysis")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total News", sentiment_data['total'])
    with col2:
        st.metric("Positive", sentiment_data['positive'])
    with col3:
        st.metric("Negative", sentiment_data['negative'])
    with col4:
        st.metric("Neutral", sentiment_data['neutral'])
    
    # Pie chart
    from .sentiment_analyzer import create_sentiment_piechart
    pie_chart = create_sentiment_piechart(sentiment_data)
    st.plotly_chart(pie_chart, use_container_width=True)
    
    # Overall Sentiment
    if sentiment_data['total'] > 0:
        sentiment_score = ((sentiment_data['positive'] - sentiment_data['negative']) / sentiment_data['total']) * 100
        sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
        
        st.metric("*Overall Sentiment*", f"{sentiment_score:.1f}% {sentiment_label}")