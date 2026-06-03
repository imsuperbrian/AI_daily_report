def remove_duplicates(filtered_articles):
    seen = set()
    cleaned_articles = []

    for article in filtered_articles:
        title = article["title"].lower()

        if title not in seen:
            seen.add(title)
            cleaned_articles.append(article)

    return cleaned_articles


def count_title(filtered_articles):
    count = {}

    for article in filtered_articles:
        for word in article["title"].split():
            word = word.lower()

            if word not in count:
                count[word] = 1
            else:
                count[word] += 1

    return count


def display_words_count(filtered_articles, keywords):
    word_count = count_title(filtered_articles)

    result = ""

    sorted_words = sorted(
        word_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    stop_words = {
        "the", "a", "an", "to", "of", "and", "for",
        "in", "on", "at", "with", "-", "is", "are",
        "as", "by", "from", "this", "that"
    }

    for keyword in keywords:
        stop_words.add(keyword.lower())

    count = 0

    for word, number in sorted_words:
        if word in stop_words:
            continue

        result += word + " - " + str(number) + "\n"
        count += 1

        if count == 5:
            break

    return result