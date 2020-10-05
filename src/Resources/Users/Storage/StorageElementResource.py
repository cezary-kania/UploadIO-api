from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort, reqparse, marshal

from werkzeug import Response

from Serializers.StorageElementFields import storage_element_fields
from Models.Users.StorageElModel import StorageElModel
from Models.Users.UserModel import UserModel

class StorageElementResource(Resource):
    
    @jwt_required
    def delete(self, element_id):
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        if user is None:
            abort(500, message = 'Something gone wrong.')
        stElement = StorageElModel.get_element(id = int(element_id))
        if stElement is None:
            abort(400, message = 'Element not found.')
        if not self.validate_user_access(user, stElement):
            abort(401)
        user.storage.delete_element(st_element = stElement)
        return {'msg' : 'Element deleted'}, 204 
    
    @jwt_required
    def put(self, element_id):
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        if user is None:
            abort(500, message = 'Something gone wrong.')
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('filename', required = False)
        request_parser.add_argument('shared', required = False)
        request_parser.add_argument('upload_pass', required = False)
        request_data = request_parser.parse_args()
        stElement = StorageElModel.get_element(id = int(element_id))
        if stElement is None:
            abort(400, message = 'Element not found.')
        if not self.validate_user_access(user, stElement):
            abort(401)
        new_filename = request_data['filename']
        new_share_state = request_data['shared']
        upload_pass = request_data['upload_pass']
        if new_share_state is not None:
            if new_share_state == "True":
                if stElement.is_shared is False:
                    stElement.share(upload_pass)
            elif new_share_state == "False":
                stElement.disable_sharing()
        if new_filename is not None:
            stElement.set_filename(new_filename)
        stElement.save()
        return marshal(stElement, storage_element_fields, envelope="Storage element")
    
    @jwt_required
    def get(self, element_id):
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        if user is None:
            abort(500, message = 'Something gone wrong.')
        stElement = StorageElModel.get_element(id = int(element_id))
        if stElement is None:
            abort(400, message = 'Element not found.')
        if not self.validate_user_access(user, stElement):
            abort(401)
        try:
            result_file = stElement.get_file()
            return Response(result_file, mimetype=result_file.content_type, direct_passthrough=True)
        except Exception as e:
            abort(500, message = str(e))

    def validate_user_access(self, user, stElement):
        user_storage = user.storage.id
        return user_storage == stElement.storage_id 