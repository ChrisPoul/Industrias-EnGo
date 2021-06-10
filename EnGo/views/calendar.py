from datetime import date, datetime
from flask import (
    Blueprint, render_template, request,
    session
)
from EnGo.models.product import SoldProduct
from EnGo.models.receipt import Receipt
from EnGo.models.expense import Expense
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
    today = date.today()
    month_index = today.month - 1
    months = get_months(today)
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


@bp.route("/day/<string:date_str>", methods=('POST', 'GET'))
@login_required
def day(date_str):
    day_date = datetime.strptime(date_str, "%d.%m.%Y")
    event_type = "Ventas"
    events = get_day_events(day_date)
    if request.method == "POST":
        event_type = request.form["event_type"]
    

    return render_template(
        "calendar/day.html",
        day=day_date,
        event_type=event_type,
        events=events
    )


def get_day_events(day):
    events = dict(
        Ventas=filter_obj_by_date(SoldProduct.query.all(), day),
        Recibos=filter_obj_by_date(Receipt.query.all(), day),
        Gastos=filter_obj_by_date(Expense.query.all(), day)
    )

    return events


def filter_obj_by_date(objs, date):
    return [obj for obj in objs if obj.date.date() == date.date()]

