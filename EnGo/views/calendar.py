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


event_types = dict(
    product="Ventas",
    receipt="Recibos",
    expense="Gastos"
)


def get_day_events(day):
    events = dict(
        product=filter_obj_by_date(SoldProduct.query.all(), day),
        receipt=filter_obj_by_date(Receipt.query.all(), day),
        expense=filter_obj_by_date(Expense.query.all(), day)
    )

    return events


def filter_obj_by_date(objs, date):
    return [obj for obj in objs if obj.date.date() == date.date()]


@bp.route("/day/<string:date_str>", methods=('POST', 'GET'))
@login_required
def day(date_str):
    day_date = datetime.strptime(date_str, "%d.%m.%Y")
    event_identifier = "receipt"
    events = get_day_events(day_date)
    if request.method == "POST":
        event_identifier = request.form["event_type"]
    if event_identifier == "receipt":
        view_name = f'{event_identifier}.edit'
    else:
        view_name = f'{event_identifier}.update'

    return render_template(
        "calendar/day.html",
        event_types=event_types,
        event_identifier=event_identifier,
        view_name=view_name,
        day=day_date,
        events=events
    )

