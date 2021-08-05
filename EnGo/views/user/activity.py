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
    description="Descripción"
)
permissions = [
    "Recursos Humanos"
]


@bp.route("/assign_activity/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def assign_activity(id):
    if request.method == "POST":
        activity = UserActivity(
            user_id=id,
            title=request.form['title'],
            description=request.form['description']
        )
        error = activity.request.add()
        if not error:
            return redirect(
                url_for('user.profile', id=id)
            )
        flash(error)
        
    return render_template(
        "user/activity/assign.html",
        activity_heads=activity_heads
    )


@bp.route('/update_activity/<int:activity_id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update_activity(activity_id):
    activity = UserActivity.query.get(activity_id)
    if request.method == "POST":
        update_obj_attrs(activity, activity_heads)
        error = activity.request.update()
        if not error:
            return redirect(
                url_for('user.profile', id=activity.user_id)
            )
        flash(error)

    return render_template(
        'user/activity/update.html',
        activity_heads=activity_heads,
        activity=activity
    )
