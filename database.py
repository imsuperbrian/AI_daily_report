import os
import sqlite3
from datetime import datetime


DB_PATH = "data/ai_daily_report.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_tables():

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

    conn.commit()
    conn.close()


def add_keyword(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO keywords(keyword)
    VALUES(?)
    """, (keyword,))

    conn.commit()
    conn.close()


def get_keywords():

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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE keywords
    SET active = 0
    WHERE keyword = ?
    """, (keyword,))

    conn.commit()
    conn.close()


def deactivate_keyword(keyword):

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

    conn = get_connection()
    cursor = conn.cursor()

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO search_runs(keyword, run_time, article_count, sentiment, summary)
    VALUES(?, ?, ?, ?, ?)
    """, (keyword, run_time, article_count, sentiment, summary))

    conn.commit()
    conn.close()


def get_search_history(keyword):

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


def get_articles(keyword):

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
    """, (keyword,))

    articles = cursor.fetchall()

    conn.close()

    return articles


def get_article_keywords():

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