from flask_restful import Resource, abort, marshal, request, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from Serializers.StorageFields import storage_fields
from Serializers.StorageElementFields import storage_element_fields
from Models.Users.UserModel import UserModel

from Utils.file_operators import get_file_size, GigaByte

class UserStorageResource(Resource):
    @jwt_required
    def get(self):
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        if user is None:
            abort(500, message = 'Something gone wrong.')
        return marshal(user.storage, storage_fields), 200
    
    @jwt_required
    def post(self):
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        if user is None:
            abort(500, message = 'Something gone wrong.')
        parser = reqparse.RequestParser()
        parser.add_argument('file' , required = True, type=FileStorage, location = 'files')
        file = parser.parse_args()['file']
        file_size = get_file_size(file)
        used_space = user.storage.used_space
        if file_size + used_space >= 10*GigaByte:
            abort(400, message = 'File storage capacity exceeded. File not uploaded')
        stElement = user.storage.add_file(file)
        return marshal(user.storage, storage_fields), 200


