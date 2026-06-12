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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS executive_briefings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_time TEXT,
        briefing TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS keyword_groups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT UNIQUE,
        active INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS group_keywords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER,
        keyword TEXT,
        active INTEGER DEFAULT 1,
        UNIQUE(group_id, keyword),
        FOREIGN KEY(group_id) REFERENCES keyword_groups(id)
    )
    """)

    conn.commit()
    conn.close()


def add_keyword(keyword):

    keyword = keyword.strip().lower()

    if not keyword:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT keyword
    FROM keywords
    WHERE LOWER(keyword) = LOWER(?)
    """, (keyword,))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
        UPDATE keywords
        SET active = 1
        WHERE LOWER(keyword) = LOWER(?)
        """, (keyword,))
    else:
        cursor.execute("""
        INSERT INTO keywords(keyword, active)
        VALUES(?, 1)
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


def remove_keyword(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM keywords
    WHERE keyword = ?
    """, (keyword,))

    cursor.execute("""
    DELETE FROM search_runs
    WHERE keyword = ?
    """, (keyword,))

    cursor.execute("""
    DELETE FROM articles
    WHERE keyword = ?
    """, (keyword,))

    cursor.execute("""
    DELETE FROM ai_insights
    WHERE keyword = ?
    """, (keyword,))

    cursor.execute("""
    DELETE FROM group_keywords
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


def save_executive_briefing(briefing):

    conn = get_connection()
    cursor = conn.cursor()

    run_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    INSERT INTO executive_briefings(
        run_time,
        briefing
    )
    VALUES (?, ?)
    """, (
        run_time,
        briefing
    ))

    conn.commit()
    conn.close()


def get_latest_executive_briefing():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        run_time,
        briefing
    FROM executive_briefings
    ORDER BY run_time DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    return row


def add_keyword_group(group_name):

    group_name = group_name.strip()

    if len(group_name) == 0:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM keyword_groups
    WHERE group_name = ?
    """, (group_name,))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
        UPDATE keyword_groups
        SET active = 1
        WHERE group_name = ?
        """, (group_name,))
    else:
        cursor.execute("""
        INSERT INTO keyword_groups(
            group_name,
            active
        )
        VALUES(?, 1)
        """, (group_name,))

    conn.commit()
    conn.close()


def get_keyword_groups():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        group_name,
        active
    FROM keyword_groups
    ORDER BY group_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def add_keyword_to_group(group_id, keyword):

    keyword = keyword.strip().lower()

    if len(keyword) == 0:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO group_keywords(
        group_id,
        keyword,
        active
    )
    VALUES(?, ?, 1)
    """, (
        group_id,
        keyword
    ))

    conn.commit()
    conn.close()


def get_keywords_by_group(group_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        keyword,
        active
    FROM group_keywords
    WHERE group_id = ?
    ORDER BY keyword
    """, (group_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows

def deactivate_keyword_group(group_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE keyword_groups
    SET active = 0
    WHERE id = ?
    """, (group_id,))

    conn.commit()
    conn.close()


def activate_keyword_group(group_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE keyword_groups
    SET active = 1
    WHERE id = ?
    """, (group_id,))

    conn.commit()
    conn.close()


def deactivate_group_keyword(group_id, keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE group_keywords
    SET active = 0
    WHERE group_id = ?
    AND keyword = ?
    """, (
        group_id,
        keyword
    ))

    conn.commit()
    conn.close()


def activate_group_keyword(
    group_id,
    keyword
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE group_keywords
    SET active = 1
    WHERE group_id = ?
    AND keyword = ?
    """, (
        group_id,
        keyword
    ))

    conn.commit()
    conn.close()


def remove_keyword_from_group(group_id, keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM group_keywords
    WHERE group_id = ?
    AND keyword = ?
    """, (
        group_id,
        keyword
    ))

    conn.commit()
    conn.close()

def remove_keyword_group(group_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM group_keywords
    WHERE group_id = ?
    """, (group_id,))

    cursor.execute("""
    DELETE FROM keyword_groups
    WHERE id = ?
    """, (group_id,))

    conn.commit()
    conn.close()


def get_history_center_data(keyword):

    history = get_search_history(keyword)
    trend_data = get_trend_data(keyword)
    articles = get_articles(keyword, limit=50)
    latest_insight = get_latest_ai_insight(keyword)

    return {
        "history": history,
        "trend_data": trend_data,
        "articles": articles,
        "latest_insight": latest_insight
    }


def get_active_group_keywords():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT
        group_keywords.keyword
    FROM group_keywords
    JOIN keyword_groups
    ON group_keywords.group_id = keyword_groups.id
    WHERE group_keywords.active = 1 AND keyword_groups.active = 1
    ORDER BY group_keywords.keyword
    """)

    rows = cursor.fetchall()

    conn.close()

    keywords = []
    for row in rows:
        keywords.append(row[0])

    return keywords