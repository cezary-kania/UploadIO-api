from flask_restful import Resource, marshal, abort, reqparse

from Models.Users.UserModel import UserModel
from Serializers.UserFields import user_fields
from Utils.JWT import admin_required

class AdUserRoleResource(Resource):
    
    #@admin_required   
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_login', required = True, location = 'json')
        parser.add_argument('account_type', required = True, location = 'json')
        request_data = parser.parse_args()
        user_login = request_data['user_login']
        account_type = request_data['account_type']
        user = UserModel.get_user(login = user_login)
        if user is None:
            abort(404, message='Invalid user login')
        user.set_type(account_type)
        return marshal(user, user_fields, envelope='User')