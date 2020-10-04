from .Auth import resources as auth_resources 
from .Storage import resources as storage_resources

url_prefix = '/users'

resources = auth_resources + storage_resources 

resources = [(res, url_prefix + endpoint) for (res, endpoint) in resources]