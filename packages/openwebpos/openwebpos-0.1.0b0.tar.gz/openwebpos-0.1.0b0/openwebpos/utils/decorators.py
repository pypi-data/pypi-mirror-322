from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def permission_required(permission: str):
    """
    Check if the current user has the required permission to access a specific resource or perform an action.
    If the user does not have the necessary permission, they are redirected to the home page with a flash
    message.

    :param permission: The specific permission required for the user to access the resource or perform the action.
    :type permission: str
    :return: A decorator that applies the permission check to the decorated function.
    :rtype: Callable
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role.has_permission(permission):
                flash("You do not have permission to do that.", "danger")
                return redirect(url_for("user.home"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator
