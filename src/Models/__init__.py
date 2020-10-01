from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from gridfs import GridFS

mongo_client = MongoClient()
mongo_db = mongo_client['files']
gfs = GridFS(mongo_db)
main_db = SQLAlchemy()