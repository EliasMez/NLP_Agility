from transformers import pipeline
from fastapi import FastAPI, Response
from pydantic import BaseModel


# model_name = "human-centered-summarization/financial-summarization-pegasus"
generator = pipeline("summarization", model="facebook/bart-large-cnn")
app = FastAPI()


class Body(BaseModel):
    text: str


@app.get('/')
def root():
    return Response("<h1>A self-documenting API to interact with a GPT2 model and generate text</h1>")


@app.post('/generate')
def predict(body: Body):
    results = generator(body.text)
    return results[0]
