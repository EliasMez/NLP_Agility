import os
from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv
from transformers import pipeline
from werkzeug.utils import secure_filename
from formulaires import SummaryText, PdfForm
from functions import *
from PDF_extract import pdf_extract

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##################################
##            Acceuil           ## 
##################################


@app.route("/")
def accueil():
    return render_template("index.html")


#################################
##      Modeles               ##
################################

@app.route('/modeles/hugging_face',methods=['GET','POST'])
def huggingface():
    form = SummaryText()
    erreur = None
    if request.method == 'POST':
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        if form.validate_on_submit(): 
            # Define the input text
            input_text = form.data["text"]

            # Generate a summary of the input text
            summary = summarizer(input_text, max_length=81, min_length=30, do_sample=False)
            return render_template("formulaire.html",form=form,erreur=erreur,summary = summary)

        form_pdf = PdfForm()
        if form_pdf.validate_on_submit():
            # Récupérer le fichier PDF
            pdf_file = request.files['pdf_file']
            # Define the input text
            input_pdf = form.data["pdf"]
            if allowed_file(input_pdf):
                input_text = pdf_extract(pdf_file)
                # Generate a summary of the input text
                summary = summarizer(input_text, max_length=81, min_length=30, do_sample=False)
                return render_template("formulaire.html",form=form,erreur=erreur,summary = summary)
            else :
                return render_template("formulaire.html",form=form,erreur=erreur)

    return render_template("formulaire.html",form=form,erreur=erreur)



@app.route('/modeles/azure',methods=['GET','POST'])
def azure():
    form = SummaryText()
    erreur = None
    if form.validate_on_submit():
        client = authenticate_client()
        summary=sample_extractive_summarization(client,[form.data["text"]])

        return render_template("formulaire.html",form=form,erreur=erreur,summary = summary)
        

    return render_template("formulaire.html",form=form,erreur=erreur)


######################################
##         error 404
####################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#########################################
##    gunicorn --timeout 600 app:app   ##
#########################################

if __name__ == '__main__':
    app.run()