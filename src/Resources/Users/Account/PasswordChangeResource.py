from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from Models.Users.UserModel import UserModel

class PasswordChangeResource(Resource):
    @jwt_required
    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('password', required = True, location = 'json')
        req_parser.add_argument('new_password', required = True, location = 'json')
        request_data = req_parser.parse_args()
        user_pass = request_data['password']
        new_pass = request_data['new_password']
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        if user is None: 
            abort(400, message = 'Invalid user')
        if not user.validate_pass(user_pass):
            abort(400, message = 'Invalid password.')
        user.change_pass(new_pass)
        return {'msg' : 'Password changed.'}, 200