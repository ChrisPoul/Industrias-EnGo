from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models.warehouse import Warehouse
from EnGo.models.expense import Expense
from .expense import expense_types
from . import (
    permission_required, login_required,
    get_form, update_obj_attrs
)

bp = Blueprint("warehouse", __name__, url_prefix="/warehouse")

permissions = [
    'Dev'
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


@bp.route("/warehouses", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def warehouses():
    warehouses = Warehouse.get_all()
    if request.method == "POST":
        search_term = request.form["search_term"]
        warehouse = Warehouse.search(search_term)
        if warehouse:
            return redirect(
                url_for('warehouse.inventory', id=warehouse.id)
            )

    return render_template(
        "warehouse/warehouses.html",
        warehouse_heads=warehouse_heads,
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
        "warehouse/add.html",
        warehouse_heads=warehouse_heads,
        form=form,
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


@bp.route("/inventory/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def inventory(id):
    warehouse = Warehouse.get(id)
    registered_expenses = warehouse.registered_expenses
    if request.method == "POST":
        search_term = request.form['search_term']
        expense = Expense.search(search_term)
        if expense:
            registered_expenses = expense.registered_expenses

    return render_template(
        "warehouse/inventory.html",
        expense_heads=expense_heads,
        registered_expenses=registered_expenses,
        warehouse=warehouse
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
        expense.registered_type = form['type']
        expense.quantity = form['quantity']
        error = warehouse.request.add_expense(expense)
        if not error:
            return redirect(
                url_for('warehouse.inventory', id=id)
            )
        flash(error)
    
    return render_template(
        'expense/add.html',
        expense_heads=expense_heads,
        form=form,
        expense_types=expense_types
    )


@bp.route('/delete/<int:id>/')
@permission_required(permissions)
@login_required
def delete_expense(id):
    from EnGo.models.expense import RegisteredExpense
    registered_expense = RegisteredExpense.get(id)
    warehouse_id = registered_expense.warehouse_id
    registered_expense.delete()

    return redirect(
        url_for('warehouse.inventory', id=warehouse_id)
    )
    

