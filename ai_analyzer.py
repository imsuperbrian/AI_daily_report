from openai import OpenAI

def analyze_market_sentiment(filtered_articles, api_key = None):
    """
    Analyze market sentiment using OpenAI.

    The function takes a list of filtered articles,
    extracts the most recent headlines, and asks
    OpenAI to generate:

    - Sentiment (Bullish / Neutral / Bearish)
    - Short summary in Traditional Chinese

    Args:
        filtered_articles:
            List of filtered article dictionaries.

    Returns:
        AI-generated sentiment analysis text.
    """

    # Create OpenAI client using OPENAI_API_KEY
    client = OpenAI(api_key = api_key)

    # Handle empty article list.
    if not filtered_articles:
        return """
Sentiment: Neutral
Summary: 今天沒有符合條件的新聞。
        """

    headlines = []

    # Limit the number of headlines to reduce token usage.
    for article in filtered_articles[:10]:
        headlines.append(article["title"])

    headlines_text = "\n".join(headlines)

    prompt = f"""
    Analyze the market sentiment based on these headlines.

    Use Traditional Chinese.

    Return exactly in this format:

    Sentiment: Bullish / Neutral / Bearish
    Summary: One short paragraph in Traditional Chinese.

    Headlines:
    {headlines_text}
    """

    try:

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:

        return "AI Analysis Failed:\n" + str(e)


def parse_ai_analysis(ai_text):
    """
    Parse OpenAI sentiment analysis output.

    Example input:

    Sentiment: Bullish
    Summary: Apple 在 WWDC 發表新的 AI 功能...

    Returns:
        sentiment:
            Bullish / Neutral / Bearish

        summary:
            Traditional Chinese summary text
    """

    sentiment = "Unknown"
    summary = ai_text

    lines = ai_text.split("\n")

    for line in lines:

        if line.startswith("Sentiment:"):
            sentiment = (
                line.replace(
                    "Sentiment:",
                    ""
                ).strip()
            )

        elif line.startswith("Summary:"):
            summary = (
                line.replace(
                    "Summary:",
                    ""
                ).strip()
            )

    return sentiment, summary




def generate_keyword_insight(keyword, articles, api_key = None):

    if not articles:
        return "No articles available for insight generation."

    client = OpenAI(api_key = api_key)

    headlines = []

    for article in articles[:15]:
        title = article["title"]
        source = article["source"]

        headlines.append(
            f"- {title} ({source})"
        )

    headlines_text = "\n".join(headlines)

    prompt = f"""
You are a market intelligence analyst.

Analyze why this keyword is trending.

Keyword:
{keyword}

Recent headlines:
{headlines_text}

Return in Traditional Chinese.

Format:
1. Why is it trending?
2. Key themes
3. Market / industry implications
4. Potential opportunities
5. Potential risks
6. One-sentence takeaway

Keep it concise but useful for decision making.
"""

    response = client.responses.create(model="gpt-4.1-mini", input=prompt)

    return response.output_text



def generate_executive_briefing(articles, api_key=None):

    if not articles:
        return "No articles available for executive briefing."

    client = OpenAI(api_key=api_key)

    headlines = []

    for article in articles[:30]:
        title = article["title"]
        source = article["source"]
        keywords = article["keywords"]

        headlines.append(
            f"- {title} ({source}) | Keywords: {keywords}"
        )

    headlines_text = "\n".join(headlines)

    prompt = f"""
    You are a senior Competitive Intelligence Analyst for M2COMM.

    M2COMM focuses on:
    - Electronic Shelf Labels (ESL)
    - Smart Retail
    - Retail Automation
    - IoT
    - Wireless Communication
    - Healthcare and Logistics Solutions

    Key Competitors:
    - Hanshow
    - VusionGroup
    - Pricer
    - SOLUM
    - Zkong

    Analyze today's news headlines and generate an executive briefing for M2COMM management.

    Headlines:
    {headlines_text}

    Return in Traditional Chinese.

    IMPORTANT:
    You MUST use EXACTLY the following section titles and field labels.

    Required Output Format:

    Top Opportunity
    Reason:
    Impact:

    Top Threat
    Reason:
    Impact:

    Fastest Growing Topic
    Reason:
    Impact:

    Regional Trend
    Reason:
    Impact:

    Recommended Actions
    - 
    - 
    - 

    Rules:
    - Do not use any other section titles.
    - Do not write an executive summary.
    - Do not use numbered sections.
    - Keep each Reason and Impact concise.
    - Focus on business value for M2COMM.
    - Focus on competitors, customer demand, markets, regions, and product opportunities.
    """


    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text