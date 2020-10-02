from .UploadCheckResource import UploadCheckResource
from .UploadResource import UploadResource
from .UploadedFileResource import UploadedFileResource

url_prefix = '/uploads'

resources = [
    (UploadCheckResource, f'{url_prefix}/uploadcheck'),
    (UploadResource, f'{url_prefix}/upload'),
    (UploadedFileResource, f'{url_prefix}/uploadedfile')
]