from textblob import TextBlob


def correctify_spelling(text: str) -> str:
    blob = TextBlob(text)
    return str(blob.correct())


def get_spelling_suggestions(text: str) -> list:
    blob = TextBlob(text)
    suggestions = []
    for word in blob.words:
        corrected_word = word.correct()
        if word != corrected_word:
            suggestions.append((word, corrected_word))
    return suggestions


def analyze_sentiment(text: str) -> str:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"


def translate_text(text: str, target_language: str = 'en') -> str:
    blob = TextBlob(text)
    return str(blob.translate(to=target_language))


def main():
    user_input = input("Enter a text to analyze: ")

    # Spell Checking and Correction
    corrected_text = correctify_spelling(user_input)
    print(f"Corrected Text: {corrected_text}")

    # Spelling Suggestions
    suggestions = get_spelling_suggestions(user_input)
    if suggestions:
        print("\nSpelling Suggestions:")
        for incorrect_word, suggested_word in suggestions:
            print(f"'{incorrect_word}' -> '{suggested_word}'")
    else:
        print("\nNo spelling mistakes found.")

    # Sentiment Analysis
    sentiment = analyze_sentiment(user_input)
    print(f"\nSentiment: {sentiment}")

    # Translate (optional)
    translate_choice = input(
        "\nDo you want to translate this text? (y/n): ").strip().lower()
    if translate_choice == 'y':
        target_language = input(
            "Enter the language code (e.g., 'es' for Spanish, 'fr' for French): ").strip()
        translated_text = translate_text(user_input, target_language)
        print(f"\nTranslated Text: {translated_text}")


if __name__ == "__main__":
    main()
