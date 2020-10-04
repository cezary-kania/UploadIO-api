from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_refresh_token_required

class AccessTokenRefResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity = user)
        return {'access_token' : access_token}, 200