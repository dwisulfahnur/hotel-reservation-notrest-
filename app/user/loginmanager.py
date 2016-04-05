import app
from flask import flash, redirect, url_for, abort
from functools import wraps
from flask.ext.login import LoginManager, current_user, login_required
from models import User, UserRoles

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
login_manager.login_view = "user.login"
login_manager.login_message = "Please log in to access this page"

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
	            flash("You've got no permission to access this page.")
            if get_current_user_role() not in roles:
                return error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def error_response():
    flash("You've got no permission to access this page.") 
    return abort(403)

def get_current_user_role():
	user_role = UserRoles.query.filter_by(user_id=current_user.id).first()
	return user_role.role.role
