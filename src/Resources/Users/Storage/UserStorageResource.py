from flask_restful import Resource, abort, marshal, request, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from Serializers.StorageElementFields import storage_element_fields
from Serializers.StorageFields import storage_fields

from Models.Users.UserModel import UserModel

class UserStorageResource(Resource):
    @jwt_required
    def get(self):
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        return marshal(user.storage, storage_fields), 200
    
    @jwt_required
    def post(self):
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        
        parser = reqparse.RequestParser()
        parser.add_argument('file' , required = True, type=FileStorage, location = 'files')
        file = parser.parse_args()['file']
        user.storage.add_file(file)
        return marshal(user.storage, storage_fields), 200



