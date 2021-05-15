from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models.user.auth import UserAuth

bp = Blueprint("auth", __name__, url_prefix="/auth")
auth = UserAuth()


@bp.route("/login", methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        error = auth.login()
        if not error:
            return redirect(
                url_for('home.main_page')
            )
        flash(error)

    return render_template(
        "auth/login.html"
    )


@bp.route("/logout")
def logout():
    auth.logout()

    return redirect(
        url_for("auth.login")
    )


@bp.before_app_request
def load_loged_in_user():
    auth.load_loged_in_user()
