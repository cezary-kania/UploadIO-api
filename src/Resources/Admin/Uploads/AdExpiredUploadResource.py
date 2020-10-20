from flask_restful import Resource, marshal, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from Models.Uploads.UploadModel import UploadModel
from Models.Uploads.UploadedFileModel import UploadedFileModel
from Serializers.UploadFields import upload_fields
from Utils.JWT import admin_required

class AdExpiredUploadResource(Resource):
    
    @admin_required
    def delete(self):
        uploads = UploadModel.get_expired_uploads()
        deleted_uploads = UploadModel.delete_uploads(uploads)
        return {'msg' : f'{deleted_uploads} uploads deleted.'}, 204
    
    @admin_required   
    def get(self):
        uploads = UploadModel.get_expired_uploads()
        return marshal(uploads,upload_fields)
