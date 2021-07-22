from datetime import datetime
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g, session
)
from EnGo.models.user import User, UserActivity, UserProduction
from EnGo.models.calendar import MyCalendar, weekday_heads
from EnGo.views import (
    permission_required, login_required,
    get_checked_permissions, get_form,
    update_obj_attrs
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
production_heads = dict(
    concept="Concepto",
    quantity="Cantidad",
    date="Fecha de Registro"
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
                url_for('user.profile', id=user.id)
            )

    return render_template(
        "user/users.html",
        user_heads=username_head,
        users=users
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


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    user = User.get(id)
    user.delete()

    return redirect(
        url_for('user.users')
    )


@bp.route("/profile/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def profile(id):
    user = User.query.get(id)
    selected_date = datetime.today()
    selected_week_str = selected_date.strftime("%Y-W%W")
    if request.method == "POST":
        selected_week_str = request.form["selected_week"]
        selected_date = datetime.strptime(selected_week_str + "-1", "%Y-W%W-%w")
    week_activities = user.schedule.get_weekday_activities(selected_date)
    week_production = user.schedule.get_week_production(selected_date)
    weekday_dates = MyCalendar.get_weekday_dates(selected_date)

    return render_template(
        "user/profile.html",
        weekday_heads=weekday_heads,
        production_heads=production_heads,
        week_activities=week_activities,
        weekday_dates=weekday_dates,
        user_production=week_production,
        selected_week_str=selected_week_str,
        user=user
    )


@bp.route('/register_production/<int:user_id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def register_production(user_id):
    if request.method == "POST":
        production = UserProduction(
            user_id=user_id,
            concept=request.form['concept'],
            quantity=request.form['quantity']
        )
        error = production.request.add()
        if not error:
            return redirect(
                url_for('user.profile', id=user_id)
            )
        flash(error)
    
    return render_template(
        "user/production/register-production.html",
        production_heads=production_heads
    )


@bp.route('/production/<int:user_id>')
@permission_required(permissions)
@login_required
def production(user_id):
    user = User.query.get(user_id)
    user_production = user.production

    return render_template(
        "user/production/production.html",
        production_heads=production_heads,
        user_production=user_production,
        user=user
    )
    
from . import auth, activity