from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField , RadioField 

class SummaryText(FlaskForm):
    text = TextAreaField("Texte a résumé :", render_kw={"placeholder": "Texte a résumé"})