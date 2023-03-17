from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.post("/")
def summarize(input_text: str, max_length: int = 81, min_length: int = 30, do_sample: bool = False):
    # Run the summarization pipeline
    summary = summarizer(input_text, max_length=max_length, min_length=min_length, do_sample=do_sample)
    return summary

# uvicorn main:app --reload --port 8001
