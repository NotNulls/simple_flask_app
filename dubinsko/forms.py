from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired, Length,email_validator
from flask_babel import _, lazy_gettext as _l

class ContactForm(FlaskForm):
    name = StringField(_l('Ime'),validators=[DataRequired(message="Ime mora sadržati više of 3 karaktera."),Length(min=3,max=30)])
    email_address = StringField(label = _l('Email:'), validators= [Email(message="Unesite validnu e-mail adresu."), DataRequired()])
    message = TextAreaField(_l('Poruka'), validators=[DataRequired(),Length(max=600)])
    submit = SubmitField(_l('Pošalji'))