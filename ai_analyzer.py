from openai import OpenAI

client = OpenAI()

def analyze_market_sentiment(filtered_articles):

    headlines = []

    for article in filtered_articles[:10]:
        headlines.append(article["title"])

    headlines_text = "\n".join(headlines)

    prompt = f"""
    Analyze the market sentiment based on these headlines and return the traditional mandarin summary.

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

    sentiment = "Unknown"
    summary = ai_text

    lines = ai_text.split("\n")

    for line in lines:
        if line.startswith("Sentiment:"):
            sentiment = line.replace("Sentiment:", "").strip()

        elif line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()

    return sentiment, summary