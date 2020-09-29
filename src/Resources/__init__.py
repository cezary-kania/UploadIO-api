from flask_restful import Api
from flask import Blueprint

api_bp = Blueprint('api',__name__)
api = Api(api_bp)
from .UploadResource import UploadResource
api.add_resource(UploadResource, '/upload', '/upload/<string:url_hash>')

