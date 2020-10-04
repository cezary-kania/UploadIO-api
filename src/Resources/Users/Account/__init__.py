from .AccountDeleteResource import AccountDeleteResource

url_prefix = '/account'

resources = [
    (AccountDeleteResource, f'{url_prefix}/delete_account'),
]