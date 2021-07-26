from datetime import datetime, timedelta, date
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models.user import User
from EnGo.models.order import Order
from EnGo.views import (
    permission_required, login_required,
    update_obj_attrs
)

bp = Blueprint("order", __name__, url_prefix="/order")

order_heads = dict(
    title="Título",
    description="Descripción",
    status="Estatus",
    user_id="Usuario",
    due_date="Fecha De Entrega"
)
order_status_options = [
    "Pendiente",
    "Completada",
    "Cancelada"
]
initial_user = dict(
    id=0,
    username="Seleccionar Empleado"
)
permissions = [
    "Recursos Humanos"
]


@bp.route("/assign", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def assign():
    min_date = datetime.today().strftime("%Y-%m-%d")
    users = [user for user in User.query.all() if not user.is_admin()]
    selected_user = initial_user
    if request.method == "POST":
        user_id = request.form['user_id']
        user = User.query.get(user_id)
        if user is not None:
            selected_user = user
        order = Order(
            user_id=user_id,
            title=request.form['title'],
            description=request.form['description'],
            due_date=request.form["due_date"]
        )
        error = order.request.add()
        if not error:
            return redirect(
                url_for('user.profile', id=user_id)
            )
        flash(error)
        
    return render_template(
        "order/assign.html",
        order_heads=order_heads,
        min_date=min_date,
        selected_user=selected_user,
        users=users
    )


@bp.route('/update/<int:order_id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update(order_id):
    order = Order.query.get(order_id)
    min_date = datetime.today().strftime("%Y-%m-%d")
    users = [user for user in User.query.all() if not user.is_admin()]
    selected_user = order.user
    if request.method == "POST":
        update_obj_attrs(order, order_heads)
        error = order.request.update()
        if not error:
            return redirect(
                url_for('user.profile', id=order.user_id)
            ) 
        flash(error)

    return render_template(
        'order/update.html',
        order_heads=order_heads,
        order_status_options=order_status_options,
        min_date=min_date,
        selected_user=selected_user,
        users=users,
        order=order
    )


@bp.route('/day_orders/<int:user_id>/<string:date_str>')
@permission_required(permissions)
@login_required
def day_orders(user_id, date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    user = User.query.get(user_id)
    day_orders = user.schedule.get_day_orders(date)
    check_for_overdue_orders(day_orders)
    
    return render_template(
        'order/day-orders.html',
        order_status_options=order_status_options,
        user=user,
        orders=day_orders,
        date=date
    )


def check_for_overdue_orders(orders):
    for order in orders:
        if order_is_overdue(order):
            order.status = "Atrasada"
            order.update()


def order_is_overdue(order):
    return order.due_date < date.today() - timedelta(days=1) and order.status == "Pendiente"
