from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models.warehouse import Warehouse
from EnGo.models.product import Product, FinishedProduct
from EnGo.models.expense import (
    Expense, ExpenseType, filter_expenses_by_type
)
from .expense import expense_heads
from .product import product_heads
from . import (
    permission_required, login_required,
    get_form, update_obj_attrs
)

bp = Blueprint("warehouse", __name__, url_prefix="/warehouse")

permissions = [
    'Contaduría',
    'Calidad'
]
accounting_permission = ["Contaduría"]
quality_permission = ["Calidad"]

warehouse_heads = dict(
    address="Dirección"
)


@bp.route("/add", methods=('POST', 'GET'))
@permission_required(accounting_permission)
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
@permission_required(accounting_permission)
@login_required
def update(id):
    warehouse = Warehouse.query.get(id)
    if request.method == "POST":
        update_obj_attrs(warehouse, warehouse_heads)
        error = warehouse.request.update()
        if not error:
            return redirect(
                url_for("warehouse.inventory", id=warehouse.id)
            )
        flash(error)

    return render_template(
        "warehouse/update.html",
        warehouse_heads=warehouse_heads,
        warehouse=warehouse
    )


@bp.route("/delete/<int:id>")
@permission_required(accounting_permission)
@login_required
def delete(id):
    warehouse = Warehouse.query.get(id)
    warehouse.delete()

    return redirect(
        url_for('home.main_page')
    )


@bp.route("/add_expense/<int:id>", methods=('POST', 'GET'))
@permission_required(accounting_permission)
@login_required
def add_expense(id):
    warehouse = Warehouse.query.get(id)
    expense_types = ExpenseType.query.all()
    if request.method == "POST":
        expense = Expense(
            concept=request.form["concept"],
            type_id=request.form['type_id'],
            cost=request.form['cost'],
            unit=request.form['unit'],
            quantity=request.form['quantity']
        )
        error = expense.request.add()
        if not error:
            warehouse.add_expense(expense)
            return redirect(
                url_for('warehouse.inventory', id=warehouse.id)
            )
        flash(error)

    return render_template(
        "expense/add.html",
        expense_heads=expense_heads,
        expense_types=expense_types,
        form=request.form
    )


@bp.route("/inventory/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def inventory(id):
    warehouse = Warehouse.query.get(id)
    warehouse_inventory = WarehouseInventory(warehouse)
    expense_types = ExpenseType.query.all()
    selected_expense_type = dict (
        id=0,
        name="Todos"
    )
    expense_types.append(selected_expense_type)
    if request.method == "POST":
        warehouse_inventory.handle_search_request()
        if warehouse_inventory.type_id != 0:
            selected_expense_type = ExpenseType.query.get(warehouse_inventory.type_id)

    return render_template(
        "warehouse/inventory.html",
        expense_heads=expense_heads,
        product_heads=product_heads,
        expenses=warehouse_inventory.expenses,
        expense_types=expense_types,
        selected_expense_type=selected_expense_type,
        products=warehouse_inventory.products,
        selected_inventory=warehouse_inventory.selected_inventory,
        warehouse=warehouse
    )


class WarehouseInventory:

    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.expenses = warehouse.expenses
        self.products = warehouse.products
        self.type_id = 0
        self.selected_inventory = "products"

    def handle_search_request(self):
        self.search_term = request.form["search_term"]
        try:
            self.type_id = int(request.form['type_id'])
            self.selected_inventory = "expenses"
            self.search_expenses()
        except KeyError:
            self.selected_inventory = "products"
            self.search_products()

    def search_expenses(self):
        if self.search_term != "":
            self.expenses = self.warehouse.search_expenses(self.search_term)
        self.expenses = filter_expenses_by_type(self.expenses, self.type_id)

    def search_products(self):
        product = Product.search(self.search_term)
        if product:
            return redirect(
                url_for('product.update', id=product.id)
            )
