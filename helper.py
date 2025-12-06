from urlextract import URLExtract
extract = URLExtract()

from collections import Counter
import pandas as pd
import emoji
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# ----------------------------------------------------------
# BASIC STATS
# ----------------------------------------------------------
def fetch_stats(selected_user, df):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    df = df.dropna(subset=["message"]).copy()
    df["message"] = df["message"].astype(str).str.lower()

    num_messages = df.shape[0]

    words = []
    for msg in df["message"]:
        words.extend(msg.split())

    media_keywords = [
        "media omitted", "image omitted", "video omitted",
        "sticker omitted", "audio omitted"
    ]

    num_media_messages = df["message"].apply(
        lambda x: any(k in x for k in media_keywords)
    ).sum()

    links = []
    for msg in df["message"]:
        links.extend(extract.find_urls(msg))

    return num_messages, len(words), num_media_messages, len(links)



# ----------------------------------------------------------
# MOST BUSY USERS
# ----------------------------------------------------------
def most_busy_users(df):

    df["message"] = df["message"].astype(str)
    df = df[~df["message"].str.lower().str.contains("omitted", na=False)]

    return df["user"].value_counts().head()



# ----------------------------------------------------------
# MOST COMMON WORDS
# ----------------------------------------------------------
def most_common_words(df, selected_user):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    df = df.dropna(subset=["message"]).copy()

    df["message"] = df["message"].astype(str).str.lower()

    df = df[~df["message"].str.contains("omitted", na=False)]

    words = []
    for msg in df["message"]:
        words.extend(msg.split())

    common = Counter(words).most_common(20)
    return pd.DataFrame(common, columns=["word", "count"])



# ----------------------------------------------------------
# MOST COMMON EMOJIS
# ----------------------------------------------------------
def most_common_emojis(df, selected_user):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    df["message"] = df["message"].astype(str)
    all_emoji = []

    for msg in df["message"]:
        for ch in msg:
            if ch in emoji.EMOJI_DATA:
                all_emoji.append(ch)

    emoji_count = Counter(all_emoji).most_common(20)
    return pd.DataFrame(emoji_count, columns=["emoji", "count"])



# ----------------------------------------------------------
# WEEKLY HEATMAP
# ----------------------------------------------------------
def activity_heatmap(df, selected_user):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    if "date" not in df.columns:
        return None

    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour

    pivot = df.pivot_table(
        index="day_name",
        columns="hour",
        values="message",
        aggfunc="count"
    ).fillna(0)

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return pivot.reindex(order)



# ----------------------------------------------------------
# MONTHLY TIMELINE
# ----------------------------------------------------------
def monthly_timeline(df, selected_user):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    if "date" not in df.columns:
        return None

    df["month_year"] = df["date"].dt.to_period("M").astype(str)

    timeline = df.groupby("month_year")["message"].count().reset_index()
    timeline.columns = ["month_year", "count"]

    return timeline



# ----------------------------------------------------------
# DAILY TIMELINE
# ----------------------------------------------------------
def daily_timeline(df, selected_user):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    df["only_date"] = df["date"].dt.date

    timeline = df.groupby("only_date")["message"].count().reset_index()
    timeline.columns = ["only_date", "count"]

    return timeline



# ----------------------------------------------------------
# WEEKLY TIMELINE
# ----------------------------------------------------------
def weekly_timeline(df, selected_user):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    df["week_number"] = df["date"].dt.isocalendar().week
    df["year"] = df["date"].dt.year
    df["year_week"] = df["year"].astype(str) + "-W" + df["week_number"].astype(str)

    timeline = df.groupby("year_week")["message"].count().reset_index()
    timeline.columns = ["year_week", "count"]

    return timeline



# ----------------------------------------------------------
# SENTIMENT ANALYSIS
# ----------------------------------------------------------
def sentiment_analysis(df, selected_user):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    df["message"] = df["message"].astype(str)

    analyzer = SentimentIntensityAnalyzer()

    scores = []
    labels = []

    for msg in df["message"]:
        s = analyzer.polarity_scores(msg)["compound"]
        scores.append(s)

        if s >= 0.05:
            labels.append("Positive")
        elif s <= -0.05:
            labels.append("Negative")
        else:
            labels.append("Neutral")

    df["sentiment_score"] = scores
    df["sentiment_category"] = labels

    summary = df["sentiment_category"].value_counts().reset_index()
    summary.columns = ["sentiment", "count"]

    return df, summary



# ----------------------------------------------------------
# LEAST ACTIVE USERS
# ----------------------------------------------------------
def least_active_users(df):

    df["message"] = df["message"].astype(str)
    df = df[~df["message"].str.contains("omitted", na=False)]

    return df["user"].value_counts().sort_values().head()



# ----------------------------------------------------------
# MOST BUSY MONTH
# ----------------------------------------------------------
def most_busy_month(df, selected_user):

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    df["month"] = df["date"].dt.month_name()

    m = df["month"].value_counts().reset_index()
    m.columns = ["month", "count"]

    return m
































