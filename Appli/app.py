import os
import threading
import queue
from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv

import requests

from formulaires import SummaryText
from functions import *

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
client = authenticate_client()
##################################
##            Acceuil           ## 
##################################

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
    if form.validate_on_submit():
        result_queue = queue.Queue()
        data = {"input_text":form.data["text"]}
        # On crée un thread pour chaque tâche de résumé
        hugging_thread = threading.Thread(target=summarize_hugging, args=(data,result_queue))
        azure_thread = threading.Thread(target=sample_extractive_summarization, args=(client,[form.data["text"]],result_queue))
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
        
        return render_template("formulaire.html",form=form,erreur=erreur,title=title,results=results)


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