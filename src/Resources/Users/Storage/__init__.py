from .UserStorageResource import UserStorageResource
from .StorageElementResource import StorageElementResource
url_prefix = '/storage'

resources = [
    (UserStorageResource, f'{url_prefix}/'),
    (StorageElementResource, f'{url_prefix}/st_element/<int:element_id>')
]