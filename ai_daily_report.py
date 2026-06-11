import requests
import feedparser
import pandas as pd

from database import get_keywords


def get_sources():
    """
    Return a list of RSS sources used by the news collector.

    Each source contains:
    - name: Display name of the RSS source
    - url: RSS feed URL
    - type: Source category, such as news, official, finance, or community
    """

    return [
        # General technology news
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
            "name": "Wired",
            "url": "https://www.wired.com/feed/rss",
            "type": "news"
        },
        {
            "name": "VentureBeat",
            "url": "https://venturebeat.com/feed/",
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

        # Apple-related sources
        {
            "name": "Apple Newsroom",
            "url": "https://www.apple.com/newsroom/rss-feed.rss",
            "type": "official"
        },
        {
            "name": "9to5Mac",
            "url": "https://9to5mac.com/feed/",
            "type": "news"
        },
        {
            "name": "MacRumors",
            "url": "https://feeds.macrumors.com/MacRumors-All",
            "type": "news"
        },
        {
            "name": "AppleInsider",
            "url": "https://appleinsider.com/rss/news",
            "type": "news"
        },

        # AI company official sources
        {
            "name": "OpenAI News",
            "url": "https://openai.com/news/rss.xml",
            "type": "official"
        },
        {
            "name": "Anthropic",
            "url": "https://www.anthropic.com/news/rss.xml",
            "type": "official"
        },
        {
            "name": "Google DeepMind",
            "url": "https://deepmind.google/blog/rss.xml",
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

        # Semiconductor and AI infrastructure
        {
            "name": "NVIDIA News",
            "url": "https://nvidianews.nvidia.com/releases.xml",
            "type": "official"
        },
        {
            "name": "NVIDIA Blog",
            "url": "https://blogs.nvidia.com/feed/",
            "type": "official"
        },

        # Google News topic feeds
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

        # Finance and market news
        {
            "name": "Yahoo Finance",
            "url": "https://finance.yahoo.com/news/rssindex",
            "type": "finance"
        },
        {
            "name": "MarketWatch",
            "url": "http://feeds.marketwatch.com/marketwatch/topstories/",
            "type": "finance"
        },
        {
            "name": "Seeking Alpha",
            "url": "https://seekingalpha.com/feed.xml",
            "type": "finance"
        },

        # World news
        {
            "name": "Associated Press",
            "url": "https://apnews.com/hub/ap-top-news?output=rss",
            "type": "news"
        },
        {
            "name": "BBC World",
            "url": "http://feeds.bbci.co.uk/news/world/rss.xml",
            "type": "news"
        },

        # Community and discussion sources
        {
            "name": "Hacker News",
            "url": "https://news.ycombinator.com/rss",
            "type": "community"
        },
        {
            "name": "Reddit Artificial",
            "url": "https://www.reddit.com/r/artificial/.rss",
            "type": "community"
        },
        {
            "name": "Reddit ChatGPT",
            "url": "https://www.reddit.com/r/ChatGPT/.rss",
            "type": "community"
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
            "name": "Reddit Apple",
            "url": "https://www.reddit.com/r/apple/.rss",
            "type": "community"
        },
        {
            "name": "Reddit Technology",
            "url": "https://www.reddit.com/r/technology/.rss",
            "type": "community"
        },
        {
            "name": "Reddit Stocks",
            "url": "https://www.reddit.com/r/stocks/.rss",
            "type": "community"
        },

        {
            "name": "Google News Taiwan",
            "url": "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
            "type": "news"
        },
        {
            "name": "Google News Tech TW",
            "url": "https://news.google.com/rss/search?q=科技&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
            "type": "news"
        },
        {
            "name": "Google News Business TW",
            "url": "https://news.google.com/rss/search?q=財經&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
            "type": "finance"
        },
        {
            "name": "Google News ESL",
            "url": "https://news.google.com/rss/search?q=electronic%20shelf%20label&hl=en-US&gl=US&ceid=US:en",
            "type": "industry"
        },
        {
            "name": "Google News Smart Retail",
            "url": "https://news.google.com/rss/search?q=smart%20retail%20OR%20retail%20automation&hl=en-US&gl=US&ceid=US:en",
            "type": "industry"
        },
        {
            "name": "Google News M2COMM Competitors",
            "url": "https://news.google.com/rss/search?q=Hanshow%20OR%20VusionGroup%20OR%20Pricer%20OR%20SOLUM%20OR%20Zkong&hl=en-US&gl=US&ceid=US:en",
            "type": "competitor"
        },
        {
            "name": "Retail Dive",
            "url": "https://www.retaildive.com/feeds/news/",
            "type": "industry"
        },
        {
            "name": "Retail Technology Innovation Hub",
            "url": "https://retailtechinnovationhub.com/home?format=rss",
            "type": "industry"
        },
        {
            "name": "IoT Business News",
            "url": "https://iotbusinessnews.com/feed/",
            "type": "iot"
        },
        {
            "name": "IoT World Today",
            "url": "https://www.iotworldtoday.com/rss.xml",
            "type": "iot"
        },
        {
            "name": "E Ink News",
            "url": "https://www.eink.com/news.xml",
            "type": "supplier"
        }
        ]



def collect_all_articles(sources):
    """
    Collect articles from all RSS sources.

    Args:
        sources: A list of RSS source dictionaries.

    Returns:
        A list of article dictionaries.
    """

    all_articles = []

    for source in sources:
        try:
            # Fetch RSS feed content with timeout to avoid hanging.
            response = requests.get(
                source["url"],
                timeout=10
            )

            feed = feedparser.parse(response.content)

            for entry in feed.entries:
                all_articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": source["name"],
                    "source_type": source["type"]
                })

            print("Success: " + source["name"])

        except Exception as e:
            # If one source fails, continue collecting from other sources.
            print("Failed: " + source["name"] + " -> " + str(e))
            continue

    return all_articles


def filter_articles(all_articles, keywords):
    """
    Filter collected articles by active keywords.

    An article is selected if at least one keyword appears in its title.

    Args:
        all_articles: A list of collected articles.
        keywords: Active keywords from the database.

    Returns:
        A list of matched article dictionaries.
    """

    filtered_articles = []

    for article in all_articles:
        title_lower = article["title"].lower()

        matched_keywords = []

        for keyword in keywords:
            keyword_lower = keyword.lower()

            if keyword_lower in title_lower:
                matched_keywords.append(keyword_lower)

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
    """
    Main collection function.

    This function:
    1. Loads RSS sources.
    2. Loads active keywords from the database.
    3. Collects articles from all RSS feeds.
    4. Filters articles by keyword.
    5. Saves matched articles to ai_news.csv.

    Returns:
        filtered_articles: Articles matched by keyword.
        keywords: Active keywords used for filtering.
    """

    sources = get_sources()
    keywords = get_keywords()

    all_articles = collect_all_articles(sources)
    filtered_articles = filter_articles(
        all_articles,
        keywords
    )

    print("total articles collected:", len(all_articles))
    print("matched articles:", len(filtered_articles))

    df = pd.DataFrame(filtered_articles)

    print(df)

    # Export filtered articles for debugging and manual review.
    df.to_csv(
        "ai_news.csv",
        index=False
    )

    return filtered_articles, keywords