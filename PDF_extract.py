# importing required modules 
from PyPDF2 import PdfReader
    
def pdf_extract(pdf_file):
    # creating a pdf file object 
    pdfFileObj = open(pdf_file, 'rb') 
        
    # creating a pdf reader object 
    pdfReader = PdfReader(pdfFileObj) 
        
    # creating a page object 
    pageObj = pdfReader.pages[0]
        
    # extracting text from page 
    result = pageObj.extract_text()
        
    # closing the pdf file object 
    pdfFileObj.close()

    return result