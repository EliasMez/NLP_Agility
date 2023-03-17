from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField , RadioField, FileField

class SummaryText(FlaskForm):
    text = TextAreaField("Texte a résumé :", render_kw={"placeholder": "Texte a résumé"})

class PdfForm(FlaskForm):
    pdf = FileField("PDF a résumé :", render_kw={"placeholder": "PDF a résumé"})