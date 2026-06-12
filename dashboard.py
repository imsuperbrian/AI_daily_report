"""
AI Daily Report Dashboard

Streamlit dashboard for keyword management, AI news analysis,
history tracking, article browsing, and trend visualization.
"""

import streamlit as st
import pandas as pd
from database import (
    create_tables,
    get_keywords,
    get_search_history,
    get_articles,
    get_article_keywords,
    get_trend_data,
    get_dashboard_stats,
    get_source_distribution,
    get_trending_keywords,
    get_trend_keywords,
    get_latest_ai_insight,
    get_latest_executive_briefing,
    add_keyword_group,
    get_keyword_groups,
    add_keyword_to_group,
    get_keywords_by_group,
    activate_group_keyword,
    deactivate_group_keyword,
    activate_keyword_group,
    deactivate_keyword_group,
    remove_keyword_from_group,
    remove_keyword_group,
    get_history_center_data
    )

from main import main as run_analysis


def extract_section(text, section_title):
    lines = text.split("\n")

    collecting = False
    section_lines = []

    section_titles = ["Top Opportunity", "Top Threat", "Fastest Growing Topic", "Regional Trend", "Recommended Actions"]

    for line in lines:
        clean_line = line.strip()

        if section_title in clean_line:
            collecting = True
            continue

        if collecting:
            for title in section_titles:
                if(title != section_title and title in clean_line):
                    return "\n".join(section_lines)
                
            section_lines.append(line)

    return "\n".join(section_lines)



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

st.sidebar.subheader("API Settings")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password"
)

