from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models.warehouse import Warehouse
from EnGo.models.product import Product, FinishedProduct
from EnGo.models.expense import (
    Expense, ExpenseType, filter_expenses_by_type
)
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


@bp.route("/inventory/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def inventory(id):
    warehouse = Warehouse.query.get(id)
    if request.method == "POST":
        product = Product.search(request.form["search_term"])
        if product and product.warehouse_id == warehouse.id:
            return redirect(
                url_for('product.update', id=product.id)
            )

    return render_template(
        "warehouse/inventory.html",
        product_heads=product_heads,
        products=warehouse.products,
        warehouse=warehouse
    )
