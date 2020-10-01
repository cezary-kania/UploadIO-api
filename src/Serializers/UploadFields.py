from flask_restful import fields
from Serializers.UploadedFileFields import uploaded_file_fields
upload_fields = {
    'url_hash' : fields.String,
    'Password' : fields.String(attribute='password'),
    'expiration_date' : fields.String,
    'uploaded_files' : fields.List(fields.Nested(uploaded_file_fields))
}