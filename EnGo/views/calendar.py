from datetime import date, datetime
from functools import lru_cache
from flask import (
    Blueprint, render_template, request
)
from EnGo.models.product import SoldProduct, FinishedProduct
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

event_categories = dict(
    selecting="Seleccionar Categoría",
    all="Todos",
    sold_product="Productos Vendidos",
    finished_product="Productos Terminados",
    receipt="Recibos",
    expense="Gastos"
)
update_views = dict(
    all="admin.admin",
    sold_product="receipt.update",
    finished_product="warehouse.update_product",
    receipt="receipt.update",
    expense="expense.update"
)


@lru_cache(maxsize=1)
def get_all_events():
    return dict(
        selecting=[],
        all=[],
        sold_product=SoldProduct.query.all(),
        finished_product=FinishedProduct.query.all(),
        receipt=Receipt.query.all(),
        expense=Expense.query.all()
    )


def get_year_events(date):

    def filter_events_by_year(events):
        return [event for event in events if event.date.date().year == date.date().year]

    all_events = get_all_events()
    year_events = {}
    for selected_category in all_events:
        events = all_events[selected_category]
        year_events[selected_category] = filter_events_by_year(events)
    
    return year_events


def get_month_events(date):

    def filter_events_by_month(events):
        return [event for event in events if event.date.date().month == date.date().month]
        
    year_events = get_year_events(date)
    month_events = {}
    for selected_category in year_events:
        events = year_events[selected_category]
        month_events[selected_category] = filter_events_by_month(events)

    return month_events


@lru_cache(maxsize=40)
def get_day_events(date):
    try:
        filter_date = date.date()
    except AttributeError:
        filter_date = date

    def filter_events_by_day(events):
        return [event for event in events if event.date.date() == filter_date]

    all_events = get_all_events()
    day_events = {}
    for selected_category in all_events:
        events = all_events[selected_category]
        day_events[selected_category] = filter_events_by_day(events)

    return day_events


def get_date_from_str(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y")


@bp.route("/calendar", methods=("POST", "GET"))
@login_required
def calendar():
    current_date = date.today()
    selected_category = "selecting"
    if request.method == "POST":
        selected_category = request.form["event_category"]
        month_str = request.form["selected_date"]
        if not month_str:
            current_date = date.today()
        else:
            current_date = datetime.strptime(month_str, "%Y-%m")
    month_index = current_date.month - 1
    months = get_months(current_date)

    return render_template(
        "calendar/calendar.html",
        weekdays=weekdays,
        event_categories=event_categories,
        month_names=month_names,
        month_index=month_index,
        selected_category=selected_category,
        get_day_events=get_day_events,
        current_date=current_date,
        update_views=update_views,
        month=months[month_index]
    )


@bp.route("/day/<string:date_str>/<string:category>", methods=('POST', 'GET'))
@login_required
def day(date_str, category):
    current_date = get_date_from_str(date_str)
    selected_category = category
    get_all_events.cache_clear()
    events = get_day_events(current_date)
    if request.method == "POST":
        selected_category = request.form["event_category"]

    return render_template(
        "calendar/day.html",
        current_date=current_date,
        event_categories=event_categories,
        selected_category=selected_category,
        update_views=update_views,
        events=events
    )
