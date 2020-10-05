from flask_restful import Resource, marshal, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from Models.Uploads.UploadModel import UploadModel
from Models.Uploads.UploadedFileModel import UploadedFileModel
from Serializers.UploadFields import upload_fields


class UploadResource(Resource):
    
    @jwt_required
    def delete(self):
        from Models.Users.UserModel import UserModel
        user_identity = get_jwt_identity()
        user = UserModel.get_user(login = user_identity)
        if user is None:
            abort(500, message = 'Something gone wrong.')
        if user.account_type != 'admin':
            abort(403)
        parser = reqparse.RequestParser()
        parser.add_argument('upload_hash', required = False, location = 'json')
        request_data = parser.parse_args()
        url_hash = request_data['upload_hash']
        if url_hash is None: 
            deleted_rows = UploadModel.delete_all_uploads()
            return {'msg' : f'{deleted_rows} rows deleted.'}, 204
        upload = UploadModel.get_upload_by_url_hash(url_hash)
        if upload is None:
            abort(404, message='Invalid url hash')
            upload.delete()
        return {'msg' : 'Upload deleted'}, 204
        
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('upload_hash', required = False, location = 'json')
        request_data = parser.parse_args()
        url_hash = request_data['upload_hash']
        if url_hash is None:
            uploads = UploadModel.get_all_uploads()
            return marshal(uploads,upload_fields, envelope='Uploads')
        upload = UploadModel.get_upload_by_url_hash(url_hash)
        if upload is None:
            abort(404, message='Invalid url hash')
        return marshal(upload, upload_fields, envelope='Upload')

