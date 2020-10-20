from flask_restful import Resource, marshal, abort, reqparse

from Models.Users.UserModel import UserModel
from Serializers.UserFields import user_fields
from Utils.JWT import admin_required

class AdUserResource(Resource):
    
    @admin_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_login', required = False, location = 'args')
        request_data = parser.parse_args()
        user_login = request_data['user_login']
        if user_login is None: 
            deleted_rows = UserModel.get_all_users()
            return {'msg' : f'{deleted_rows} rows deleted.'}, 204
        user = UserModel.get_user(login = user_login)
        if user is None:
            abort(404, message='Invalid user login')
        UserModel.delete_user(user.login)
        return {'msg' : 'User deleted'}, 204
    
    @admin_required   
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_login', required = False, location = 'args')
        request_data = parser.parse_args()
        user_login = request_data['user_login']
        if user_login is None:
            users = UserModel.get_all_users()
            return marshal(users,user_fields)
        user = UserModel.get_user(login = user_login)
        if user is None:
            abort(404, message='Invalid user login')
        return marshal(user, user_fields)
