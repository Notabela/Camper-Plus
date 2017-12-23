from functools import wraps
from flask_login import current_user
from flask import abort
from camperapp.models import User
from camperapp import login_manager

login_manager.login_view = 'login'


def requires_roles(*roles):
    """
    Wrapper to Allow Routes Function to only be
    run if current flask login user has Role
    :param roles: Role.admin or Role.parent or both
    :return: function is role is met, abort if unauthorized access
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
