from flask_restful import fields

user_fields = {
    'login' : fields.String,
    'email' : fields.String,
    'account_type' : fields.String,
    'account_creation_date' : fields.String,
}