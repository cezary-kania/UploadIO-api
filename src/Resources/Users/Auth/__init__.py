from .UserRegistrationResource import UserRegistrationResource
from .UserLoginResource import UserLoginResource
from .AccessTokenRefResource import AccessTokenRefResource

url_prefix = '/auth'

resources = [
    (UserRegistrationResource, f'{url_prefix}/register'),
    (UserLoginResource, f'{url_prefix}/login'),
    (AccessTokenRefResource, f'{url_prefix}/get_access_token')
]