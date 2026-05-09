from transformers import pipeline

# Load summarization model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_text(text, max_length):
    summary = summarizer(
        text,
        max_length=max_length,
        min_length=30,
        do_sample=False
    )

    return summary[0]['summary_text']