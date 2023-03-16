import os
from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv
from transformers import pipeline

from formulaires import SummaryText

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

##################################
##            Acceuil           ## 
##################################

@app.route("/")
def accueil():
    return render_template("index.html")


@app.route('/modeles/hugginf_face',methods=['GET','POST'])
def huggingface():
    form = SummaryText()
    erreur = None
    if form.validate_on_submit():
        

        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        # Define the input text
        input_text = form.data["text"]

        # Generate a summary of the input text
        summary = summarizer(input_text, max_length=81, min_length=30, do_sample=False)

        # Print the summary
        print(summary[0]['summary_text'])

        return render_template("huggingface.html",form=form,erreur=erreur,summary = summary)
        # return redirect(url_for("accueil"))

    return render_template("huggingface.html",form=form,erreur=erreur)


###########################
##    gunicorn app:app   ##
###########################

if __name__ == '__main__':
    app.run()