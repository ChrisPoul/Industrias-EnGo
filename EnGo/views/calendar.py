from datetime import date, datetime
from flask import (
    Blueprint, render_template, request,
    session
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
month_names = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
]


@bp.route("/calendar", methods=("POST", "GET"))
@login_required
def calendar():
    month_index = 0
    months = get_months(date.today())
    if request.method == "POST":
        selected_month = request.form["selected_month"]
        month_index = month_names.index(selected_month)

    return render_template(
        "calendar/calendar.html",
        weekdays=weekdays,
        month_names=month_names,
        month_index=month_index,
        month=months[month_index]
    )


@bp.route("/day/<string:date_str>")
@login_required
def day(date_str):
    day_date = datetime.strptime(date_str, "%d.%m.%Y")

    return render_template(
        "calendar/day.html"
    )