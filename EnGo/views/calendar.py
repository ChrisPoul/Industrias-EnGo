from datetime import date, datetime
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

event_types = dict(
    selecting="Seleccionar Categoría",
    sold_product="Productos Vendidos",
    finished_product="Productos Terminados",
    receipt="Recibos",
    expense="Gastos"
)
required_views = dict(
    sold_product="receipt.add",
    finished_product="warehouse.add_product",
    receipt="receipt.add",
    expense="expense.expenses"
)


def get_all_events():
    return dict(
        selecting=[],
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
    for event_identifier in all_events:
        events = all_events[event_identifier]
        year_events[event_identifier] = filter_events_by_year(events)
    
    return year_events


def get_month_events(date):

    def filter_events_by_month(events):
        return [event for event in events if event.date.date().month == date.date().month]
        
    year_events = get_year_events(date)
    month_events = {}
    for event_identifier in year_events:
        events = year_events[event_identifier]
        month_events[event_identifier] = filter_events_by_month(events)

    return month_events


def get_day_events(date):

    def filter_events_by_day(events):
        return [event for event in events if event.date.date() == date.date()]

    all_events = get_all_events()
    day_events = {}
    for event_identifier in all_events:
        events = all_events[event_identifier]
        day_events[event_identifier] = filter_events_by_day(events)

    return day_events


def get_view_name(event_identifier):
    if event_identifier == "receipt" or event_identifier == "sold_product":
        view_name = 'receipt.update'
    elif event_identifier == "finished_product":
        view_name = 'warehouse.update_product'
    else:
        view_name = f'{event_identifier}.update'

    return view_name


def get_date_from_str(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y")


@bp.route("/calendar", methods=("POST", "GET"))
@login_required
def calendar():
    current_date = date.today()
    event_identifier = "selecting"
    if request.method == "POST":
        event_identifier = request.form["event_type"]
        current_date_str = request.form["selected_date"]
        if not current_date_str:
            current_date = date.today()
        else:
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    view_name = get_view_name(event_identifier)
    month_index = current_date.month - 1
    months = get_months(current_date)

    return render_template(
        "calendar/calendar.html",
        weekdays=weekdays,
        event_types=event_types,
        month_names=month_names,
        view_name=view_name,
        month_index=month_index,
        event_identifier=event_identifier,
        get_day_events=get_day_events,
        current_date=current_date,
        required_views=required_views,
        month=months[month_index]
    )


@bp.route("/day/<string:date_str>", methods=('POST', 'GET'))
@login_required
def day(date_str):
    current_date = get_date_from_str(date_str)
    event_identifier = "selecting"
    events = get_day_events(current_date)
    if request.method == "POST":
        event_identifier = request.form["event_type"]
    view_name = get_view_name(event_identifier)

    return render_template(
        "calendar/day.html",
        current_date=current_date,
        view_name=view_name,
        event_types=event_types,
        event_identifier=event_identifier,
        required_views=required_views,
        events=events
    )
