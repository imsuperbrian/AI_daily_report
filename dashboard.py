"""
AI Daily Report Dashboard

Streamlit dashboard for keyword management, AI news analysis,
history tracking, article browsing, and trend visualization.
"""

import streamlit as st
import pandas as pd
from database import (
    create_tables,
    add_keyword,
    get_keywords,
    get_all_keywords,
    delete_keyword,
    reactivate_keyword,
    get_search_history,
    get_articles,
    get_article_keywords,
    get_trend_data,
    get_dashboard_stats,
    get_source_distribution,
    get_trending_keywords,
    get_trend_keywords,
    get_latest_ai_insight
)

from main import main as run_analysis


st.set_page_config(
    page_title="AI Daily Report",
    layout="wide"
)

# Initialize database tables.
create_tables()

# Page title.
st.title("AI Daily Report Dashboard")

# Sidebar navigation.
st.sidebar.header("Menu")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Overview",
        "Keywords",
        "Run Analysis",
        "History",
        "Articles",
        "Trend",
        "AI Insights"

    ]
)


if page == "Overview":

    st.header("Overview")

    active_keywords, total_articles, total_runs, latest_run = (
        get_dashboard_stats()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Active Keywords", active_keywords)
    col2.metric("Total Articles", total_articles)
    col3.metric("Total Runs", total_runs)
    col4.metric("Latest Run", latest_run)

    st.divider()

    st.subheader("Top Hot Topics Today")

    trending = get_trending_keywords()

    if trending:

        df = pd.DataFrame(trending)

        df = df.rename(
            columns={
                "keyword": "Keyword",
                "hotness_score": "Hotness",
                "volume_score": "Volume",
                "momentum_score": "Momentum",
                "sentiment_score": "Sentiment",
                "difference": "Growth %",
                "latest": "Today",
                "previous": "Previous",
                "sentiment": "Sentiment Label"
            }
        )

        top3 = df.head(3)
        columns = st.columns(min(3, len(top3)))

        for i, col in enumerate(columns):
            with col:
                st.metric(
                    top3.iloc[i]["Keyword"],
                    f"{top3.iloc[i]['Hotness']:.1f}"
                )

        df_display = df.copy()

        df_display["Growth %"] = (
            df_display["Growth %"]
            .map(lambda x: f"{x:+.1f}%")
        )

        df_display = df_display[
            [
                "Keyword",
                "Hotness",
                "Volume",
                "Momentum",
                "Sentiment",
                "Sentiment Label",
                "Growth %",
                "Today",
                "Previous"
            ]
        ]

        st.dataframe(df_display)

        st.bar_chart(
            df.set_index("Keyword")["Hotness"]
        )

        st.caption(
            "Hotness = Volume Score + Momentum Score + Sentiment Score"
        )

    else:
        st.info("Not enough trend data yet.")

    st.divider()

    st.subheader("Source Distribution")

    source_data = get_source_distribution()

    if source_data:

        df_sources = pd.DataFrame(
            source_data,
            columns=["Source", "Count"]
        )

        st.bar_chart(
            df_sources.set_index("Source")
        )

        st.dataframe(df_sources)

    else:
        st.info("No source data yet.")


elif page == "Keywords":

    # Keyword management page.
    st.header("Keyword Management")

    # Add new keyword.
    new_keyword = st.text_input("Add a new keyword")

    if st.button("Add Keyword"):
        if new_keyword.strip():
            add_keyword(new_keyword.strip().lower())
            st.success(f"Added keyword: {new_keyword}")
            st.rerun()

    st.subheader("Current Keywords")

    # Display active and inactive keywords.
    keywords = get_all_keywords()

    for keyword, active in keywords:
        col1, col2 = st.columns([4, 1])

        with col1:
            if active == 1:
                st.write(f"🟢 {keyword}")
            else:
                st.write(f"🔴 {keyword}")

        with col2:
            # Soft delete / reactivate keyword.
            if active == 1:
                if st.button("Deactivate", key=f"deactivate_{keyword}"):
                    delete_keyword(keyword)
                    st.success(f"Deactivated: {keyword}")
                    st.rerun()
            else:
                if st.button("Reactivate", key=f"reactivate_{keyword}"):
                    reactivate_keyword(keyword)
                    st.success(f"Reactivated: {keyword}")
                    st.rerun()


elif page == "Run Analysis":

    # Run full analysis pipeline.
    st.header("Run AI Daily Report")

    st.write(
        "This will run analysis using all active keywords in the database."
    )

    if st.button("Run Analysis"):
        with st.spinner("Running analysis..."):
            run_analysis()

        st.success("Analysis completed.")

        # Display latest generated report.
        try:
            with open("daily_report.md", "r", encoding="utf-8") as file:
                report = file.read()

            st.markdown(report)

        except FileNotFoundError:
            st.warning("No report file found.")


elif page == "History":

    # Historical search results page.
    st.header("Search History")

    keywords = get_keywords()

    if not keywords:
        st.info("No keywords available.")
    else:
        selected_keyword = st.selectbox(
            "Choose keyword",
            keywords
        )

        history = get_search_history(selected_keyword)

        if history:
            st.subheader(f"History for {selected_keyword}")

            # Display historical analysis runs.
            for row in history:
                run_time = row[0]
                article_count = row[1]
                sentiment = row[2]

                st.write(
                    f"{run_time} | {article_count} articles | {sentiment}"
                )

        else:
            st.info("No history found for this keyword.")


elif page == "Articles":

    # Article browsing page.
    st.header("Articles")

    keywords = get_article_keywords()

    if not keywords:
        st.info("No articles available.")
    else:
        selected_keyword = st.selectbox(
            "Choose keyword",
            keywords
        )

        articles = get_articles(selected_keyword)

        st.write("Articles Found:", len(articles))

        if articles:
            # Display stored articles.
            for article in articles:
                title = article[0]
                source = article[1]
                published = article[2]
                link = article[3]

                st.subheader(title)
                st.write(f"{source} | {published}")
                st.link_button("Open Article", link)
                st.divider()

        else:
            st.info("No articles found.")


elif page == "Trend":

    # Article count trend page.
    st.header("Trend Analytics")

    keywords = get_trend_keywords()

    if not keywords:
        st.info("No trend data available.")
    else:
        selected_keyword = st.selectbox(
            "Choose keyword",
            keywords
        )

        trend_data = get_trend_data(selected_keyword)

        if trend_data:

            df = pd.DataFrame(
                trend_data,
                columns=["Time", "Article Count"]
            )

            # Convert time strings into datetime objects.
            df["Time"] = pd.to_datetime(df["Time"])

            df = df.sort_values("Time")

            latest_count = df["Article Count"].iloc[-1]

            # Compare latest run with previous run.
            if len(df) >= 2:
                previous_count = df["Article Count"].iloc[-2]
                change = latest_count - previous_count
            else:
                change = 0

            st.metric(
                "Latest Article Count",
                latest_count,
                change
            )

            # Line chart for article count over time.
            st.line_chart(
                df.set_index("Time")["Article Count"]
            )

            # Raw data for verification.
            st.subheader("Raw Trend Data")
            st.dataframe(df)

        else:
            st.info("No trend data found for this keyword.")


elif page == "AI Insights":

    st.header("AI Insights")

    keywords = get_article_keywords()

    if not keywords:
        st.info("No article data available.")
    else:
        selected_keyword = st.selectbox(
            "Choose keyword",
            keywords
        )

        result = get_latest_ai_insight(
            selected_keyword
        )

        if result:
            run_time = result[0]
            insight = result[1]

            st.caption(f"Generated at: {run_time}")
            st.markdown(insight)

        else:
            st.info(
                "No AI insight found. Please run analysis first."
            )