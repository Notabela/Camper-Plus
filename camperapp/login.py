from camperapp import login_manager
from flask_login import current_user
from flask import Response, abort
from functools import wraps
from camperapp.models import User

login_manager.login_view = 'login'


def requires_roles(*roles):
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
