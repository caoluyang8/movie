import os

class Config:
    SECRET_KEY = '35as1da3w513s51a3sd1ads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_NUM = 5
    UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'static/upload')
    MAX_CONTENT_LENGTH = 1024*1024*64

class DevelopmentConfig(Config):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir,'exam.sqlite')
    DEBUG = True
    TESTING = False

configDict = {
    'default':DevelopmentConfig,
}