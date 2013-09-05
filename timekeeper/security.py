from passlib.apps import custom_app_context as pwd_context

from pyramid.security import (
        Allow,
        Everyone,
        )

from .models import (
        DBSession,
        Employee,
        )

def generate_user_password(password):
    return pwd_context.encrypt(password)

def authenticate_user(login, password):
    user = DBSession.query(Employee).filter_by(login=login).first()
    if user is None or not user.active:
        return None

    valid, new_hash = pwd_context.verify_and_update(password, user.password_hash)
    if new_hash:
        user.password_hash = new_hash

    if valid:
        return user
    else:
        return None

def authentication_policy(userid, request):
    user = DBSession.query(Employee).get(userid)
    if user is None or not user.active:
        return None

    if user.admin:
        return ['group:admins']
    else:
        return []

class RootFactory(object):
    __acl__ = [
            (Allow, Everyone, 'clock'),
            (Allow, 'group:admins', 'report'),
            (Allow, 'group:admins', 'manage'),
            ]

    def __init__(self, request):
        pass
