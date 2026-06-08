import streamlit as st
from database import get_article_keywords, reactivate_keyword, get_all_keywords, get_articles


from database import (
    create_tables,
    add_keyword,
    get_keywords,
    delete_keyword,
    get_search_history
)

from main import main as run_analysis


st.set_page_config(
    page_title="AI Daily Report",
    layout="wide"
)

create_tables()

st.title("AI Daily Report Dashboard")

st.sidebar.header("Menu")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Keywords",
        "Run Analysis",
        "History",
        "Articles"
    ]
)

if page == "Keywords":

    st.header("Keyword Management")

    new_keyword = st.text_input("Add a new keyword")

    if st.button("Add Keyword"):
        if new_keyword.strip():
            add_keyword(new_keyword.strip().lower())
            st.success(f"Added keyword: {new_keyword}")
            st.rerun()

    st.subheader("Current Keywords")

    keywords = get_all_keywords()

    for keyword, active in keywords:
        col1, col2 = st.columns([4, 1])

        with col1:
            if active == 1:
                st.write(f"🟢 {keyword}")
            else:
                st.write(f"🔴 {keyword}")

        with col2:
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

    st.header("Run AI Daily Report")

    st.write("This will run analysis using all active keywords in the database.")

    if st.button("Run Analysis"):
        with st.spinner("Running analysis..."):
            run_analysis()

        st.success("Analysis completed.")

        try:
            with open("daily_report.md", "r", encoding="utf-8") as file:
                report = file.read()

            st.markdown(report)

        except FileNotFoundError:
            st.warning("No report file found.")


elif page == "History":

    st.header("Search History")

    keywords = get_keywords()

    selected_keyword = st.selectbox(
        "Choose keyword",
        keywords
    )

    if selected_keyword:
        history = get_search_history(selected_keyword)

        if history:
            st.subheader(f"History for {selected_keyword}")

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

    st.header("Articles")

    keywords = get_article_keywords()

    selected_keyword = st.selectbox(
        "Choose keyword",
        keywords
    )

    articles = get_articles(selected_keyword)

    st.write("Articles Found:", len(articles))

    if articles:
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