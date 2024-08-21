from functools import wraps
from flask import url_for, redirect, request, session
import logging


def site_login_required(f):
    @wraps(f)
    def site_login_required_decorator(*args, **kwargs):
        authenticated = session.get("admin_authenticated", None)
        if authenticated:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("admin"))

    return site_login_required_decorator
