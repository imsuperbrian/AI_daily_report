import os
import sqlite3
from datetime import datetime


DB_PATH = "data/ai_daily_report.db"


def get_connection():
    """
    Create and return a SQLite database connection.

    The data folder is created automatically if it does not exist.
    """

    os.makedirs("data", exist_ok=True)

    return sqlite3.connect(DB_PATH)


def create_tables():
    """
    Create required database tables if they do not already exist.

    Tables:
    - keywords: Stores tracked keywords and active status.
    - search_runs: Stores analysis history.
    - articles: Stores collected articles.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS keywords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT UNIQUE,
        active INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_runs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        run_time TEXT,
        article_count INTEGER,
        sentiment TEXT,
        summary TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        title TEXT,
        source TEXT,
        source_type TEXT,
        published TEXT,
        link TEXT,
        run_time TEXT,
        UNIQUE(keyword, link)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_insights(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        run_time TEXT,
        insight TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_keyword(keyword):
    """
    Add a keyword to the database.

    If the keyword already exists, it will be ignored.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO keywords(keyword)
    VALUES(?)
    """, (keyword,))

    conn.commit()
    conn.close()


def get_keywords():
    """
    Get all active keywords.

    Returns:
        List of active keyword strings.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT keyword
    FROM keywords
    WHERE active = 1
    """)

    rows = cursor.fetchall()

    conn.close()

    keywords = []

    for row in rows:
        keywords.append(row[0])

    return keywords


def delete_keyword(keyword):
    """
    Soft delete a keyword by setting active to 0.

    The keyword remains in the database so historical data is preserved.
    """

    deactivate_keyword(keyword)


def deactivate_keyword(keyword):
    """
    Deactivate a keyword.

    Deactivated keywords are not used in future analysis runs.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE keywords
    SET active = 0
    WHERE keyword = ?
    """, (keyword,))

    conn.commit()
    conn.close()


def reactivate_keyword(keyword):
    """
    Reactivate a previously deactivated keyword.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE keywords
    SET active = 1
    WHERE keyword = ?
    """, (keyword,))

    conn.commit()
    conn.close()


def save_search_run(keyword, article_count, sentiment, summary):
    """
    Save one analysis run for a keyword.

    Args:
        keyword:
            Keyword used in the analysis.

        article_count:
            Number of matched articles for the keyword.

        sentiment:
            AI-generated sentiment label.

        summary:
            AI-generated summary text.
    """

    conn = get_connection()
    cursor = conn.cursor()

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO search_runs(
        keyword,
        run_time,
        article_count,
        sentiment,
        summary
    )
    VALUES(?, ?, ?, ?, ?)
    """, (
        keyword,
        run_time,
        article_count,
        sentiment,
        summary
    ))

    conn.commit()
    conn.close()


def get_search_history(keyword):
    """
    Get historical analysis results for a keyword.

    Returns:
        List of rows containing run time, article count, sentiment, and summary.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        run_time,
        article_count,
        sentiment,
        summary
    FROM search_runs
    WHERE keyword = ?
    ORDER BY run_time
    """, (keyword,))

    history = cursor.fetchall()

    conn.close()

    return history


