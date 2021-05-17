from flask import (
    Blueprint, render_template, request,
    flash
)
from . import permission_required, login_required

bp = Blueprint('admin', __name__, url_prefix="/admin")

@bp.route("/main_page", methods=('POST', 'GET'))
@permission_required(["admin"])
@login_required
def main_page():

    return render_template(
        "admin/main-page.html"
    )
