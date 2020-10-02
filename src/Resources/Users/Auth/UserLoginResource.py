from flask_restful import Resource, reqparse, abort, marshal
from flask_jwt_extended import create_access_token, create_refresh_token
from Models.Users.UserModel import UserModel
from Serializers.UserFields import user_fields

class UserLoginResource(Resource):
    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('Login', location = 'json')
        req_parser.add_argument('Password', required = True, location = 'json')
        req_parser.add_argument('E-mail', location = 'json')
        request_data = req_parser.parse_args()

        user_login = request_data['Login']
        user_pass = request_data['Password']
        user_email = request_data['E-mail']
        
        user = None
        if user_login is None and user_email is None:
            abort(400, message = f'Login or email required.')
        if user_login is not None:
            user = UserModel.get_user(login = user_login)
            if user is None: 
                abort(400, message = f'User {user_login} doesn\'t exists.')
        else:
            user = UserModel.get_user(email = user_email)
            if user is None:
                abort(400, message = f'User with email: {user_email} doesn\'t exists.')
        return {
            'Login' : user.login,
            'access_token' : create_access_token(identity = user_login),
            'refresh_token' : create_refresh_token(identity = user_login)
        }, 200
        