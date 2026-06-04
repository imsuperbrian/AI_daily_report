import streamlit as st

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
        "History"
    ]
)

if page == "Keywords":

    st.header("Keyword Management")

    new_keyword = st.text_input("Add a new keyword")

    if st.button("Add Keyword"):
        if new_keyword.strip():
            add_keyword(new_keyword.strip().lower())
            st.success(f"Added keyword: {new_keyword}")

    st.subheader("Current Keywords")

    keywords = get_keywords()

    for keyword in keywords:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(keyword)

        with col2:
            if st.button("Delete", key=keyword):
                delete_keyword(keyword)
                st.success(f"Deleted: {keyword}")
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