from flask_restful import Resource, reqparse, abort, marshal
from flask_jwt_extended import create_access_token, create_refresh_token
from Models.Users.UserModel import UserModel
from Serializers.UserFields import user_fields

class UserLoginResource(Resource):
    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('login_or_email', required = True, location = 'json')
        req_parser.add_argument('Password', required = True, location = 'json')
        request_data = req_parser.parse_args()

        user_identifier = request_data['login_or_email']
        user_pass = request_data['Password']
        
        user = UserModel.get_user(login = user_identifier)
        if user is None: 
            user = UserModel.get_user(email = user_identifier)
            if user is None:
                abort(400, message = f'User {user_identifier} doesn\'t exists.')
        if not user.validate_pass(user_pass):
            abort(400, message = f'User login or password not valid. Try again.')
        return {
            'Login' : user.login,
            'access_token' : create_access_token(identity = user.login),
            'refresh_token' : create_refresh_token(identity = user.login)
        }, 200
        