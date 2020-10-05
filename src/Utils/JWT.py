from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_restful import abort

from Models.Users.UserModel import UserModel

jwt = JWTManager()

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['account_type'] != 'admin' or claims['account_type'] is None:
            abort(403)
        else:
            return fn(*args, **kwargs)
    return wrapper

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user =  UserModel.get_user(login = identity)
    if user is None:
        return {'account_type' : None}
    if user.account_type == 'admin':
         return {'account_type' : 'admin'}
    else:
        return {'account_type' : 'user'}