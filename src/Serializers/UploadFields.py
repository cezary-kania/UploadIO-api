from flask_restful import fields
upload_fields = {
    'url_hash' : fields.String,
    'Password' : fields.String(attribute='password'),
    'Exp_date' : fields.String(attribute='expiration_date')
}