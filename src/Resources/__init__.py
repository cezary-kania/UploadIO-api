from flask_restful import Api
from flask import Blueprint

api_bp = Blueprint('api',__name__)
api = Api(api_bp)

from .Uploads import resources as uploads_resources 
from .Users import resources as users_resources 
from .Admin import resources as admin_resources
resources = uploads_resources + users_resources + admin_resources

for res,endpoint in resources:
    api.add_resource(res,endpoint)