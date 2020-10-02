from .UserRegistrationResource import UserRegistrationResource
from .UserLoginResource import UserLoginResource

url_prefix = '/auth'

resources = [
    (UserRegistrationResource, f'{url_prefix}/register'),
    (UserLoginResource, f'{url_prefix}/login'),
]