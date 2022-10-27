from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired, Length,email_validator

class ContactForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(message="The name has to 3 character and longer."),Length(min=3,max=30)])
    email_address = StringField(label = 'Email:', validators= [Email(message="Inser a valid email address!"), DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(),Length(max=600)])
    submit = SubmitField('Submit')