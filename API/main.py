from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
from transformers import AutoTokenizer

app = FastAPI()
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)

summarizer = pipeline("summarization",model=model_name,tokenizer=tokenizer)
class Request(BaseModel):
    input_text : str

@app.post("/summarize")
async def summarize(input_text: Request):
    text_to_summarize = input_text.dict()["input_text"]
    
    # sentences = text_to_summarize.split(".")
    # # Group the sentences into clusters of 3
    # clusters = [sentences[i:i+3] for i in range(0, len(sentences), 3)]
    # # Generate a summary for each cluster
    # cluster_summaries = [summarizer(' '.join(cluster), do_sample=False)[0]['summary_text'] for cluster in clusters]

    # # Combine the cluster summaries into a final summary
    # final_summary = ' '.join(cluster_summaries)
    max_input_length = 1024
    input_text = input_text[:max_input_length]
    # Generate a summary of the input text
    summary = text_to_summarize(input_text, do_sample=True)
    return {"summary":str(summary[0]['summary_text'])}

# uvicorn main:app --reload --port 8001
