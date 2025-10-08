# twitter_sentiment.py
import streamlit as st
import time
from app import get_tweets, save_to_csv, plot_sentiment_distribution
from utils import save_sentiment_plot

COOLDOWN_SECONDS = 16 * 60  # 16 minutes

def show_page(company=None, bearer_tokens=None, max_requests=0):
    st.subheader("🐦 Public Sentiment Analysis")
    keyword = st.text_input("🔍 Enter keyword to analyze:", company or "")
    tweet_limit = st.slider("🔢 Number of tweets to fetch", 10, 100, 50)

    if st.button("🚀 Analyze Sentiment", type="primary"):
        if not keyword:
            st.warning("Please enter a keyword.")
            return

        now = time.time()
        last_time = st.session_state.get("last_request_time", 0)
        request_count = st.session_state.get("request_count", 0)

        time_since_last = now - last_time
        if time_since_last < COOLDOWN_SECONDS and request_count >= max_requests and max_requests > 0:
            remaining = int((COOLDOWN_SECONDS - time_since_last) / 60) + 1
            st.warning(f"⚠️ You've used all {max_requests} requests. Wait ~{remaining} minutes.")
            return

        with st.spinner("📡 Fetching tweets..."):
            try:
                tweets = get_tweets(keyword, max_results=tweet_limit, bearer_tokens=bearer_tokens)
            except Exception as e:
                st.error(f"Error fetching tweets: {e}")
                tweets = []  # no fallback, force error if tokens fail

        if not tweets:
            st.info("No tweets found for that keyword.")
            return

        df = save_to_csv(tweets, f"{keyword}_tweets.csv")

        st.session_state["request_count"] = st.session_state.get("request_count", 0) + 1
        if st.session_state["request_count"] >= max_requests and max_requests > 0:
            st.session_state["last_request_time"] = time.time()
            st.info("🎯 All tokens used — cooldown started.")

        st.success(f"✅ Analyzed {len(df)} tweets.")

        st.subheader("📊 Sentiment Results")
        st.dataframe(df[["text", "sentiment"]], use_container_width=True)

        counts = df["sentiment"].value_counts()
        for s, c in counts.items():
            pct = (c / len(df)) * 100
            st.write(f"**{s}:** {c} tweets ({pct:.1f}%)")

        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV Report", data=csv, file_name=f"{keyword}_sentiment_analysis.csv", mime="text/csv")

        plot_counts = plot_sentiment_distribution(df, keyword)
        img_path = save_sentiment_plot(plot_counts, filename="sentiment_graph.png", title=f"Sentiment for {keyword}")
        st.image(img_path, caption="Sentiment Distribution", use_column_width=True)

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
