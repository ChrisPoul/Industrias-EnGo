from flask import (
    Blueprint, render_template, g,
    session
)
from . import permission_required
from EnGo.models.permission import Permission

bp = Blueprint('admin', __name__, url_prefix="/admin")


@bp.route("/main_page")
@permission_required("admin")
def main_page():

    return render_template(
        "admin/main-page.html"
    )


@bp.before_app_request
def load_loged_in_user():
    try:
        user_id = session["user_id"]
    except KeyError:
        user_id = None

    if user_id is None:
        g.user = None
    else:
        g.user = User.get(user_id)
