from flask_restful import Resource, reqparse, abort, marshal
from flask_jwt_extended import create_access_token, create_refresh_token

from Models.Users.UserModel import UserModel
from Serializers.UserFields import user_fields

from Utils.validators import user_validators

class UserRegistrationResource(Resource):
    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('Login', type = user_validators["user_login"], required = True, location = 'json')
        req_parser.add_argument('Password', type = user_validators["user_password"], required = True, location = 'json')
        req_parser.add_argument('E-mail', type = user_validators["user_email"], required = True, location = 'json')
        request_data = req_parser.parse_args()

        user_login = request_data['Login']
        user_pass = request_data['Password']
        user_email = request_data['E-mail']
        
        if UserModel.get_user(login = user_login) is not None:
            abort(400, message = f'Login {user_login} already used.')
        if UserModel.get_user(email = user_email) is not None:
            abort(400, message = f'Account with email: {user_email} already exists.')    
        user = UserModel(user_login, user_pass, user_email)
        try:
            UserModel.add(user)
            return {
                'Login' : user.login,
                'access_token' : create_access_token(identity = user_login),
                'refresh_token' : create_refresh_token(identity = user_login)
            }, 201
        except:
            abort(500, message = 'Can\'t create user. Plase try later.')
        