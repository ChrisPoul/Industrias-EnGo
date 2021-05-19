from flask import (
    Blueprint, render_template, request,
    flash, url_for
)
from werkzeug.utils import redirect
from .customer import customer_heads
from .product import product_heads
from EnGo.models.customer import Customer
from EnGo.models.receipt import Receipt
from . import update_obj_attrs

bp = Blueprint('receipt', __name__)


@bp.route('/receipt', methods=("POST", "GET"))
def add():
    if request.method == "POST":
        error = None
        customer = None
        for head in customer_heads:
            customers = Customer.search(request.form[head])
            if len(customers) != 0:
                customer = customers[-1]
                break
        if not customer:
            customer = Customer(
                customer_name=request.form['customer_name'],
                address=request.form['address'],
                rfc=request.form['rfc']
            )
            error = customer.request.add()
        if not error:
            receipt = Receipt(
                customer_id=customer.id
            )
            receipt.add()
            return redirect(
                url_for('receipt.edit', id=receipt.id)
            )
        flash(error)    
    
    return render_template(
        'receipt/add.html',
    )


@bp.route("/edit/<int:id>", methods=('POST', 'GET'))
def edit(id):
    receipt = Receipt.get(id)
    if request.method == "POST":
        update_obj_attrs(receipt.customer, customer_heads)
        error = receipt.request.edit()
        print(error)

    return render_template(
        'receipt/edit.html'
    )


def update_products(products):
    update_products(receipt.products)
    for product in products:
        for attribute in product_heads:
            setattr(product, attribute, request.form[f"{attribute}_{product.id}"])