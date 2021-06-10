from flask import (
    Blueprint, render_template
)
from . import login_required

bp = Blueprint("calendar", __name__)


@bp.route("/calendar")
@login_required
def calendar():

    return render_template(
        "calendar/calendar.html"
    )