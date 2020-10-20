
from .AdUploadResource import AdUploadResource
from .AdExpiredUploadResource import AdExpiredUploadResource

url_prefix = '/uploads'

resources = [
    (AdUploadResource, f'{url_prefix}'),
    (AdExpiredUploadResource, f'{url_prefix}/expired')
]