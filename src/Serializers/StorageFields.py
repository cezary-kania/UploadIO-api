from flask_restful import fields
from .StorageElementFields import storage_element_fields
storage_fields = {
    'used_space' : fields.Integer,
    'storage_elements' : fields.List(fields.Nested(storage_element_fields))
}