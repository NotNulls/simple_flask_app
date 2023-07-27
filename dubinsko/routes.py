from email.message import Message
from dubinsko import app, mail
from flask import current_app, render_template, request, redirect, abort, url_for
from dubinsko.email import send_email
from dubinsko.forms import ContactForm
from dubinsko import app
from flask import session
from flask_babel import _, lazy_gettext as _l



@app.route("/home", methods=["GET","POST"])
@app.route("/", methods=["GET","POST"])
def home_page():
    
    form = ContactForm()
    
    
    if request.method == "POST":
        name = form.name.data
        email = form.email_address.data
        message = form.message.data


        try:
             send_email(
                 subject=name + '@ Dubinsko - upit',
                 sender=email,
                 recipients=current_app.config['MAIL_USERNAME'],
                 text_body=message,
                
             )

        except:
             return render_template('index.html', form = form, title=_('Home - Dubinsko čišćenje'))
    
    return render_template('index.html', form = form)

@app.route('/language/<language>')
def set_language(language=None):
    if language and language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(url_for('home_page'))

