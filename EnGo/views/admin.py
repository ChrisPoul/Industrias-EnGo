from flask import (
    Blueprint, render_template, request,
    flash
)
from . import permission_required
from EnGo.models.permission import Permission, UserPermission
from EnGo.models.user.auth import Auth

bp = Blueprint('admin', __name__, url_prefix="/admin")


@bp.route("/main_page", methods=('POST', 'GET'))
@permission_required("admin")
def main_page():
    if request.method == "POST":
        auth = Auth()
        error = auth.register()

        if not error:
            flash("El usuario se registro correctamente")
        else:
            flash(error)

    return render_template(
        "admin/main-page.html"
    )
