import os
from dotenv import load_dotenv



basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = []
    LANGUAGES = {
        'en': "English",
        'sr_Latn_ME': "Montenegrin",
        }
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(basedir, "dubinsko/translations")
    
