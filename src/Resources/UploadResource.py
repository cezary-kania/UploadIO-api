from flask_restful import Resource, marshal, abort, request

from Models.UploadModel import UploadModel
from Models.UploadedFileModel import UploadedFileModel
from Serializers.UploadFields import upload_fields

class UploadResource(Resource):
    def post(self):
        if 'files[]' not in request.files:
            abort(400, message = 'Invalid request')
        files_amount = len(request.files.getlist('files[]'))
        if files_amount <= 0 or files_amount > 5 or request.files.getlist('files[]')[0].filename == '':
            abort(400, message = 'Invalid files amount')
        new_upload = UploadModel(upload_pass = request.form['upload_pass'])
        new_upload.save()
        for index,file in enumerate(request.files.getlist('files[]'),1):
            uploaded_file = UploadedFileModel(new_upload.id,index, file)
            uploaded_file.save()
        return marshal(new_upload, upload_fields, envelope='Upload')
        
    def get(self, url_hash = None):
        if url_hash is None: # Getting all uploads is temporary 
            uploads = UploadModel.get_all_uploads()
            for upload in uploads:
                uploaded_files = upload.uploaded_files
                for file in uploaded_files:
                    print(file)
            return marshal(uploads,upload_fields, envelope='Uploads')
        else:
            upload = UploadModel.get_upload_by_url_hash(url_hash)
            if upload:
                return marshal(upload, upload_fields, envelope='Upload')
            abort(404, message='Invalid url hash')
