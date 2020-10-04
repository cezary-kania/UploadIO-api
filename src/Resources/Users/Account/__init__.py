from .AccountDeleteResource import AccountDeleteResource
from .PasswordChangeResource import PasswordChangeResource
url_prefix = '/account'

resources = [
    (AccountDeleteResource, f'{url_prefix}/delete_account'),
    (PasswordChangeResource, f'{url_prefix}/change_password')
]