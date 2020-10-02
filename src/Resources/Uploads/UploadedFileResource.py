from flask_restful import Resource, abort, request, reqparse
from werkzeug import Response

from Models.UploadModel import UploadModel
from Models.UploadedFileModel import UploadedFileModel
from Serializers.UploadFields import upload_fields

class UploadedFileResource(Resource):
    def get(self):
        parser  = reqparse.RequestParser()
        parser.add_argument('upload_hash', help = 'upload_hash can\'t be blank', required = True, location = 'json')
        parser.add_argument('file_index', help = 'file_index can\'t be blank', required = True, location = 'json')
        parser.add_argument('upload_pass',default='', required = False, location = 'json')
        data = parser.parse_args()
        upload_hash = data['upload_hash']
        file_index = data['file_index']
        upload_password = data['upload_pass']
        try:
            result_file = UploadedFileModel.get_file_by_upload(upload_hash,upload_password, file_index)
            return Response(result_file, mimetype=result_file.content_type, direct_passthrough=False)
        except Exception as e:
            abort(404, message = str(e))