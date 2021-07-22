from datetime import datetime, timedelta
from flask import (
    render_template, request,
    flash, redirect, url_for
)
from EnGo.models.user import User, UserActivity
from EnGo.views import (
    permission_required, login_required,
    update_obj_attrs
)
from . import bp

activity_heads = dict(
    title="Título",
    description="Descripción",
    status="Estatus",
    due_date="Fecha De Entrega"
)
activity_status_options = [
    "Incompleta",
    "Completada",
    "Cancelada"
]
permissions = [
    "Recursos Humanos"
]


@bp.route("/assign_activity/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def assign_activity(id):
    min_date = datetime.today().strftime("%Y-%m-%d")
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
        "user/activity/assign.html",
        activity_heads=activity_heads,
        min_date=min_date
    )


@bp.route('/update_activity/<int:activity_id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update_activity(activity_id):
    activity = UserActivity.query.get(activity_id)
    min_date = datetime.today().strftime("%Y-%m-%d")
    if request.method == "POST":
        update_obj_attrs(activity, activity_heads)
        due_date_str = request.form['due_date']
        try:
            activity.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            error = activity.request.update()
        except ValueError:
            error = "Fecha invalida"
        if not error:
            return redirect(
                url_for('user.profile', id=activity.user_id)
            )
        flash(error)

    return render_template(
        'user/activity/update.html',
        activity_heads=activity_heads,
        activity_status_options=activity_status_options,
        min_date=min_date,
        activity=activity
    )


@bp.route('/day_activities/<int:id>/<string:date_str>')
@permission_required(permissions)
@login_required
def day_activities(id, date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    user = User.query.get(id)
    day_activities = user.schedule.get_day_activities(date)
    check_for_overdue_activities(day_activities)
    
    return render_template(
        'user/activity/day-activities.html',
        activity_status_options=activity_status_options,
        user=user,
        activities=day_activities,
        date=date
    )


def check_for_overdue_activities(activities):
    for activity in activities:
        if activity_is_overdue(activity):
            activity.status = "Atrasada"
            activity.update()


def activity_is_overdue(activity):
    return activity.due_date < datetime.today() - timedelta(days=1) and activity.status == "Incompleta"
