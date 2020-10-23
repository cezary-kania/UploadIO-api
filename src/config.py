class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'some-secret-string'
     # JWT 
    JWT_SECRET_KEY = 'jwt-sercret-string'
    JWT_REFRESH_TOKEN_EXPIRES = 60*60*24*14
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