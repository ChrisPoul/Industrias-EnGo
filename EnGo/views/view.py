from flask import (
    Blueprint, render_template, request
)
from EnGo.models.permission import Permission
from EnGo.models.view import View
from . import get_checked_permissions


bp = Blueprint('view', __name__, url_prefix="/view")


@bp.route('/update/<int:id>', methods=("POST", "GET"))
def update(id):
    view = View.get(id)
    permissions = Permission.get_all()
    if request.method == "POST":
        checked_permissions = get_checked_permissions()
        view.update_permissions(checked_permissions)

    return render_template(
        'view/update.html',
        permissions=permissions
    )