from transformers import pipeline

model_name = "facebook/bart-large-cnn"
summarizer = pipeline("summarization",model=model_name)