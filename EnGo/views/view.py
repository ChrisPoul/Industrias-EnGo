from flask import (
    Blueprint, render_template, request,
    redirect, url_for
)
from EnGo.models.permission import Permission
from EnGo.models.view import View
from . import get_checked_permissions


bp = Blueprint('view', __name__, url_prefix="/view")


@bp.route('/update/<int:id>', methods=("POST", "GET"))
def update(id):
    view = View.get(id)
    if request.method == "POST":
        checked_permissions = get_checked_permissions()
        view.update_permissions(checked_permissions)
        return redirect(
            url_for('admin.main_page')
        )

    return render_template(
        'view/update.html',
        view=view
    )