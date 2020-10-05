from flask_restful import Resource, marshal, abort, request, reqparse

from Models.Uploads.UploadModel import UploadModel
from Models.Uploads.UploadedFileModel import UploadedFileModel
from Serializers.UploadFields import upload_fields
from Utils.file_operators import get_file_size, GigaByte

class UploadResource(Resource):
    def post(self):
        if 'files[]' not in request.files:
            abort(400, message = 'Invalid request')
        files = request.files.getlist('files[]')
        files_amount = len(files)
        if files_amount <= 0 or files_amount > 5 or files[0].filename == '':
            abort(400, message = 'Invalid files amount')
        request_size = 0
        for file in files:
            request_size += get_file_size(file)
        
        if request_size > GigaByte:
            abort(400, message = 'Maximum upload size is 1GB.')
        upload_pass = request.form['upload_pass']
        days_to_expire = request.form['days_to_expire']
        days_to_expire = 1 if days_to_expire is None or days_to_expire not in [1, 2, 7, 14] else int(days_to_expire)
        new_upload = UploadModel(upload_pass,days_to_expire)
        new_upload.size = request_size
        new_upload.save()
        for index,file in enumerate(files,1):
            uploaded_file = UploadedFileModel(file,index)
            uploaded_file.upload = new_upload
            uploaded_file.save()
        
        return marshal(new_upload, upload_fields, envelope='Upload')
        
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('upload_hash', required = True, location = 'json')
        parser.add_argument('upload_pass', required = False, location = 'json')
        request_data = parser.parse_args()
        url_hash = request_data['upload_hash']
        upload_pass = request_data['upload_pass']
        upload = UploadModel.get_upload_by_url_hash(url_hash)
        if upload is None:
            abort(404, message='Invalid url hash')
        if not upload.check_expiration_time():
            abort(400, message='Upload expired')
        if not upload.check_is_active():
            abort(400, message='Upload not active')
        if upload.is_pass_required():
            if upload_pass is None or (not upload.verify_pass(upload_pass)):
                abort(400, message = 'Invalid password')
        return marshal(upload, upload_fields, envelope='Upload')

