from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g, session
)
from . import (
    permission_required, login_required,
    update_obj_attrs
)
from EnGo.models.user import User

bp = Blueprint("user", __name__, url_prefix="/user")

user_heads = dict(
    username="Nombre de usuario",
    password="Contraseña"
)
permissions = [
    "admin"
]


@bp.route("/users")
def users():
    users = User.get_all()

    return render_template(
        "user/users.html",
        user_heads=user_heads,
        users=users
    )


@bp.route("/register", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        error = user.request.register()
        if not error:
            flash("El usuario se registro correctamente")
        else:
            flash(error)

    return render_template(
        "user/register.html",
        user_heads=user_heads
    )


@bp.route("/login", methods=('POST', 'GET'))
def login():
    if g.user:
        return redirect(
            url_for('home.main_page')
        )
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        error = user.request.login()
        if not error:
            return redirect(
                url_for('home.main_page')
            )
        flash(error)

    return render_template(
        "user/login.html",
        user_heads=user_heads
    )


@bp.route("/update/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update(id):
    user = User.get(id)
    if request.method == "POST":
        update_obj_attrs(user, user_heads)
        error = user.request.update()

    return render_template(
        "user/update.html",
        user_heads=user_heads
    )


@bp.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect(
        url_for("user.login")
    )


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    user = User.get(id)
    user.delete()

    return redirect(
        url_for('user.users')
    )


@bp.before_app_request
def load_loged_in_user():
    try:
        user_id = session["user_id"]
    except KeyError:
        user_id = None

    if user_id is None:
        g.user = None
    else:
        g.user = User.get(user_id)
