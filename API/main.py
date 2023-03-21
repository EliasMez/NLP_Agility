from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

app = FastAPI()
model_name = "human-centered-summarization/financial-summarization-pegasus"
summarizer = pipeline("summarization",model=model_name)
class Request(BaseModel):
    input_text : str

@app.post("/summarize")
def summarize(input_text: Request):                                                                 
    text_to_summarize = input_text.dict()["input_text"]
    
    sentences = text_to_summarize.split(".")

    # Group the sentences into clusters of 3
    clusters = [sentences[i:i+3] for i in range(0, len(sentences), 3)]

    # Generate a summary for each cluster
    cluster_summaries = [summarizer(' '.join(cluster))[0]['summary_text'] for cluster in clusters]

    # Combine the cluster summaries into a final summary
    final_summary = ' '.join(cluster_summaries)
    return {"summary":str(final_summary)}

# uvicorn main:app --reload --port 8001
