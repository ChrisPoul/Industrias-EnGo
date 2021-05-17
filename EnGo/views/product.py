from flask import (
    Blueprint, render_template, request,
    flash
)
from EnGo.models.product import Product

bp = Blueprint("product", __name__, url_prefix="/product")


@bp.route("/add", methods=('POST', 'GET'))
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