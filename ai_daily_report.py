import requests
import feedparser
import pandas as pd
from database import get_keywords

def get_sources():
    return [
        {
            "name": "NYTimes Technology",
            "url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
            "type": "news"
        },
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed/",
            "type": "news"
        },
        {
            "name": "Google News AI",
            "url": "https://news.google.com/rss/search?q=AI",
            "type": "news"
        },
        {
            "name": "Google News NVIDIA",
            "url": "https://news.google.com/rss/search?q=NVIDIA",
            "type": "news"
        },
        {
            "name": "Google News Tesla",
            "url": "https://news.google.com/rss/search?q=Tesla",
            "type": "news"
        },
        {
            "name": "Google News OpenAI",
            "url": "https://news.google.com/rss/search?q=OpenAI",
            "type": "news"
        },
        {
            "name": "Hacker News",
            "url": "https://hnrss.org/frontpage",
            "type": "community"
        },
        {
            "name": "Reddit AI",
            "url": "https://www.reddit.com/r/artificial/.rss",
            "type": "community"
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com/rss/index.xml",
            "type": "news"
        },
        {
            "name": "Ars Technica",
            "url": "https://feeds.arstechnica.com/arstechnica/index",
            "type": "news"
        },
        {
            "name": "MIT News",
            "url": "https://news.mit.edu/rss/feed",
            "type": "news"
        },
        {
            "name": "MIT Technology Review",
            "url": "https://www.technologyreview.com/feed/",
            "type": "news"
        },
        {
            "name": "NVIDIA News",
            "url": "https://nvidianews.nvidia.com/releases.xml",
            "type": "official"
        },
        {
            "name": "OpenAI News",
            "url": "https://openai.com/news/rss.xml",
            "type": "official"
        },
        {
            "name": "Google AI Blog",
            "url": "https://blog.google/technology/ai/rss/",
            "type": "official"
        },
        {
            "name": "Microsoft AI Blog",
            "url": "https://blogs.microsoft.com/ai/feed/",
            "type": "official"
        },
        {
            "name": "Reddit Machine Learning",
            "url": "https://www.reddit.com/r/MachineLearning/.rss",
            "type": "community"
        },
        {
            "name": "Reddit LocalLLaMA",
            "url": "https://www.reddit.com/r/LocalLLaMA/.rss",
            "type": "community"
        },
        {
            "name": "Reddit Artificial Intelligence",
            "url": "https://www.reddit.com/r/ArtificialInteligence/.rss",
            "type": "community"
        }
            ]


def collect_all_articles(sources):
    all_articles = []

    for source in sources:
        response = requests.get(source["url"])
        feed = feedparser.parse(response.content)

        for entry in feed.entries:
            all_articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": source["name"],
                "source_type": source["type"]
            })

    return all_articles


def filter_articles(all_articles, keywords):
    filtered_articles = []

    for article in all_articles:
        title_lower = article["title"].lower()

        matched_keywords = []

        for keyword in keywords:
            if keyword in title_lower:
                matched_keywords.append(keyword)

        if matched_keywords:
            filtered_articles.append({
                "title": article["title"],
                "link": article["link"],
                "published": article["published"],
                "source": article["source"],
                "source_type": article["source_type"],
                "keywords": ", ".join(matched_keywords)
            })

    return filtered_articles

def collect_articles():
    sources = get_sources()
    keywords = get_keywords()

    all_articles = collect_all_articles(sources)
    filtered_articles = filter_articles(all_articles, keywords)

    print("total articles collected:", len(all_articles))
    print("matched articles:", len(filtered_articles))

    df = pd.DataFrame(filtered_articles)
    print(df)
    df.to_csv("ai_news.csv", index=False)

    return filtered_articles, keywords