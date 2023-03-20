import os
from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv

import requests

from formulaires import SummaryText
from functions import *

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

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
    title = "Hugging face Model"
    if form.validate_on_submit():
        
        data = {"input_text":form.data["text"]}
        response = requests.post("http://0.0.0.0/summarize", json=data)
        summary =  response.json()["summary"]
        
        return render_template("formulaire.html",form=form,erreur=erreur,summary = summary,title=title)


    return render_template("formulaire.html",form=form,erreur=erreur,title=title)

@app.route('/modeles/azure',methods=['GET','POST'])
def azure():
    form = SummaryText()
    erreur = None
    title = "Azure Model"
    if form.validate_on_submit():
        client = authenticate_client()
        summary=sample_extractive_summarization(client,[form.data["text"]])

        return render_template("formulaire.html",form=form,erreur=erreur,summary = summary,title=title)
        

    return render_template("formulaire.html",form=form,erreur=erreur,title=title)


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