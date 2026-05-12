def summarize_text(text):

    sentences = text.split('.')

    summary = '. '.join(sentences[:3])

    return summary