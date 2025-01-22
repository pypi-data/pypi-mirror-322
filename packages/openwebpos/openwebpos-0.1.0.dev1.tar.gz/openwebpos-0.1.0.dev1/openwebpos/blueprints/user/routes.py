from urllib.parse import urlsplit

from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required, login_user, logout_user

from openwebpos.blueprints.product.models import OrderType
from .forms import LoginForm
from .models.user import User

user_bp = Blueprint("user", __name__, template_folder="templates")


@user_bp.route("/")
@login_required
def home():
    """Home page"""
    order_types = OrderType.list_active_and_visible()
    context = {
        "title": "Home",
        "order_types": order_types,
    }
    return render_template("user/home.html", **context)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    form = LoginForm()
    context = {
        "title": "Login",
        "form": form,
    }
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        print(user)
        if user and user.check_password(form.password.data):
            if user.is_active:
                login_user(user, remember=form.remember_me.data)
                flash(
                    "Logged in successful. Welcome back {}!".format(user.username),
                    "success",
                )
                next_page = request.args.get("next")
                if not next_page or urlsplit(next_page).netloc != "":
                    next_page = url_for("user.home")
                return redirect(next_page)
            else:
                flash(
                    "Your account is not activated yet. please check back later",
                    "danger",
                )
        else:
            flash("Invalid username or password.", "danger")

    return render_template("user/login.html", **context)


@user_bp.route("/logout")
@login_required
def logout():
    """Logout page"""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("user.login"))
