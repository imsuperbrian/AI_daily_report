from ai_daily_report import collect_articles
from article_processor import remove_duplicates, display_words_count
from ai_summary import summarize_articles
from ai_analyzer import analyze_market_sentiment, parse_ai_analysis, generate_keyword_insight
from database import create_tables, save_search_run, get_search_history, save_articles, save_ai_insight, get_trending_keywords


def main(api_key = None):
    """
    Run the complete AI Daily Report pipeline.

    Workflow:
    1. Collect articles from RSS sources.
    2. Filter articles by active keywords.
    3. Remove duplicate articles.
    4. Generate summary and trending words.
    5. Generate AI sentiment analysis.
    6. Save report to file.
    7. Save history and articles to the database.
    """

    # Ensure required database tables exist.
    create_tables()

    # Collect and filter articles.
    filtered_articles, keywords = collect_articles()

    # Remove duplicate headlines.
    cleaned_articles = remove_duplicates(filtered_articles)

    # Generate article summary.
    summary = summarize_articles(cleaned_articles, keywords)

    # Generate trending words report.
    trending_words = display_words_count(cleaned_articles, keywords)

    report = summary

    report += "\nTrending Words:\n"
    report += trending_words

    # Generate AI sentiment analysis.
    try:

        ai_analysis = analyze_market_sentiment(cleaned_articles, api_key)

    except Exception as e:

        ai_analysis = ("AI analysis skipped: " + str(e))

    sentiment_label, summary_text = (parse_ai_analysis(ai_analysis))

    report += "\nAI Market Sentiment Analysis:\n"
    report += ai_analysis + "\n"

    print(report)

    # Save report to markdown file.
    with open("daily_report.md", "w" ,encoding="utf-8") as file:

        file.write("# AI Daily Report\n\n")
        file.write(report)

    # Save keyword-specific history and articles.
    for keyword in keywords:

        keyword_articles = []

        # Find articles associated with the current keyword.
        for article in cleaned_articles:

            article_keywords = (article["keywords"].lower())

            if keyword.lower() in article_keywords:
                keyword_articles.append(article)

        # Save trend history.
        save_search_run(keyword, len(keyword_articles), sentiment_label, summary_text)

        print("Saving articles for:", keyword)
        print("Article count:", len(keyword_articles))

        # Save article details.
        save_articles(keyword, keyword_articles)

        # Generate and save AI insight.
        insight = generate_keyword_insight(keyword, keyword_articles, api_key)

        save_ai_insight(keyword, insight)

        report += f"\n\n## AI Insight for {keyword}\n"
        report += insight

    print(get_search_history("nvidia"))

    print("History saved!")

if __name__ == "__main__":
    main()