from flask import (
    render_template, request,
    flash, redirect, url_for,
    g, session
)
from EnGo.models.user import User
from EnGo.views import (
    permission_required, login_required,
    get_checked_permissions, get_form
)
from . import bp, user_heads

user_login_heads = dict(
    username="Nombre de Usuario",
    password="Contraseña"
)
password_heads = dict(
    password="Escribe una contraseña...",
    password_confirm="Confirma la contraseña..."
)
permissions = [
    "Recursos Humanos"
]


@bp.route("/register", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def register():
    form = get_form(user_heads)
    if request.method == "POST":
        error = None
        if form["password"] != request.form["password_confirm"]:
            error = "Las contraseñas no coinciden"
        if not error:
            user = User(
                username=form['username'],
                password=form['password'],
                salary=form['salary']
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
        "user/auth/register.html",
        user_heads=user_heads,
        password_heads=password_heads,
        form=form
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
        "user/auth/login.html",
        user_heads=user_login_heads
    )


@bp.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect(
        url_for("user.login")
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


@bp.route("/update_password/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update_password(id):
    user = User.get(id)
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
        'user/auth/update-password.html',
        password_heads=password_heads,
        user=user
    )
