from datetime import date 
from flask import (
    Blueprint, render_template
)
from . import login_required, get_months

bp = Blueprint("calendar", __name__)

weekdays = [
    "Lunes",
    "Martes",
    "Miercoles",
    "Jueves",
    "Viernes",
    "Sabado",
    "Domingo"
]


@bp.route("/calendar")
@login_required
def calendar():
    months = get_months(date.today())
    return render_template(
        "calendar/calendar.html",
        weekdays=weekdays,
        month=months[0]
    )