from flask_restful import fields
storage_element_fields = {
    'id' : fields.Integer,
    'filename' : fields.String,
    'el_type' : fields.String,
    'mongo_id' : fields.String,
    'is_shared' : fields.Boolean,
    'share_url' : fields.String,
    'size' : fields.Integer
}