import os
from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv
from transformers import pipeline
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration

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
    if form.validate_on_submit():
        
        # Let's load the model and the tokenizer 
        model_name = "human-centered-summarization/financial-summarization-pegasus"
        summarizer = pipeline("summarization",model=model_name)                                                                   
        text_to_summarize = form.data["text"]
       
        sentences = text_to_summarize.split(".")

        # Group the sentences into clusters of 3
        clusters = [sentences[i:i+3] for i in range(0, len(sentences), 3)]

        # Generate a summary for each cluster
        cluster_summaries = [summarizer(' '.join(cluster))[0]['summary_text'] for cluster in clusters]

        # Combine the cluster summaries into a final summary
        final_summary = ' '.join(cluster_summaries)

        summary = final_summary
        
        return render_template("formulaire.html",form=form,erreur=erreur,summary = summary)


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