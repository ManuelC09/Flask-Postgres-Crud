from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    
    DEBUG = True
    TESTING = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    
class ProductionConfig(Config):
        DEBUG = False
        
class DevelopmentConfig(Config):
        DEBUG = True
        TESTING = True