from .AdUserResource import AdUserResource
from .AdUserRoleResource import AdUserRoleResource

url_prefix = '/users'

resources = [
    (AdUserResource, f'{url_prefix}'),
    (AdUserRoleResource, f'{url_prefix}/account_type')
]