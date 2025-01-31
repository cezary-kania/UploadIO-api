from flask_restful import Resource, abort, request, reqparse
from werkzeug import Response
from Models import gfs
from bson import ObjectId
from Models.Uploads.UploadModel import UploadModel
from Models.Uploads.UploadedFileModel import UploadedFileModel
from Serializers.UploadFields import upload_fields

class UploadedFileResource(Resource):
    def get(self):
        parser  = reqparse.RequestParser()
        parser.add_argument('upload_hash', help = 'upload_hash can\'t be blank', required = True, location = 'args')
        parser.add_argument('file_index', help = 'file_index can\'t be blank', required = True, location = 'args')
        parser.add_argument('uploadPass',default='', required = False, location = 'headers')
        data = parser.parse_args()
        upload_hash = data['upload_hash']
        file_index = data['file_index']
        upload_password = data['uploadPass']
        try:
            result_file = UploadedFileModel.get_file_by_upload(upload_hash,upload_password,file_index)
            return Response(result_file, mimetype=result_file.content_type, direct_passthrough=True)
        except Exception as e:
            abort(400, message = str(e))