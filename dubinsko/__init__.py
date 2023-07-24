from asyncio.log import logger
from flask import Flask, request, current_app
from config import Config
from flask_mail import Mail
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_babel import Babel
from flask import session
from babel.core import UnknownLocaleError

app = Flask(__name__)
mail = Mail()
bootstrap = Bootstrap()
babel = Babel()

app.debug = True
app.config.from_object(Config)
app.config['MAIL_SERVER'] ="smtp.gmail.com"
app.config['MAIL_PORT'] =587
app.config['MAIL_USERNAME'] ="your_email_here"
app.config['MAIL_PASSWORD'] ="your_password_here"
app.config['MAIL_USE_TLS'] =True
app.config['MAIL_USE_SSL'] =False


app.config['BOOTSTRAP_SERVE_LOCAL'] = True

@app.context_processor
def inject_conf_var():
    return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'], CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys())))
    

def get_locale():
        

        language = session.get('language')

        # Check if the language is available in LANGUAGES
        if language and language in app.config['LANGUAGES']:
            return language

        # Get the language from the URL parameter
        url_language = request.view_args.get('language')

        # Check if the language is available in LANGUAGES
        if url_language and url_language in app.config['LANGUAGES']:
            return url_language

        return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

# mail.init_app(app)
babel.init_app(app, locale_selector=get_locale)
bootstrap.init_app(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TSL']:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], 
        subject='Microblog Failure',
        credentials=auth, 
        secure=secure)

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/dubinsko.log',backupCount=10, maxBytes=10240)
    file_handler.setFormatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]')
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler('Dubinsko Miroslav')

    

from dubinsko import routes, error_handlers
