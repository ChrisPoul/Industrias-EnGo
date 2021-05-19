from flask import (
    Blueprint, render_template, request,
    flash, url_for
)
from werkzeug.utils import redirect
from .customer import customer_heads
from .product import product_heads
from EnGo.models.customer import Customer
from EnGo.models.product import Product, SoldProduct
from EnGo.models.receipt import Receipt
from . import update_obj_attrs, get_form

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
        update_receipt_products(receipt)
        product = get_product_to_add()
        error = receipt.request.edit(product)

    return render_template(
        'receipt/edit.html'
    )


@bp.route("/remove_product/<int:id>")
def remove_product(id):
    sold_product = SoldProduct.get(id)
    receipt_id = sold_product.receipt.id
    sold_product.delete()

    return redirect(
        url_for('receipt.edit', id=receipt_id)
    )


@bp.route("/delete/<int:id>")
def delete(id):
    receipt = Receipt.get(id)
    receipt.delete()

    return redirect(
        url_for('customer.customers')
    )


def get_product_to_add():
    form = get_form(product_heads)
    product = Product(
        code=form["code"],
        description=form["description"],
        price=form["price"]
    )

    return product


def update_receipt_products(receipt):
    for product in receipt.products:
        update_receipt_product(product)


def update_receipt_product(product):
    for attribute in product_heads:
        update_product_attr(product, attribute)


def update_product_attr(product, attribute):
    unique_key = f"{attribute}_{product.id}"
    try:
        value = request.form[unique_key]
        setattr(product, attribute, value)
    except KeyError:
        pass