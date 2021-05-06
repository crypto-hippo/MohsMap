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

# def admin_site_login_required(f):
#    @wraps(f)
#    def admin_site_login_required_decorator(*args, **kwargs):
#        session = get_current_session()
#        admin_user_id = session.get("user_id")
#        if admin_user_id:
#            admin_user = AdminUser.get_by_id(admin_user_id)
#            if admin_user:
#                kwargs["user"] = admin_user
#                kwargs["session"] = session
#                return f(*args, **kwargs)
#            else:
#                return redirect(url_for("profile_blueprint.profile"))
#        else:
#            return redirect(url_for("auth_blueprint.signin"))
#    return admin_site_login_required_decorator




# def super_admin_site_login_required(f):
#    @wraps(f)
#    def admin_required_decorator(*args, **kwargs):
#        session = get_current_session()
#        super_admin_user_id = session.get("user_id")
#        if super_admin_user_id:
#            super_admin_user = AdminUser.get_by_id(user_id)
#            if super_admin_user.is_super_admin():
#                kwargs["user"], kwargs["session"] = super_admin_user, session
#                return f(*args, **kwargs)
#            else:
#                return redirect(url_for("profile_blueprint.profile"))
#        else:
#            return redirect(url_for("auth_blueprint.signin"))
#    return admin_required_decorator

# # if user is logged in and not admin, run route
# # else if user is admin, redirect to admin
# # if user is not logged in redirect to signin
# def customer_site_login_required(f):
#    @wraps(f)
#    def customer_site_login_required_decorator(*args, **kwargs):
#        session = get_current_session()
#        customer_user_id = session.get("user_id")
#        if customer_user_id:
#            customer_user = CustomerUser.get_by_id(customer_user_id)
#            if customer_user:
#                admin_users = CustomerUser.get_admin_schedules(customer_user.admin_viewing_tokens)