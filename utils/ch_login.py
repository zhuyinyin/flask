from flask import url_for,redirect,session
from functools import wraps


def is_login(func):
    @wraps(func)
    def check_login(*args,**kwargs):
        user = session.get('username')
        if user:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return check_login