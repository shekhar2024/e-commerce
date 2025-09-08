from functools import wraps
from flask_jwt_extended import get_jwt
from flask import current_app as app

def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {"message": "Only admin can access this resource."}, 403
        return func(*args, **kwargs)
    return inner

def user_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        claims = get_jwt()
        if claims.get("is_admin", False):
            return {"message": "Only user can access this resource."}, 403
        return func(*args, **kwargs)
    return inner
   