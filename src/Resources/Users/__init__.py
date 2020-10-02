from .Auth import resources as auth_resources 

url_prefix = '/users'

resources = auth_resources

resources = [(res, url_prefix + endpoint) for (res, endpoint) in resources]