from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from . import (
    permission_required, login_required, update_obj_attrs,
    get_form
)
from EnGo.models.product import Product

bp = Blueprint("product", __name__, url_prefix="/product")

product_heads = dict(
    code="Código",
    description="Descripción",
    price="Precio"
)
permissions = [
    "Contaduría"
]


@bp.route("/products", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def products():
    products = Product.get_all()
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


@bp.route("/add", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def add():
    form = get_form(product_heads)
    if request.method == "POST":
        product = Product(
            code=form["code"],
            description=form["description"],
            price=form["price"]
        )
        error = product.request.add()
        if not error:
            return redirect(
                url_for('product.products')
            )
        flash(error)

    return render_template(
        "product/add.html",
        product_heads=product_heads,
        form=form
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
                url_for('product.products')
            )
        flash(error)


    return render_template(
        "product/update.html",
        product_heads=product_heads,
        product=product
    )


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    product = Product.get(id)
    product.delete()

    return redirect(
        url_for('product.products')
    )
