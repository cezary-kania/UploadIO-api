from flask_restful import Resource, marshal, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from Models.Uploads.UploadModel import UploadModel
from Models.Uploads.UploadedFileModel import UploadedFileModel
from Serializers.UploadFields import upload_fields
from Utils.JWT import admin_required

class AdUploadResource(Resource):
    
    @admin_required
    def delete(self):
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
    
    @admin_required   
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

