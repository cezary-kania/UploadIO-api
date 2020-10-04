from flask_restful import Resource, abort, reqparse

from Models.Uploads.UploadModel import UploadModel

class UploadCheckResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('upload_hash', help='upload_hash can\'t be empty', required = True, location = 'json')
        request_data = parser.parse_args()
        url_hash = request_data['upload_hash']
        upload = UploadModel.get_upload_by_url_hash(url_hash)
        if upload is None:
            abort(404, message='Invalid url hash')
        if not upload.check_expiration_time():
            abort(400, message='Upload expired')
        pass_required = upload.is_pass_required()
        return {'status' : 'active', 'pass_required' : pass_required}, 200