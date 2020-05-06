import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USER')
    MAIL_PASSWORD = os.getenv('MAIL_PASS')
    # MAIL_SERVER = 'smtp.sendgrid.net'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True    
    # MAIL_USERNAME = 'apikey'
    # MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    # SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    
