from flask_restful import Resource, marshal, abort

from Models.UploadModel import UploadModel
from Serializers.UploadFields import upload_fields

class UploadResource(Resource):
    def post(self):
        new_upload = UploadModel()
        new_upload.save()
        return {'status' : 'ok'}, 200
    def get(self, url_hash = None):
        if url_hash is None:
            uploads = UploadModel.get_all_uploads()
            return marshal(uploads,upload_fields, envelope='Uploads')
        else:
            upload = UploadModel.get_upload_by_url_hash(url_hash)
            if upload:
                return marshal(upload, upload_fields, envelope='Upload')
            abort(404, message='Invalid url hash')
