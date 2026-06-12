import requests
import feedparser
import pandas as pd

from database import get_active_group_keywords

def get_sources():
    """
    Return a list of RSS sources used by the news collector.

    Each source contains:
    - name: Display name of the RSS source
    - url: RSS feed URL
    - type: Source category, such as news, official, finance, or community
    """

    return [
    # International technology news
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "type": "technology"
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "type": "technology"
    },
    {
        "name": "Ars Technica",
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "type": "technology"
    },
    {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
        "type": "technology"
    },
    {
        "name": "VentureBeat",
        "url": "https://venturebeat.com/feed/",
        "type": "technology"
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "type": "technology"
    },

    # Taiwan / Chinese technology and business news
    {
        "name": "Google News Taiwan Tech",
        "url": "https://news.google.com/rss/search?q=科技&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        "type": "technology_tw"
    },
    {
        "name": "Google News Taiwan Business",
        "url": "https://news.google.com/rss/search?q=財經&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        "type": "business_tw"
    },
    {
        "name": "Google News Taiwan IoT",
        "url": "https://news.google.com/rss/search?q=物聯網&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        "type": "iot_tw"
    },
    {
        "name": "Google News Taiwan Smart Retail",
        "url": "https://news.google.com/rss/search?q=智慧零售&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        "type": "retail_tw"
    },
    {
        "name": "Google News Taiwan Electronic Shelf Label",
        "url": "https://news.google.com/rss/search?q=電子貨架標籤 OR 電子價籤&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        "type": "esl_tw"
    },

    # ESL / Smart retail / Retail automation
    {
        "name": "Google News Electronic Shelf Label",
        "url": "https://news.google.com/rss/search?q=electronic%20shelf%20label&hl=en-US&gl=US&ceid=US:en",
        "type": "esl"
    },
    {
        "name": "Google News ESL Market",
        "url": "https://news.google.com/rss/search?q=electronic%20shelf%20label%20market&hl=en-US&gl=US&ceid=US:en",
        "type": "esl"
    },
    {
        "name": "Google News Smart Retail",
        "url": "https://news.google.com/rss/search?q=smart%20retail&hl=en-US&gl=US&ceid=US:en",
        "type": "retail"
    },
    {
        "name": "Google News Retail Automation",
        "url": "https://news.google.com/rss/search?q=retail%20automation&hl=en-US&gl=US&ceid=US:en",
        "type": "retail"
    },
    {
        "name": "Google News Inventory Automation",
        "url": "https://news.google.com/rss/search?q=inventory%20automation%20OR%20inventory%20visibility&hl=en-US&gl=US&ceid=US:en",
        "type": "retail"
    },

    # M2COMM competitor intelligence
    {
        "name": "Google News ESL Competitors",
        "url": "https://news.google.com/rss/search?q=Hanshow%20OR%20VusionGroup%20OR%20Pricer%20OR%20SOLUM%20OR%20Zkong%20OR%20Displaydata&hl=en-US&gl=US&ceid=US:en",
        "type": "competitor"
    },
    {
        "name": "Google News Vusion Hanshow Pricer",
        "url": "https://news.google.com/rss/search?q=VusionGroup%20OR%20Hanshow%20OR%20Pricer&hl=en-US&gl=US&ceid=US:en",
        "type": "competitor"
    },

    # Retail industry sources
    {
        "name": "Retail Dive",
        "url": "https://www.retaildive.com/feeds/news/",
        "type": "retail"
    },
    {
        "name": "Retail Technology Innovation Hub",
        "url": "https://retailtechinnovationhub.com/home?format=rss",
        "type": "retail"
    },
    {
        "name": "RetailWire",
        "url": "https://retailwire.com/feed/",
        "type": "retail"
    },
    {
        "name": "Chain Store Age",
        "url": "https://chainstoreage.com/rss.xml",
        "type": "retail"
    },

    # IoT / wireless / edge technology
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
        "name": "Google News IoT",
        "url": "https://news.google.com/rss/search?q=IoT%20OR%20Internet%20of%20Things&hl=en-US&gl=US&ceid=US:en",
        "type": "iot"
    },
    {
        "name": "Google News LPWAN",
        "url": "https://news.google.com/rss/search?q=LPWAN%20OR%20low%20power%20wireless&hl=en-US&gl=US&ceid=US:en",
        "type": "wireless"
    },

    # Healthcare / logistics applications
    {
        "name": "Google News Healthcare IoT",
        "url": "https://news.google.com/rss/search?q=healthcare%20IoT%20OR%20hospital%20inventory%20automation&hl=en-US&gl=US&ceid=US:en",
        "type": "healthcare"
    },
    {
        "name": "Google News Logistics Automation",
        "url": "https://news.google.com/rss/search?q=logistics%20automation%20OR%20warehouse%20automation&hl=en-US&gl=US&ceid=US:en",
        "type": "logistics"
    },
    {
        "name": "Google News Cold Chain Monitoring",
        "url": "https://news.google.com/rss/search?q=cold%20chain%20monitoring%20OR%20cold%20chain%20IoT&hl=en-US&gl=US&ceid=US:en",
        "type": "logistics"
    },

    # Display / e-paper supply chain
    {
        "name": "E Ink News",
        "url": "https://www.eink.com/news.xml",
        "type": "supplier"
    },
    {
        "name": "Google News E Paper",
        "url": "https://news.google.com/rss/search?q=e-paper%20display%20OR%20electronic%20paper%20display&hl=en-US&gl=US&ceid=US:en",
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
    keywords = get_active_group_keywords()

    print("active group keywords:", keywords)

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