def save_articles(keyword, articles):
    """
    Save matched articles for a keyword.

    Duplicate articles are ignored based on UNIQUE(keyword, link).
    """

    conn = get_connection()
    cursor = conn.cursor()

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for article in articles:
        cursor.execute("""
        INSERT OR IGNORE INTO articles(
            keyword,
            title,
            source,
            source_type,
            published,
            link,
            run_time
        )
        VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (
            keyword,
            article["title"],
            article["source"],
            article["source_type"],
            article["published"],
            article["link"],
            run_time
        ))

    conn.commit()
    conn.close()


def get_articles(keyword, limit=20):
    """
    Get stored articles for a keyword.

    Args:
        keyword:
            Keyword to query.

        limit:
            Maximum number of articles to return.

    Returns:
        List of article rows.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        title,
        source,
        published,
        link
    FROM articles
    WHERE keyword = ?
    ORDER BY published DESC
    LIMIT ?
    """, (keyword, limit))

    articles = cursor.fetchall()

    conn.close()

    return articles


def get_article_keywords():
    """
    Get keywords that have stored articles.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT keyword
    FROM articles
    ORDER BY keyword
    """)

    rows = cursor.fetchall()

    conn.close()

    keywords = []

    for row in rows:
        keywords.append(row[0])

    return keywords


def get_all_keywords():
    """
    Get all keywords, including active and inactive ones.

    Returns:
        List of tuples: (keyword, active)
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT keyword, active
    FROM keywords
    ORDER BY keyword
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_trend_keywords():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT keyword
    FROM search_runs
    ORDER BY keyword
    """)

    rows = cursor.fetchall()

    conn.close()

    keywords = []

    for row in rows:
        keywords.append(row[0])

    return keywords


def get_trend_data(keyword):
    """
    Get article count trend data for a keyword.

    Returns:
        List of rows containing run time and article count.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        run_time,
        article_count
    FROM search_runs
    WHERE keyword = ?
    ORDER BY run_time
    """, (keyword,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_trending_keywords(limit=10):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        keyword,
        run_time,
        article_count,
        sentiment
    FROM search_runs
    ORDER BY keyword, run_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    keyword_data = {}

    for keyword, run_time, article_count, sentiment in rows:

        if keyword not in keyword_data:
            keyword_data[keyword] = {
                "counts": [],
                "sentiment": sentiment
            }

        keyword_data[keyword]["counts"].append(article_count)

    total_count = []

    for keyword, data in keyword_data.items():

        counts = data["counts"]
        sentiment = data["sentiment"]

        if len(counts) < 2:
            continue

        latest = counts[0]
        previous = counts[1]

        if previous == 0:
            continue

        difference = ((latest - previous) / previous) * 100

        total_count.append({
            "keyword": keyword,
            "latest": latest,
            "previous": previous,
            "difference": round(difference, 1),
            "sentiment": sentiment
        })

    if not total_count:
        return []

    growth_values = []

    for item in total_count:
        growth_values.append(item["difference"])

    growth_values.sort()

    for item in total_count:

        if len(growth_values) == 1:
            item["momentum_score"] = 20
            continue

        rank = growth_values.index(item["difference"])

        percentile = rank / (len(growth_values) - 1)

        item["momentum_score"] = round(percentile * 40, 1)

    if not total_count:
        return []

    max_articles = max(item["latest"]for item in total_count)

    for item in total_count:
        item["volume_score"] = round(item["latest"] / max_articles * 40, 1)

    for item in total_count:

        sentiment = item["sentiment"]

        if sentiment == "Bullish":
            item["sentiment_score"] = 20

        elif sentiment == "Neutral":
            item["sentiment_score"] = 10

        else:
            item["sentiment_score"] = 0

        item["hotness_score"] = round(item["volume_score"] + item["momentum_score"]+ item["sentiment_score"], 1)

    total_count.sort(key=lambda item: item["hotness_score"], reverse=True)

    return total_count[:limit]
    



def get_dashboard_stats():
    """
    Get basic dashboard statistics.

    Returns:
        active_keywords:
            Number of active keywords.

        total_articles:
            Total number of stored articles.

        total_runs:
            Total number of analysis runs.

        latest_run:
            Most recent analysis run time.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM keywords
    WHERE active = 1
    """)
    active_keywords = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM articles
    """)
    total_articles = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM search_runs
    """)
    total_runs = cursor.fetchone()[0]

    cursor.execute("""
    SELECT run_time
    FROM search_runs
    ORDER BY run_time DESC
    LIMIT 1
    """)
    latest_run = cursor.fetchone()

    conn.close()

    if latest_run:
        latest_run = latest_run[0]
    else:
        latest_run = "No runs yet"

    return active_keywords, total_articles, total_runs, latest_run


def get_top_keywords(limit=10):
    """
    Get the latest keyword article counts.

    Args:
        limit:
            Maximum number of rows to return.

    Returns:
        List of keyword and article count rows.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        keyword,
        article_count
    FROM search_runs
    ORDER BY run_time DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_source_distribution(limit=10):
    """
    Get article count by source.

    Args:
        limit:
            Maximum number of sources to return.

    Returns:
        List of source and count rows.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        source,
        COUNT(*) as count
    FROM articles
    GROUP BY source
    ORDER BY count DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def save_ai_insight(keyword, insight):

    conn = get_connection()
    cursor = conn.cursor()

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO ai_insights(
        keyword,
        run_time,
        insight
    )
    VALUES(?, ?, ?)
    """, (
        keyword,
        run_time,
        insight
    ))

    conn.commit()
    conn.close()


def get_latest_ai_insight(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        run_time,
        insight
    FROM ai_insights
    WHERE keyword = ?
    ORDER BY run_time DESC
    LIMIT 1
    """, (keyword,))

    row = cursor.fetchone()

    conn.close()

    return row


def get_latest_insights():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        keyword,
        insight
    FROM ai_insights
    ORDER BY run_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows