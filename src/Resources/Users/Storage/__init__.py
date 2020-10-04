from .UserStorageResource import UserStorageResource

url_prefix = '/storage'

resources = [
    (UserStorageResource, f'{url_prefix}/')
]