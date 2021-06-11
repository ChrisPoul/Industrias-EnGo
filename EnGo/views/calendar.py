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
    select="Seleccionar Evento",
    sold_product="Productos Vendidos",
    finished_product="Productos Terminados",
    receipt="Recibos",
    expense="Gastos"
)
required_views = dict(
    sold_product="product.products",
    finished_product="warehouse.warehouses",
    receipt="receipt.add",
    expense="expense.expenses"
)


def get_day_events(day):

    def filter_obj_by_day(objs):
        return [obj for obj in objs if obj.date.date() == day.date()]

    events = dict(
        select=[],
        sold_product=filter_obj_by_day(SoldProduct.query.all()),
        finished_product=filter_obj_by_day(FinishedProduct.query.all()),
        receipt=filter_obj_by_day(Receipt.query.all()),
        expense=filter_obj_by_day(Expense.query.all())
    )

    return events


@bp.route("/day/<string:date_str>", methods=('POST', 'GET'))
@login_required
def day(date_str):
    day_date = datetime.strptime(date_str, "%d.%m.%Y")
    event_identifier = "select"
    events = get_day_events(day_date)
    if request.method == "POST":
        event_identifier = request.form["event_type"]
    if event_identifier == "receipt" or event_identifier == "sold_product":
        view_name = 'receipt.update'
    elif event_identifier == "finished_product":
        view_name = 'warehouse.update_product'
    else:
        view_name = f'{event_identifier}.update'

    return render_template(
        "calendar/day.html",
        event_types=event_types,
        required_views=required_views,
        event_identifier=event_identifier,
        view_name=view_name,
        day=day_date,
        events=events
    )



