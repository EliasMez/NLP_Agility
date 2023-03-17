from transformers import pipeline

model_name = "human-centered-summarization/financial-summarization-pegasus"
summarizer = pipeline("summarization",model=model_name)