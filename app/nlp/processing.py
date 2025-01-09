import spacy

# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

def process_user_input(text):
    """
    Tokenize and normalize user input.
    :param text: User input string
    :return: A response string
    """
    try:
        # Tokenize and normalize input
        doc = nlp(text)

        # Filter tokens: Exclude stop words and punctuation, include meaningful words
        tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]

        print(tokens)

        # Join tokens back into a normalized string
        normalized_text = " ".join(tokens)

        # If no meaningful tokens remain, return a fallback response
        if not normalized_text:
            normalized_text = "I couldn't understand your message."

        # Return the processed response
        return f"You said: {normalized_text}"
    except Exception as e:
        # Return an error message for debugging
        raise ValueError(f"Error in NLP processing: {e}")
