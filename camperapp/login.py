"""
.. module:: camperapp.login
   :platform: Unix, Windows
   :synopsis: Login functions for flask_login

.. moduleauthor:: Daniel Obeng, Chris Kwok, Eric Kolbusz, Zhirayr Abrahamyam

"""
from functools import wraps
from flask_login import current_user
from flask import abort
from camperapp.models import User
from camperapp import login_manager

login_manager.login_view = 'login'


def requires_roles(*roles):
    """Wrapper Function to restrict access to endpoints

       Functions with this as a wrapper will only execute
       if the flask_login current_user has a role from ``Role class``
       specified in this function's input

       Args:
           roles (any) : roles

       Returns:
            A wrapped version of the original function that will only
            run if current_user.role is in roles

       Raises:
           werkzeug.exceptions.Unauthorized: An error occurred if current_user.role is not in roles
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
    """Retrieve user with id user_id from database

        Retrieves the user with the specified user_id from
        the Users table in the database

        Args:
           user_id (int) : id of user to be queried

        Returns:
            sql_alchemy user object with specified user_id
    """
    return User.query.get(int(user_id))
