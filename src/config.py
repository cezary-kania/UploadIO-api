class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'some-secret-string'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
    MONGO_URI = ''
    ENV = 'production'
    DEBUG = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    MONGO_URI = 'mongodb://localhost:27017/'
    ENV = 'development'
    DEBUG = True
    # JWT 
    JWT_SECRET_KEY = 'jwt-sercret-string'