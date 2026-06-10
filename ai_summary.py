def source_count(filtered_articles):
    """
    Count how many articles come from each source.

    Args:
        filtered_articles:
            List of article dictionaries after keyword filtering.

    Returns:
        Dictionary where the key is source name and the value is article count.
    """

    sources = {}

    for article in filtered_articles:
        source = article["source"]

        if source in sources:
            sources[source] += 1
        else:
            sources[source] = 1

    return sources


def summarize_articles(filtered_articles, keywords):
    """
    Generate a basic text summary for the daily report.

    The summary includes:
    - Total matched article count
    - Top sources
    - Top headlines
    - Source category counts

    Args:
        filtered_articles:
            List of filtered article dictionaries.

        keywords:
            List of active keywords used in the search.

    Returns:
        A formatted text summary.
    """

    categories = categorize_sources(filtered_articles)
    article_found = len(filtered_articles)
    sources = source_count(filtered_articles)
    headlines = top_headlines(filtered_articles)

    keywords_text = ", ".join(keywords)

    summary = (
        f"Today, we found {article_found} "
        f"articles related to {keywords_text}.\n\n"
    )

    summary += "Top Sources:\n"

    for source, count in sources.items():
        summary += f"- {source}: {count} articles\n"

    summary += "\nTop Headlines:\n"

    i = 1

    for headline in headlines:
        summary += str(i) + ". " + headline + "\n"
        i += 1

    summary += "\nCategories:\n"

    for category, count in categories.items():
        summary += f"- {category.capitalize()}: {count} articles\n"

    return summary


def top_headlines(filtered_articles):
    """
    Return the first five article headlines.

    Args:
        filtered_articles:
            List of filtered article dictionaries.

    Returns:
        A list of up to five headline strings.
    """

    headlines = []

    for article in filtered_articles:
        headlines.append(article["title"])

    return headlines[:5]


def categorize_sources(filtered_articles):
    """
    Count articles by source type.

    Current supported categories:
    - news
    - official
    - community
    - finance

    Args:
        filtered_articles:
            List of filtered article dictionaries.

    Returns:
        Dictionary containing article counts by category.
    """

    news = 0
    community = 0
    official = 0
    finance = 0

    for article in filtered_articles:
        source_type = article["source_type"]

        if source_type == "news":
            news += 1
        elif source_type == "community":
            community += 1
        elif source_type == "official":
            official += 1
        elif source_type == "finance":
            finance += 1

    return {
        "news": news,
        "official": official,
        "community": community,
        "finance": finance
    }