from datetime import datetime
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g, session
)
from EnGo.models.user import User
from EnGo.models.calendar import MyCalendar, weekday_heads
from EnGo.views import (
    permission_required, login_required,
    get_checked_permissions, get_form,
    update_obj_attrs
)
from EnGo.views.production import production_heads

bp = Blueprint("user", __name__, url_prefix="/user")

username_head = dict(
    username="Nombre de Usuario"
)
user_heads = dict(
    username_head,
    password="Contraseña",
    salary="Salario Mensual"
)
permissions = [
    "Recursos Humanos"
]

from . import auth


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
    week_finished_orders = user.schedule.get_finished_week_orders(selected_date)
    week_pending_orders = user.schedule.get_pending_week_orders(selected_date)
    week_production = user.schedule.get_week_production(selected_date)
    weekday_dates = MyCalendar.get_weekday_dates(selected_date)

    return render_template(
        "user/profile.html",
        weekday_heads=weekday_heads,
        production_heads=production_heads,
        week_activities=week_activities,
        week_finished_orders=week_finished_orders,
        week_pending_orders=week_pending_orders,
        weekday_dates=weekday_dates,
        production=week_production,
        selected_week_str=selected_week_str,
        user=user
    )


@bp.route('/day_assignments/<int:user_id>/<string:date_str>')
@permission_required(permissions)
@login_required
def day_assignments(user_id, date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    user = User.query.get(user_id)
    day_activities = user.schedule.get_day_activities(date)
    day_orders = user.schedule.get_day_orders(date)
    
    return render_template(
        'user/day-assignments.html',
        user=user,
        date=date,
        activities=day_activities,
        orders=day_orders
    )
