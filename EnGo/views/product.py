from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from . import permission_required, login_required
from EnGo.models.product import Product

bp = Blueprint("product", __name__, url_prefix="/product")

product_heads = dict(
    code="Código",
    description="Descripción",
    price="Precio"
)


@bp.route("/products")
@permission_required(["contaduría"])
@login_required
def products():

    return render_template(
        "product/products.html"
    )


@bp.route("/add", methods=('POST', 'GET'))
@permission_required(["contaduría"])
@login_required
def add():
    if request.method == "POST":
        product = Product(
            code=request.form["code"],
            description=request.form["description"],
            price=request.form["price"]
        )
        error = product.request.add()

        flash(error)

    return render_template(
        "product/add.html"
    )


@bp.route("/update/<int:id>", methods=('POST', 'GET'))
@permission_required(["contaduría"])
@login_required
def update(id):
    product = Product.get(id)
    if request.method == "POST":
        for attribute in product_heads:
            setattr(product, attribute, request.form[attribute])
        product.request.update()

    return render_template(
        "product/update.html",
        product=product
    )


@bp.route("/delete/<int:id>")
@permission_required(["contaduría"])
@login_required
def delete(id):
    product = Product.get(id)
    product.delete()

    return redirect(
        url_for('product.products')
    )
