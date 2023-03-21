import os
import requests
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction


def authenticate_client():
    load_dotenv()
    key1 = os.getenv('key1')
    key2 = os.getenv('key2')
    endpoint = os.getenv('endpoint')
    ta_credential = AzureKeyCredential(key1)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client


def sample_extractive_summarization(client,document,result_queue):
    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count=4)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else :
            summarization = "{}".format(" ".join([sentence.text for sentence in extract_summary_result.sentences]))
            result_tuple = ("Azure" ,summarization)
            result_queue.put(result_tuple)

def summarize_hugging(data,result_queue):
    response = requests.post("http://0.0.0.0/summarize", json=data)
    summary_hugging = response.json()["summary"]
    result_tuple = ("Hugging" ,summary_hugging)
    result_queue.put(result_tuple)