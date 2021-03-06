from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from . import (
    permission_required, login_required, update_obj_attrs,
    get_form, get_empty_form
)
from EnGo.models.product import Product, FinishedProduct

bp = Blueprint("product", __name__, url_prefix="/product")

product_heads = dict(
    code="Código",
    description="Descripción",
    price="Precio"
)
finished_product_heads = dict(
    quantity="Cantidad",
    unit="Unidad",
    date="Fecha de Registro"
)
permissions = [
    "Contaduría"
]


@bp.route("/products", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def products():
    products = Product.query.all()
    if request.method == "POST":
        product = Product.search(request.form['search_term'])
        if product:
            return redirect(
                url_for('product.update', id=product.id)
            )

    return render_template(
        "product/products.html",
        product_heads=product_heads,
        products=products
    )


@bp.route("/add/<int:warehouse_id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def add(warehouse_id):
    if request.method == "POST":
        product = Product(
            warehouse_id=warehouse_id,
            code=request.form["code"],
            description=request.form["description"],
            price=request.form["price"]
        )
        error = product.request.add()
        if not error:
            return redirect(
                url_for('warehouse.inventory', id=warehouse_id)
            )
        flash(error)

    return render_template(
        "product/add.html",
        product_heads=product_heads
    )


@bp.route("/update/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update(id):
    product = Product.get(id)
    if request.method == "POST":
        update_obj_attrs(product, product_heads)
        error = product.request.update()
        if not error:
            return redirect(
                url_for('warehouse.inventory', id=product.warehouse_id)
            )
        flash(error)


    return render_template(
        "product/update.html",
        product_heads=product_heads,
        product=product
    )


@bp.route("/profile/<int:id>", methods=('POST', 'GET'))
def profile(id):
    product = Product.query.get(id)
    form = get_form(finished_product_heads)
    if request.method == "POST":
        finished_product = FinishedProduct(
            product_id=product.id,
            unit=request.form["unit"],
            quantity=request.form["quantity"]
        )
        error = finished_product.request.add()
        if error:
            flash(error)
        else:
            form = get_empty_form(finished_product_heads)
    
    return render_template(
        'product/profile.html',
        product_heads=product_heads,
        finished_product_heads=finished_product_heads,
        form=form,
        product=product
    )


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    product = Product.get(id)
    warehouse_id = product.warehouse_id
    product.delete()

    return redirect(
        url_for('product.products', warehouse_id=warehouse_id)
    )
