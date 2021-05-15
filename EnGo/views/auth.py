from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        auth = Auth()
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
    auth = Auth()
    auth.logout()

    return redirect(
        url_for("auth.login")
    )
