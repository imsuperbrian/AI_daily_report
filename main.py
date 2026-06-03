from ai_daily_report import collect_articles
from ai_summary import summarize_articles
from article_processor import remove_duplicates, display_words_count
from ai_analyzer import analyze_market_sentiment, parse_ai_analysis
from database import create_tables, save_search_run, get_search_history


def main():

    create_tables()

    filtered_articles, keywords = collect_articles()

    cleaned_articles = remove_duplicates(filtered_articles)

    summary = summarize_articles(
        cleaned_articles,
        keywords
    )

    trending_words = display_words_count(
        cleaned_articles,
        keywords
    )

    report = summary

    report += "\nTrending Words:\n"
    report += trending_words

    try:
        ai_analysis = analyze_market_sentiment(
            cleaned_articles
        )

    except Exception as e:
        ai_analysis = ("AI analysis skipped: " + str(e))

    sentiment_label, summary_text = parse_ai_analysis(
        ai_analysis
    )

    report += "\nAI Market Sentiment Analysis:\n"
    report += ai_analysis + "\n"

    print(report)

    with open("daily_report.md", "w", encoding="utf-8") as file:
        file.write("# AI Daily Report\n\n")
        file.write(report)


    for keyword in keywords:
        save_search_run(keyword, len(cleaned_articles), sentiment_label, summary_text)

    print(get_search_history("nvidia"))
    print("History saved!")


if __name__ == "__main__":
    main()