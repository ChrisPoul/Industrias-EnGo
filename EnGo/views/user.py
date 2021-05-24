from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g, session
)
from . import (
    permission_required, login_required,
    update_obj_attrs
)
from EnGo.models.user import User
from EnGo.models.permission import Permission

bp = Blueprint("user", __name__, url_prefix="/user")

users_heads = dict(
    username="Nombre de Usuario"
)
user_heads = dict(
    users_heads,
    password="Contraseña"
)
permissions = [
    "recursos humanos"
]


@bp.route("/users")
@permission_required(permissions)
@login_required
def users():
    users = User.get_all()

    return render_template(
        "user/users.html",
        user_heads=users_heads,
        users=users
    )


@bp.route("/register", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def register():
    permissions = Permission.get_all()
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        error = user.request.register()
        if not error:
            checked_permissions = get_checked_permissions(permissions)
            user.add_permissions(checked_permissions)
            return redirect(
                url_for('user.users')
            )
        flash(error)

    return render_template(
        "user/register.html",
        user_heads=user_heads,
        permissions=permissions
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
    permissions = Permission.get_all()
    if request.method == "POST":
        update_obj_attrs(user, user_heads)
        checked_permissions = get_checked_permissions(permissions)
        user.update_permissions(checked_permissions)
        error = user.request.update()
        if not error:
            return redirect(
                url_for('user.users')
            )
        flash(error)

    return render_template(
        "user/update.html",
        user_heads=user_heads,
        user=user,
        permissions=permissions
    )


def get_checked_permissions(permissions):
    checked_permissions = []
    for permission in permissions:
        try:
            permission_id = request.form[permission.permission_name]
            checked_permissions.append(permission)
        except KeyError:
            pass

    return checked_permissions


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
