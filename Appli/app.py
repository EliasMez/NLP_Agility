import os
import queue
from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import requests
from formulaires import SummaryText, PdfForm
from functions import *


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

##################################
##            Acceuil           ## 
##################################

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def accueil():
    return render_template("index.html")


#################################
##      Modeles               ##
################################

    


@app.route('/summary',methods=['GET','POST'])
def summary():
    form = SummaryText()
    erreur = None
    title = "Résumé avec differents modèles"
    result_queue = queue.Queue()

    
    if form.validate_on_submit():
        data = {"input_text":form.data["text"]}
        results = get_summarization(data,result_queue)
        return render_template("formulaire.html",form=form,erreur=erreur,title=title,results=results)


    return render_template("formulaire.html",form=form,erreur=erreur,title=title)


@app.route('/summary-pdf',methods=['GET','POST'])
def pdf_summary():
    title = "Résumé du pdf avec differents modèles"
    result_queue = queue.Queue()
    erreur = None
    form = PdfForm()
    if form.validate_on_submit():
            # Récupérer le fichier PDF
            # pdf_file = request.files['pdf_file']
            # Define the input text
            # return render_template(pdf_extract(pdf_file))
            
            data = {"input_text":pdf_extract(form.pdf.data)}
            
            # data = {"input_text":pdf_extract(pdf_file)}
            results = get_summarization(data,result_queue)
            return render_template("pdf.html",erreur=erreur,title=title,results=results,form_pdf=form)
    return render_template("pdf.html",form_pdf=form,erreur=erreur,title=title)

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