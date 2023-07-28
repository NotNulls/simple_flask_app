from asyncio.log import logger
from flask import Flask, request
from config import Config
from flask_mail import Mail
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_babel import Babel
from flask import session
from babel.core import UnknownLocaleError


mail = Mail()
bootstrap = Bootstrap()
babel = Babel()


def create_app(config_class=Config):

    app = Flask(__name__)

    app.debug = True
    app.config.from_object(Config)
    app.config['MAIL_SERVER'] ="smtp.gmail.com"
    app.config['MAIL_PORT'] =587
    app.config['MAIL_USERNAME'] ="<your-email-address>"
    app.config['MAIL_PASSWORD'] ="<yourp-email-password>"
    app.config['MAIL_USE_TLS'] =True
    app.config['MAIL_USE_SSL'] =False
    app.config['MAIL_DEFAULT_SENDER'] = ('<admin-name>', '<your-email-address>')


    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    mail.init_app(app)
    bootstrap.init_app(app)

    from dubinsko.routes import bp as routes_blueprint
    app.register_blueprint(routes_blueprint)

    from dubinsko.error_handlers import bp as errors_blueprint
    app.register_blueprint(errors_blueprint)

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

    babel.init_app(app, locale_selector=get_locale)

    if not app.debug and not app.testing:
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
            subject='Dubinsko Miroslav Failure',
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

    return app

from dubinsko import routes, error_handlers