page = st.sidebar.radio(
    "Choose a page",
    [
        "Executive Briefing",
        "Overview",
        "Keywords",
        "Run Analysis",
        "History",
        "Keyword Intelligence"

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



elif page == "Executive Briefing":

    st.header("Executive Briefing")

    result = get_latest_executive_briefing()

    if result:
        run_time, briefing = result

        st.caption(f"Generated at: {run_time}")
        st.markdown(briefing)

    else:
        st.info(
            "No executive briefing found. Please run analysis first."
        )


elif page == "Keywords":

    st.header("Keyword Groups")

    st.subheader("Create New Group")

    new_group = st.text_input("Group name")

    if st.button("Add Group"):
        if len(new_group.strip()) != 0:
            add_keyword_group(new_group.strip())
            st.success("Group Added: " + new_group)
            st.rerun()
        else:
            st.warning("Group name cannot be empty.")

    st.divider()

    groups = get_keyword_groups()

    if len(groups) == 0:
        st.info("No groups yet. Create a group first.")

    else:
        group_names = []

        for i in range(len(groups)):

            group_id = groups[i][0]
            group_name = groups[i][1]
            group_active = groups[i][2]

            if group_active == 1:
                group_names.append(f"🟢 {group_name}")
            else:
                group_names.append(f"🔴 {group_name}")

        selected_group = st.selectbox("Choose a group", group_names)

        selected_group_id = None
        selected_group_name = None
        selected_group_active = None

        for i in range(len(groups)):

            group_id = groups[i][0]
            group_name = groups[i][1]
            group_active = groups[i][2]

            if group_active == 1:
                display_name = f"🟢 {group_name}"
            else:
                display_name = f"🔴 {group_name}"

            if display_name == selected_group:
                selected_group_id = group_id
                selected_group_name = group_name
                selected_group_active = group_active

        st.subheader("Group: " + selected_group_name)

        col1, col2 = st.columns(2)

        with col1:

            if selected_group_active == 1:
                if st.button("Deactivate Group", key=f"deactivate_group_{selected_group_id}"):
                    deactivate_keyword_group(selected_group_id)
                    st.rerun()

            else:
                if st.button("Activate Group", key=f"activate_group_{selected_group_id}"):
                    activate_keyword_group(selected_group_id)
                    st.rerun()

        with col2:

            if st.checkbox("Delete Group", key=f"confirm_group_delete_{selected_group_id}"):

                if st.button("Confirm", key=f"delete_group_{selected_group_id}"):
                    remove_keyword_group(selected_group_id)

                    st.success(f"Deleted group: {selected_group_name}")

                    st.rerun()

        st.divider()

        new_keyword = st.text_input("Add keyword to this group")

        if st.button("Add Keyword to Group"):
            if len(new_keyword.strip()) != 0:
                add_keyword_to_group(selected_group_id, new_keyword.strip())
                st.success(f"Added keyword: {new_keyword}")
                st.rerun()

            else:
                st.warning("Keyword cannot be empty.")

        st.divider()

        st.subheader("Keywords in this group")

        group_keywords = get_keywords_by_group(selected_group_id)

        if not group_keywords:
            st.info("No keywords in this group yet.")

        else:
            for i in range(len(group_keywords)):

                keyword = group_keywords[i][0]
                active = group_keywords[i][1]

                col1, col2, col3 = st.columns([4, 1, 1])

                with col1:
                    if active == 1:
                        st.write(f"🟢 {keyword}")
                    else:
                        st.write(f"🔴 {keyword}")

                with col2:
                    if active == 1:
                        if st.button("Deactivate",key=f"deactivate_keyword_{selected_group_id}_{keyword}_{i}"):
                            deactivate_group_keyword(selected_group_id, keyword)
                            st.rerun()

                    else:
                        if st.button("Activate", key=f"activate_keyword_{selected_group_id}_{keyword}_{i}"):
                            activate_group_keyword(selected_group_id, keyword)
                            st.rerun()

                with col3:
                    if st.button("Remove", key=f"remove_keyword_{selected_group_id}_{keyword}_{i}"):
                        remove_keyword_from_group(selected_group_id, keyword)
                        st.rerun()


elif page == "Run Analysis":

    # Run full analysis pipeline.
    st.header("Run AI Daily Report")

    st.write("This will run analysis using all active keywords in the database.")

    if st.button("Run Analysis"):

        if not api_key:
            st.error("Please enter your OpenAI API key first.")

        else:
            with st.spinner("Running analysis..."):
                run_analysis(api_key)

            st.success("Analysis completed.")

        # Display latest generated report.
        try:
            with open("daily_report.md", "r", encoding="utf-8") as file:
                report = file.read()

            st.markdown(report)

        except FileNotFoundError:
            st.warning("No report file found.")


elif page == "History":

    st.header("History Center")

    keywords = get_trend_keywords()

    if not keywords:
        st.info("No history data available.")

    else:
        selected_keyword = st.selectbox(
            "Choose keyword",
            keywords
        )

        data = get_history_center_data(
            selected_keyword
        )

        history = data["history"]
        trend_data = data["trend_data"]
        articles = data["articles"]
        latest_insight = data["latest_insight"]

        st.subheader(f"History for {selected_keyword}")

        if history:

            for i in range(len(history)):

                run_time = history[i][0]
                article_count = history[i][1]
                sentiment = history[i][2]
                summary = history[i][3]

                with st.expander(
                    f"{run_time} | {article_count} articles | {sentiment}"
                ):

                    st.subheader("Summary")
                    st.write(summary)

                    st.subheader("Trend")

                    if trend_data:
                        df_trend = pd.DataFrame(
                            trend_data,
                            columns=["Time", "Article Count"]
                        )

                        df_trend["Time"] = pd.to_datetime(
                            df_trend["Time"]
                        )

                        df_trend = df_trend.sort_values("Time")

                        st.line_chart(
                            df_trend.set_index("Time")["Article Count"]
                        )

                        st.dataframe(df_trend)

                    else:
                        st.info("No trend data available.")

                    st.subheader("Articles")

                    if articles:
                        for article in articles:
                            title = article[0]
                            source = article[1]
                            published = article[2]
                            link = article[3]

                            st.write(f"**{title}**")
                            st.caption(f"{source} | {published}")
                            st.link_button("Open Article", link)
                            st.divider()
                    else:
                        st.info("No articles found.")

                    st.subheader("Keyword Intelligence")

                    if latest_insight:
                        insight_time = latest_insight[0]
                        insight = latest_insight[1]

                        st.caption(f"Generated at: {insight_time}")
                        st.markdown(insight)
                    else:
                        st.info("No keyword intelligence found.")

        else:
            st.info("No history found for this keyword.")


# elif page == "Articles":

#     # Article browsing page.
#     st.header("Articles")

#     keywords = get_article_keywords()

#     if not keywords:
#         st.info("No articles available.")
#     else:
#         selected_keyword = st.selectbox(
#             "Choose keyword",
#             keywords
#         )

#         articles = get_articles(selected_keyword)

#         st.write("Articles Found:", len(articles))

#         if articles:
#             # Display stored articles.
#             for article in articles:
#                 title = article[0]
#                 source = article[1]
#                 published = article[2]
#                 link = article[3]

#                 st.subheader(title)
#                 st.write(f"{source} | {published}")
#                 st.link_button("Open Article", link)
#                 st.divider()

#         else:
#             st.info("No articles found.")


# elif page == "Trend":

#     # Article count trend page.
#     st.header("Trend Analytics")

#     keywords = get_trend_keywords()

#     if not keywords:
#         st.info("No trend data available.")
#     else:
#         selected_keyword = st.selectbox(
#             "Choose keyword",
#             keywords
#         )

#         trend_data = get_trend_data(selected_keyword)

#         if trend_data:

#             df = pd.DataFrame(
#                 trend_data,
#                 columns=["Time", "Article Count"]
#             )

#             # Convert time strings into datetime objects.
#             df["Time"] = pd.to_datetime(df["Time"])

#             df = df.sort_values("Time")

#             latest_count = df["Article Count"].iloc[-1]

#             # Compare latest run with previous run.
#             if len(df) >= 2:
#                 previous_count = df["Article Count"].iloc[-2]
#                 change = latest_count - previous_count
#             else:
#                 change = 0

#             st.metric(
#                 "Latest Article Count",
#                 latest_count,
#                 change
#             )

#             # Line chart for article count over time.
#             st.line_chart(
#                 df.set_index("Time")["Article Count"]
#             )

#             # Raw data for verification.
#             st.subheader("Raw Trend Data")
#             st.dataframe(df)

#         else:
#             st.info("No trend data found for this keyword.")


elif page == "Keyword Intelligence":

    st.header("Keyword Intelligence")

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