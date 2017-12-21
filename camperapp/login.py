from camperapp import login_manager
from functools import wraps
from camperapp.models import User

login_manager.login_view = 'login'


# def requires_roles(*roles):
#     def wrapper(f):
#         @wraps(f)
#         def wrapped(*args, **kwargs):
#             if get_current_user_role() not in roles:
#                 return error_response()
#             return f(*args, **kwargs)
#         return wrapped
#     return wrapper

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
