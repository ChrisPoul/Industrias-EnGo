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
    'Dev'
]
warehouse_heads = dict(
    address="Dirección"
)
product_heads = dict(
    product_heads,
    unit="Unidad",
    quantity="Cantidad",
    cost="Costo"
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
        "warehouse/update.html"
    )


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    warehouse = Warehouse.query.get(id)
    warehouse.delete()

    return redirect(
        url_for('warehouse.warehouses')
    )


@bp.route("/inventory/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def inventory(id):
    warehouse = Warehouse.query.get(id)
    expenses = warehouse.expenses
    expense_types = ExpenseType.query.all()
    type_all = dict (
        id=0,
        name="Todos"
    )
    expense_types.insert(0, type_all)
    if request.method == "POST":
        search_term = request.form["search_term"]
        if search_term != "":
            expenses = warehouse.search_expenses(search_term)
        type_id = request.form['type_id']
        expense_type = ExpenseType.query.get(type_id)
        if type_id == "0":
            expense_type = type_all
        expense_types.remove(expense_type)
        expense_types.insert(0, expense_type)
        expenses = filter_expenses_by_type(expenses, type_id)

    return render_template(
        "warehouse/inventory.html",
        expense_heads=expense_heads,
        product_heads=product_heads,
        expenses=expenses,
        expense_types=expense_types,
        products=warehouse.finished_products,
        warehouse=warehouse
    )


@bp.route("/add_expense/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def add_expense(id):
    form = get_form(expense_heads)
    warehouse = Warehouse.query.get(id)
    expense_types = ExpenseType.query.all()
    if request.method == "POST":
        expense = Expense(
            concept=form['concept'],
            type_id=form['type_id'],
            cost=form['cost'],
            unit=form['unit'],
            quantity=form['quantity']
        )
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
        expense_types=expense_types,
        warehouse=warehouse
    )


@bp.route('/add_product/<int:id>', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def add_product(id):
    warehouse = Warehouse.query.get(id)
    product = None
    form = get_form(product_heads)
    if request.method == "POST":
        error = None
        product = Product.search(form['code'])
        if not product:
            product = Product(
                code=form['code'],
                description=form['description'],
                price=form['price']
            )
            error = product.request.add()
        if not error:
            finished_product = FinishedProduct(
                product_id=product.id,
                warehouse_id=warehouse.id,
                quantity=form['quantity'],
                unit=form['unit'],
                cost=form['cost']
            )
            error = finished_product.request.add()
        else:
            error = """
                Ese producto aún no está registrado, porfavor 
                registra un producto válido antes de continuar,
                puedes registrarlo desde aquí
            """
        if not error:
            return redirect(
                url_for('warehouse.inventory', id=id)
            )
        flash(error)

    return render_template(
        'warehouse/add-product.html',
        product_heads=product_heads,
        warehouse=warehouse,
        product=product,
        form=form
    )


@bp.route('/update_product/<int:id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update_product(id):
    finished_product = FinishedProduct.query.get(id)
    if request.method == "POST":
        finished_product_attrs = [
            "quantity",
            "unit",
            "cost"
        ]
        update_obj_attrs(finished_product, finished_product_attrs)
        error = finished_product.request.update()
        if not error:
            return redirect(
                url_for('warehouse.inventory', id=finished_product.warehouse.id)
            )
        flash(error)

    return render_template(
        "product/update.html",
        product_heads=product_heads,
        product=finished_product,
        warehouse=finished_product.warehouse
    )


@bp.route('/delete_product/<int:id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def delete_product(id):
    finished_product = FinishedProduct.query.get(id)
    warehouse_id = finished_product.warehouse.id
    finished_product.delete()

    return redirect(
        url_for('warehouse.inventory', id=warehouse_id)
    )
