from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g, session
)
from . import (
    permission_required, login_required,
    update_obj_attrs, get_checked_permissions
)
from EnGo.models.user import User

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


@bp.route("/users", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def users():
    users = User.get_all()
    if request.method == "POST":
        user = User.search(request.form['search_term'])
        if user:
            return redirect(
                url_for('user.update', id=user.id)
            )

    return render_template(
        "user/users.html",
        user_heads=users_heads,
        users=users
    )


@bp.route("/register", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def register():
    if request.method == "POST":
        user = User(
            username=request.form['username'],
            password=request.form['password']
        )
        error = user.request.register()
        if not error:
            checked_permissions = get_checked_permissions()
            user.add_permissions(checked_permissions)
            return redirect(
                url_for('user.users')
            )
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
    user_heads = dict(
        username="Nombre del empleado"
    )
    if request.method == "POST":
        user.username = request.form["username"]
        checked_permissions = get_checked_permissions()
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
        user=user
    )


@bp.route("/update_password/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update_password(id):
    user = User.get(id)
    password_heads = dict(
        password="Escribe una contraseña...",
        password_confirm="Confirma la contraseña..."
    )
    if request.method == "POST":
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        if password != password_confirm:
            error = "Las contraseñas no coinciden"
        else:
            user.password = password
            error = user.validation.validate()
        if not error:
            from werkzeug.security import generate_password_hash
            user.password = generate_password_hash(user.password)
            user.update()
            return redirect(
                url_for('user.update', id=id)
            )
        flash(error)
    
    return render_template(
        'user/update_password.html',
        password_heads=password_heads,
        user=user
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
