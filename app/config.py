import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        'title': 'Logora NLP',
        'description': 'A collection of tools to analyse collections of documents.',
        'version': '1.0.0',
        'uiversion': 3,
        'specs_route': '/docs/'
    }
