from flask_restful import fields
from Serializers.UploadedFileFields import uploaded_file_fields
upload_fields = {
    'url_hash' : fields.String,
    'expiration_date' : fields.String,
    'has_expired' : fields.Boolean,
    'password' : fields.String,
    'uploaded_files' : fields.List(fields.Nested(uploaded_file_fields))
}