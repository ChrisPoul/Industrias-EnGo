from datetime import datetime
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g, session
)
from EnGo.models.user import User, UserActivity
from . import (
    permission_required, login_required,
    get_checked_permissions, get_form
)

bp = Blueprint("user", __name__, url_prefix="/user")

username_head = dict(
    username="Nombre de Usuario"
)
user_login_heads = dict(
    username_head,
    password="Contraseña"
)
user_heads = dict(
    user_login_heads,
    salary="Salario Mensual"
)
password_heads = dict(
    password="Escribe una contraseña...",
    password_confirm="Confirma la contraseña..."
)
weekday_heads = {
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado",
    7: "Domingo"
}
activity_heads = dict(
    title="Titulo",
    description="Descripsión",
    due_date="Fecha De Entrega"
)
permissions = [
    "Recursos Humanos"
]


@bp.route("/users", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def users():
    users = User.query.all()
    if request.method == "POST":
        user = User.search(request.form['search_term'])
        if user:
            return redirect(
                url_for('user.update', id=user.id)
            )

    return render_template(
        "user/users.html",
        user_heads=username_head,
        users=users
    )


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
        "user/register.html",
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
        "user/login.html",
        user_heads=user_login_heads
    )


@bp.route("/profile/<int:id>")
@permission_required(permissions)
@login_required
def profile(id):
    user = User.query.get(id)
    week_activities = user.get_week_activities(datetime.today())

    return render_template(
        "user/profile.html",
        weekday_heads=weekday_heads,
        week_activities=week_activities,
        user=user
    )


@bp.route("/assign_activity/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def assign_activity(id):
    if request.method == "POST":
        error = None
        due_date_str = request.form["due_date"]
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            error = "No has seleccionado una fecha, porfavor selecciona una"
        if not error:
            activity = UserActivity(
                user_id=id,
                title=request.form['title'],
                description=request.form['description'],
                due_date=due_date
            )
            error = activity.request.add()
        if not error:
            return redirect(
                url_for('user.profile', id=id)
            )
        flash(error)
        
    return render_template(
        "user/assign_activity.html",
        activity_heads=activity_heads,
        form=request.form
    )


@bp.route("/update/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update(id):
    user = User.get(id)
    user_heads = dict(
        username_head,
        salary="Salario"
    )
    if request.method == "POST":
        user.username = request.form["username"]
        user.salary = request.form['salary']
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
