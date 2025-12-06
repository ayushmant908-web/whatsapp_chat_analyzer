import streamlit as st
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

import preprocessor
import helper


# ------------------------------ SIDEBAR TITLE ------------------------------
st.sidebar.title("Whatsapp Chat Analyzer")

# ------------------------------ FILE UPLOADER ------------------------------
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    file_name = uploaded_file.name.lower()

    # -------------------------- LOAD FILE --------------------------
    if file_name.endswith(".txt"):
        data = uploaded_file.getvalue().decode("utf-8")
        df = preprocessor.preprocess_txt(data)

    elif file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    else:
        st.error("Unsupported file type!")
        st.stop()

    # -------------------------- CLEAN COLUMNS --------------------------
    df.columns = df.columns.str.lower().str.strip()

    # -------------------------- SHOW DATAFRAME --------------------------
    st.subheader("Your DataFrame")
    st.dataframe(df)

    # -------------------------- USER LIST --------------------------
    user_list = df["user"].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")

    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox("Show analysis w.r.t", user_list)

    # -------------------------- ALL ANALYSIS INSIDE BUTTON --------------------------
    if st.sidebar.button("Show analysis"):

        # -------------------------------------------------------------------
        # BASIC STATS
        # -------------------------------------------------------------------
        num_msgs, words, media, links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.title(num_msgs)

        with col2:
            st.subheader("Total Words")
            st.title(words)

        with col3:
            st.subheader("Media Shared")
            st.title(media)

        with col4:
            st.subheader("Links Shared")
            st.title(links)

        # -------------------------------------------------------------------
        # MOST BUSY USERS
        # -------------------------------------------------------------------
        if selected_user == "overall":

            st.title("Most Busy Users")

            busy = helper.most_busy_users(df)

            colA, colB = st.columns(2)

            with colA:
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.bar(busy.index, busy.values, color="red")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with colB:
                st.subheader("User Message Count")
                st.dataframe(busy)

        # -------------------------------------------------------------------
        # MOST COMMON WORDS
        # -------------------------------------------------------------------
        st.title("Most Common Words")

        wc_df = helper.most_common_words(df, selected_user)
        colW1, colW2 = st.columns(2)

        with colW1:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.barh(wc_df["word"], wc_df["count"], color="green")
            ax.invert_yaxis()
            st.pyplot(fig)

        with colW2:
            st.dataframe(wc_df)

        # -------------------------------------------------------------------
        # MOST COMMON EMOJIS
        # -------------------------------------------------------------------
        st.title("Most Common Emojis")

        emoji_df = helper.most_common_emojis(df, selected_user)
        colE1, colE2 = st.columns(2)

        with colE1:
            fig, ax = plt.subplots(figsize=(6, 8))
            ax.barh(emoji_df["emoji"], emoji_df["count"], color="orange")
            ax.invert_yaxis()
            st.pyplot(fig)

        with colE2:
            st.dataframe(emoji_df)

        # -------------------------------------------------------------------
        # WEEKLY ACTIVITY HEATMAP
        # -------------------------------------------------------------------
        st.title("Weekly Activity Heatmap")

        heatmap_data = helper.activity_heatmap(df, selected_user)

        if heatmap_data is not None:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(heatmap_data, cmap="Blues", linewidths=.5, ax=ax)
            st.pyplot(fig)

        # -------------------------------------------------------------------
        # MONTHLY TIMELINE
        # -------------------------------------------------------------------
        st.title("Monthly Timeline")

        monthly_df = helper.monthly_timeline(df, selected_user)
        if monthly_df is not None:
            colMT1, colMT2 = st.columns(2)

            with colMT1:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(monthly_df["month_year"], monthly_df["count"],
                        marker="o", color="purple")
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with colMT2:
                st.dataframe(monthly_df)

        # -------------------------------------------------------------------
        # DAILY TIMELINE
        # -------------------------------------------------------------------
        st.title("Daily Timeline")

        daily_df = helper.daily_timeline(df, selected_user)
        if daily_df is not None:
            colDT1, colDT2 = st.columns(2)

            with colDT1:
                fig, ax = plt.subplots(figsize=(12, 5))
                ax.plot(daily_df["only_date"], daily_df["count"],
                        marker="o", color="blue")
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with colDT2:
                st.dataframe(daily_df)

        # -------------------------------------------------------------------
        # WEEKLY TIMELINE
        # -------------------------------------------------------------------
        st.title("Weekly Timeline")

        weekly_df = helper.weekly_timeline(df, selected_user)
        if weekly_df is not None:
            colWT1, colWT2 = st.columns(2)

            with colWT1:
                fig, ax = plt.subplots(figsize=(12, 5))
                ax.plot(weekly_df["year_week"], weekly_df["count"],
                        marker="o", color="brown")
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with colWT2:
                st.dataframe(weekly_df)

        # -------------------------------------------------------------------
        # SENTIMENT ANALYSIS
        # -------------------------------------------------------------------
        st.title("Sentiment Analysis")

        sentiment_df, sentiment_summary = helper.sentiment_analysis(df, selected_user)

        colS1, colS2 = st.columns(2)

        with colS1:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                sentiment_summary["count"],
                labels=sentiment_summary["sentiment"],
                autopct="%1.1f%%",
                colors=["green", "red", "yellow"]
            )
            plt.title("Sentiment Distribution")
            st.pyplot(fig)

        with colS2:
            st.subheader("Sentiment Summary")
            st.dataframe(sentiment_summary)

        st.subheader("Detailed Sentiment Data")
        st.dataframe(sentiment_df[["date", "user", "message",
                                   "sentiment_score", "sentiment_category"]])

        # -------------------------------------------------------------------
        # LEAST ACTIVE USERS
        # -------------------------------------------------------------------
        st.title("Least Active Users")

        least = helper.least_active_users(df)

        colL1, colL2 = st.columns(2)

        with colL1:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(least.index, least.values, color="black")
            plt.xticks(rotation=45)
            plt.title("Least Active Users")
            st.pyplot(fig)

        with colL2:
            st.subheader("Least Active User Count")
            st.dataframe(least)

        # -------------------------------------------------------------------
        # MOST BUSY MONTH
        # -------------------------------------------------------------------
        st.title("Most Busy Month (Month Ranking)")

        busy_month_df = helper.most_busy_month(df, selected_user)

        if busy_month_df is not None and not busy_month_df.empty:

            colMB1, colMB2 = st.columns(2)

            with colMB1:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(busy_month_df["month"], busy_month_df["count"], color="purple")
                plt.xticks(rotation=45)
                plt.title("Messages Per Month")
                st.pyplot(fig)

            with colMB2:
                st.subheader("Month Ranking (Highest to Lowest)")
                st.dataframe(busy_month_df)

        else:
            st.write("Month data not available.")


















