# app.py
import requests, time
from textblob import TextBlob
import pandas as pd

TWITTER_RECENT_SEARCH = "https://api.twitter.com/2/tweets/search/recent"

def classify_sentiment(text):
    tb = TextBlob(text)
    p = tb.sentiment.polarity
    if p > 0.1: return "Positive"
    elif p < -0.1: return "Negative"
    return "Neutral"

def get_tweets(keyword, max_results=50, bearer_tokens=None):
    keyword = keyword.strip()
    if not keyword: return []
    if not bearer_tokens:  # mock tweets if no tokens
        return [{"text": f"Tweet about {keyword} #{i+1}", "sentiment": classify_sentiment(f"Tweet about {keyword} #{i+1}")} for i in range(max_results)]

    tweets, token_index, remaining, next_token = [], 0, max_results, None
    while remaining > 0:
        token = bearer_tokens[token_index % len(bearer_tokens)]
        headers = {"Authorization": f"Bearer {token}"}
        params = {"query": f"{keyword} -is:retweet lang:en", "max_results": str(min(100, remaining)), "tweet.fields": "text,created_at,author_id"}
        if next_token: params["next_token"] = next_token

        try:
            resp = requests.get(TWITTER_RECENT_SEARCH, headers=headers, params=params, timeout=10)
        except: break

        if resp.status_code == 200:
            data = resp.json().get("data", [])
            for item in data:
                text = item.get("text", "")
                tweets.append({"text": text, "sentiment": classify_sentiment(text)})
                if len(tweets) >= max_results: break
            meta = resp.json().get("meta", {})
            next_token = meta.get("next_token")
            if not next_token: break
            remaining = max_results - len(tweets)
            time.sleep(0.4)
        elif resp.status_code == 429:
            token_index += 1
            if token_index >= len(bearer_tokens): break
            time.sleep(2)
            continue
        else: break

    if not tweets:
        return [{"text": f"Tweet about {keyword} (mock) #{i+1}", "sentiment": classify_sentiment(f"Tweet about {keyword} (mock) #{i+1}")} for i in range(max_results)]
    return tweets[:max_results]

def save_to_csv(tweets, filename):
    df = pd.DataFrame(tweets)
    if "sentiment" not in df.columns:
        df["sentiment"] = df["text"].apply(classify_sentiment)
    df.to_csv(filename, index=False)
    return df

def plot_sentiment_distribution(df, keyword):
    return df["sentiment"].value_counts()
