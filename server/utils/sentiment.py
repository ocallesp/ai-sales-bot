# server/utils/sentiment.py
from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def analyze_sentiment(text: str) -> str:
    result = classifier(text)[0]
    label = result["label"].lower()  # "positive" or "negative"
    score = result["score"]  # Confidence score between 0 and 1
    # If the confidence is below 0.7, classify as "neutral"
    if score < 0.7:
        return "neutral"
    return label
