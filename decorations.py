from functools import wraps
from flask import g, redirect, url_for

def admin_login(func):
    @wraps(func)
    def verify(*args, **kwargs):
        if g.user and g.user.isAdmin():
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login_form'))
    return verify


def user_login(func):
    @wraps(func)
    def verify(*args, **kwargs):
        # print(g.user, "1111")
        if g.user and not g.user.isAdmin():
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login_form'))
    return verify