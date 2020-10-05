from .Uploads import resources as uploads_resources 
from .Users import resources as users_resources
url_prefix = '/admin'

resources = uploads_resources + users_resources

resources = [(res, url_prefix + endpoint) for (res, endpoint) in resources]