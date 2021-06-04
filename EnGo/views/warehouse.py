from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models.warehouse import Warehouse
from EnGo.models.expense import Expense
from . import (
    permission_required, login_required,
    get_form, update_obj_attrs
)

bp = Blueprint("warehouse", __name__, url_prefix="/warehouse")

permissions = [
    "inventario"
]
warehouse_heads = dict(
    address="Dirección"
)
expense_heads = dict(
    concept="Concepto",
    type="Tipo",
    cost="Costo",
    quantity="Cantidad"
)


@bp.route("/warehouses")
@permission_required(permissions)
@login_required
def warehouses():
    warehouses = Warehouse.get_all()

    return render_template(
        "warehouse/warehouses.html",
        warehouses=warehouses
    )


@bp.route("/add", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def add():
    form = get_form(warehouse_heads)
    if request.method == "POST":
        warehouse = Warehouse(
            address=form["address"]
        )
        error = warehouse.request.add()
        if not error:
            return redirect(
                url_for('warehouse.inventory', id=warehouse.id)
            )
        flash(error)

    return render_template(
        "warehouse/add.html"
    )


@bp.route("/update/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update(id):
    warehouse = Warehouse.get(id)
    if request.method == "POST":
        update_obj_attrs(warehouse, warehouse_heads)
        error = warehouse.request.update()
        if not error:
            return redirect(
                url_for("warehouse.inventory", id=warehouse.id)
            )
        flash(error)

    return render_template(
        "warehouse/update.html"
    )


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    warehouse = Warehouse.get(id)
    warehouse.delete()

    return redirect(
        url_for('warehouse.warehouses')
    )


@bp.route("/inventory/<int:id>")
@permission_required(permissions)
@login_required
def inventory(id):

    return render_template(
        "warehouse/inventory.html"
    )


@bp.route("/add_expense/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def add_expense(id):
    form = get_form(expense_heads)
    warehouse = Warehouse.get(id)
    if request.method == "POST":
        expense = Expense.search(form['concept'])
        if not expense:
            expense = Expense(
                concept=form['concept'],
                type=form['type'],
                cost=form['cost']
            )
        expense.quantity = form['quantity']
        error = warehouse.request.add_expense(expense)
        flash(error)
    
    return render_template(
        'expense/add.html',
        expense_heads=expense_heads,
        form=form
    )