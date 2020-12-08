from functools import wraps

from flask import flash, redirect, url_for, request
from flask_login import current_user

from webapp import models


def login_required_Admin(f):
    """
    bắt buộc đăng nhập với quyền admin
    :param f: function
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or not current_user.is_authenticated or current_user.role != models.Role.admin:
            flash('Please login to access this page.')

            return redirect(url_for('login_admin', next=request.url_rule))
        return f(*args, **kwargs)

    return decorated_function


def login_required_user(f):
    """
    bắt buộc đăng nhập với quyền editor
    :param f: function
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or not current_user.is_authenticated or current_user.role != models.Role.manager:
            flash('Please login to access this page.')
            return redirect(url_for('login_us', next=request.url_rule))
        return f(*args, **kwargs)

    return decorated_function
