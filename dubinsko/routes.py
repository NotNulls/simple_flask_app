from email.message import Message
from flask import current_app, render_template, request, redirect, abort, url_for, Blueprint, current_app
from dubinsko.email import send_email
from dubinsko.forms import ContactForm
from flask import session, current_app
from flask_babel import _, lazy_gettext as _l

bp = Blueprint('routes', __name__)

@bp.route("/home", methods=["GET","POST"])
@bp.route("/", methods=["GET","POST"])
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

@bp.route('/language/<language>')
def set_language(language=None):
    if language and language in current_app.config['LANGUAGES']:
        session['language'] = language
    return redirect(url_for('routes.home_page'))

