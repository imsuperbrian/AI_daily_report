import re

def remove_duplicates(filtered_articles):
    """
    Remove duplicate articles based on title.

    Articles with the same title are treated as duplicates.
    Only the first occurrence is kept.

    Args:
        filtered_articles:
            List of filtered article dictionaries.

    Returns:
        List of unique articles.
    """

    seen = set()
    cleaned_articles = []

    for article in filtered_articles:

        title = article["title"].lower()

        if title not in seen:
            seen.add(title)
            cleaned_articles.append(article)

    return cleaned_articles


def count_title(filtered_articles):
    """
    Count word frequency from article titles.

    Args:
        filtered_articles:
            List of filtered article dictionaries.

    Returns:
        Dictionary where:
            key = word
            value = frequency
    """

    count = {}
    

    for article in filtered_articles:

        title = article["title"]

def count_title(filtered_articles):
    """
    Count word frequency from article titles.

    Args:
        filtered_articles:
            List of filtered article dictionaries.

    Returns:
        Dictionary where:
            key = word
            value = frequency
    """

    count = {}
    
    for article in filtered_articles:

        title = article["title"]

        words = re.findall(r"\b[a-zA-Z0-9]+\b", title.lower())

        for word in words:

            word = word.lower()

            if word not in count:
                count[word] = 1
            else:
                count[word] += 1

    return count


def display_words_count(filtered_articles, keywords):
    """
    Generate a simple trending-word report.

    Common stop words and tracked keywords are removed.

    Args:
        filtered_articles:
            List of filtered article dictionaries.

        keywords:
            Active keywords currently being tracked.

    Returns:
        Formatted string containing the top 5 trending words.
    """

    word_count = count_title(filtered_articles)

    result = ""

    sorted_words = sorted(
        word_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    # Common English stop words.
    stop_words = {
        "the", "a", "an", "to", "of", "and", "for",
        "in", "on", "at", "with", "-", "is", "are",
        "as", "by", "from", "this", "that"
    }

    # Remove tracked keywords from trending-word analysis.
    for keyword in keywords:
        stop_words.add(keyword.lower())

    count = 0

    for word, number in sorted_words:

        if word in stop_words:
            continue

        result += (word + " - " + str(number) + "\n")
        count += 1

        # Only display the top 5 words.
        if count == 5:
            break

    return result