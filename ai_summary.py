def source_count(filtered_articles):
    sources = {}
    for article in filtered_articles:
        source = article["source"]
        if source in sources:
            sources[source] += 1
        else:
            sources[source] = 1

    return sources

def summarize_articles(filtered_articles, keywords):
    
    categories = categorize_sources(filtered_articles)
    article_found = len(filtered_articles)
    sources = source_count(filtered_articles)
    headlines = top_headlines(filtered_articles)

    keywords_text = ", ".join(keywords)

    summary = f"Today, we found {article_found} articles related to {keywords_text}.\n\n"
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
    headlines = []
    for article in filtered_articles:
        headlines.append(article["title"])
    return headlines[:5]

def categorize_sources(filtered_articles):
    news = 0
    community = 0
    official = 0

    for article in filtered_articles:
        source_type = article["source_type"]

        if source_type == "news":
            news += 1
        elif source_type == "community":
            community += 1
        elif source_type == "official":
            official += 1

    return {
        "news": news,
        "official": official,
        "community": community
    }
