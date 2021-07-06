from datetime import date, datetime
from flask import (
    Blueprint, render_template, request
)
from EnGo.models.calendar import MyCalendar
from . import login_required

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
    selected_date = date.today()
    selected_category = "selecting"
    if request.method == "POST":
        selected_category = request.form["event_category"]
        month_str = request.form["selected_date"]
        if not month_str:
            selected_date = date.today()
        else:
            selected_date = datetime.strptime(month_str, "%Y-%m")
    month_index = selected_date.month - 1
    months = MyCalendar.get_months(selected_date)

    return render_template(
        "calendar/calendar.html",
        weekdays=weekdays,
        event_categories=event_categories,
        month_names=month_names,
        month_index=month_index,
        selected_category=selected_category,
        get_day_events=MyCalendar.get_day_events,
        selected_date=selected_date,
        update_views=update_views,
        month=months[month_index]
    )


@bp.route("/day/<string:date_str>/<string:category>", methods=('POST', 'GET'))
@login_required
def day(date_str, category):
    selected_date = datetime.strptime(date_str, "%d.%m.%Y")
    selected_category = category
    events = MyCalendar.get_day_events(selected_date)
    if request.method == "POST":
        selected_category = request.form["event_category"]

    return render_template(
        "calendar/day.html",
        selected_date=selected_date,
        event_categories=event_categories,
        selected_category=selected_category,
        update_views=update_views,
        events=events
    )
