from datetime import datetime, timedelta
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models.user import User
from EnGo.models.activity import Activity
from EnGo.views import (
    permission_required, login_required,
    update_obj_attrs
)

bp = Blueprint("activity", __name__, url_prefix="/activity")

activity_heads = dict(
    title="Título",
    description="Descripción",
    user_id="Empleado"
)
permissions = [
    "Recursos Humanos"
]


@bp.route("/assign", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def assign():
    users = [user for user in User.query.all() if not user.is_admin()]
    selected_user = dict(
        id=0,
        username="Seleccionar Empleado"
    )
    if request.method == "POST":
        activity = Activity(
            user_id=request.form['user_id'],
            title=request.form['title'],
            description=request.form['description']
        )
        error = activity.request.add()
        if not error:
            return redirect(
                url_for('user.profile', id=activity.user_id)
            )
        flash(error)
        
    return render_template(
        "activity/assign.html",
        activity_heads=activity_heads,
        selected_user=selected_user,
        users=users
    )


@bp.route('/update/<int:activity_id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update(activity_id):
    activity = Activity.query.get(activity_id)
    users = [user for user in User.query.all() if not user.is_admin()]
    selected_user = activity.user
    if request.method == "POST":
        update_obj_attrs(activity, activity_heads)
        error = activity.request.update()
        if not error:
            return redirect(
                url_for('user.profile', id=activity.user_id)
            )
        flash(error)

    return render_template(
        'activity/update.html',
        activity_heads=activity_heads,
        selected_user=selected_user,
        users=users,
        activity=activity
    )
