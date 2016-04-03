import app
import datetime
from flask import (Blueprint, 
                   render_template,
                   request,
                   flash,
                   redirect,
                   url_for,
                   abort,
                   views,
                   session)
from flask.ext.login import (login_user, 
                             current_user,
                             login_required,
                             logout_user)
from app.core.db import db
from models import User, UserRoles, Roles
from flask.ext.bcrypt import check_password_hash
from sqlalchemy.exc import IntegrityError

user_views = Blueprint('user', __name__, template_folder='../templates/user', static_folder='../static')

@user_views.route("/home/")
def home():
    user=current_user
    return render_template("home.html", **locals())

@user_views.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You're logged in")
        return redirect(url_for('hotel.hotel_view'))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #Validate Forms
        #Return Errors if failed to validate
        errors = []
        if not username:
            errors.append(dict(field="username", msg="Username can't empty"))
        if not password:
            errors.append(dict(field="password", msg="Password can't empty"))

        #Valitaing User 
        #Give session to user if forms has been Validated
        if len(errors) == 0:
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash("You're logged in")
                    return redirect(url_for('hotel.hotel_view'))
            errors.append(dict(field="username", msg="Username or Password is wrong!"))
    return render_template("login.html", **locals())

@user_views.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You're logged in")
        return redirect(url_for('hotel.hotel_view'))
    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        email = request.form.get("email")
        address = request.form.get("address")
        phone_number = request.form.get("phone_number")
        password = unicode(request.form.get("password"))
        password_confirm = unicode(request.form.get("password_confirm"))

        #Validate Forms and User data
        #Send error message if not valid or empty
        errors = []
        if fullname == "":
            errors.append(dict(field="fullname", msg="Fullname is not valid"))

        if User.query.filter_by(username=username).first() or not username:
            errors.append(dict(field="username", msg="Username is not valid"))

        if '@' not in email or User.query.filter_by(email=email).first() or not email:
            errors.append(dict(field="email", msg="Email not valid or has been used"))

        if not address:
            errors.append(dict(field="address", msg="Address not valid"))

        if User.query.filter_by(phone_number=phone_number).first() or not phone_number:
            errors.append(dict(field="phone_number", msg="Number Phone is not valid"))

        if not password:
            errors.append(dict(field="password", msg="Password is not valid"))

        if not(password_confirm == password):
            errors.append(dict(field="password_confirm", msg="Password must match"))

        #Append user data to Database if not Failed to validate
        if len(errors) == 0:
            user = User(fullname=fullname,
                        username=username,
                        email=email,
                        address=address,
                        phone_number=phone_number,
                        password=password)
            db.session.add(user)
            as_user = Roles.query.filter_by(role='user').first()
            user_role = UserRoles(role_id=as_user.id,
                                  user_id=user.id)
            db.session.add(user_role)
            db.session.commit()
            flash("Your account has been registered")
    return render_template("register.html", **locals())

@user_views.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()
    flash("You're logged out")
    return redirect(url_for('user.login'))