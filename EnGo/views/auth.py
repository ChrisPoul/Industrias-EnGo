from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g
)
from . import permission_required, login_required
from EnGo.models.user.auth import UserAuth

bp = Blueprint("auth", __name__, url_prefix="/auth")
auth = UserAuth()


@bp.route("/register", methods=('POST', 'GET'))
@permission_required(["admin"])
@login_required
def register():
    if request.method == "POST":
        error = auth.register_user()
        if not error:
            flash("El usuario se registro correctamente")
        else:
            flash(error)

    return render_template(
        "auth/register.html"
    )


@bp.route("/login", methods=('POST', 'GET'))
def login():
    if g.user:
        return redirect(
            url_for('home.main_page')
        )
    if request.method == "POST":
        error = auth.login_user()
        if not error:
            return redirect(
                url_for('home.main_page')
            )
        flash(error)

    return render_template(
        "auth/login.html"
    )


@bp.route("/logout")
@login_required
def logout():
    auth.logout_user()

    return redirect(
        url_for("auth.login")
    )


@bp.before_app_request
def load_loged_in_user():
    auth.load_loged_in_user()
