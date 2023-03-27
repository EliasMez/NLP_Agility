import os
import requests
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction
from PyPDF2 import PdfReader
import threading


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
    response = requests.post("http://api-summary.esbmczgjaqhjhyfh.francecentral.azurecontainer.io/summarize", json=data)
    summary_hugging = response.json()["summary"]
    result_tuple = ("Hugging Face (facebook/bart-large-cnn)" ,summary_hugging)
    result_queue.put(result_tuple)

    
def pdf_extract(pdf_file):
    # creating a pdf file object 
    # pdfFileObj = open(pdf_file, 'rb') 
        
    # creating a pdf reader object 
    # pdfReader = PdfReader(pdfFileObj)
    pdfReader = PdfReader(pdf_file) 
    text = ''

    for i, page in enumerate(pdfReader.pages):
        text += f'\n'
        text += page.extract_text()

    text = text.split('\n')
    text = " ".join(text)
    text= text.replace("\xa0"," " )
        
    # creating a page object 
    # pagesObj = [pdfReader.pages[i] for i in range(len(pdfReader.pages))]
        
    # extracting text from page 
    # result = ' \n '.join([pagesObj[i].extract_text() for i in range(len(pagesObj))])
        
    # closing the pdf file object 
    # pdfFileObj.close()

    return text


def get_summarization(data,result_queue) : 
    client = authenticate_client()
    # On crée un thread pour chaque tâche de résumé
    hugging_thread = threading.Thread(target=summarize_hugging, args=(data,result_queue))
    azure_thread = threading.Thread(target=sample_extractive_summarization, args=(client,[data['input_text']],result_queue))
    # On lance les deux threads en parallèle
    hugging_thread.start()
    azure_thread.start()

    # On attend que les deux threads aient terminé leur travail
    hugging_thread.join()
    azure_thread.join()
    
    # On récupère tous les résultats de la queue
    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)
    
    return results