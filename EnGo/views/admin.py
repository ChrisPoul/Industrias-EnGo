from flask import (
    Blueprint, render_template, g,
    session, request
)
from . import permission_required
from EnGo.models.permission import Permission, UserPermission
from EnGo.models.user import User

bp = Blueprint('admin', __name__, url_prefix="/admin")


@bp.route("/main_page", methods=('POST', 'GET'))
@permission_required("admin")
def main_page():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User(
            username=username,
            password=password
        )
        user.add()

    return render_template(
        "admin/main-page.html"
    )
