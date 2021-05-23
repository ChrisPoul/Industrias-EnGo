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
from . import (
    login_required, permission_required,
    update_obj_attrs, get_form, get_empty_form
)
from .customer import customer_heads

bp = Blueprint('receipt', __name__)

product_heads = dict(
    quantity="Cantidad",
    code="Código",
    description="Descripcción",
    price="Precio",
    total="Total"
)
permissions = [
    "contaduría"
]


@bp.route('/receipt', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def add():
    if request.method == "POST":
        error = None
        customer = search_for_customer()
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
        customer_heads=customer_heads
    )


def search_for_customer():
    customer = None
    for head in customer_heads:
        value = request.form[head]
        customers = Customer.search(value)
        if len(customers) != 0 and value != "":
            customer = customers[-1]
            break

    return customer


@bp.route("/edit/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def edit(id):
    receipt = Receipt.get(id)
    form = get_form(product_heads)
    if request.method == "POST":
        update_obj_attrs(receipt.customer, customer_heads)
        update_receipt_products(receipt)
        error = receipt.request.edit()
        if not error:
            product = get_product_to_add()
            error = receipt.request.add_product(product)
            if not error:
                form = get_empty_form(product_heads)
        else:
            flash(error)

    return render_template(
        'receipt/edit.html',
        customer_heads=customer_heads,
        product_heads=product_heads,
        receipt=receipt,
        form=form
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
    for sold_product in receipt.sold_products:
        update_receipt_product(sold_product)


def update_receipt_product(sold_product):
    for attribute in product_heads:
        if attribute != "total":
            update_product_attr(sold_product, attribute)


def update_product_attr(sold_product, attribute):
    try:
        value = request.form[sold_product.get_unique_key(attribute)]
        if attribute == "code" or attribute == "description":
            setattr(sold_product.product, attribute, value)
            print(sold_product.product.description)
        else:
            setattr(sold_product, attribute, value)
    except KeyError:
        pass


@bp.route("/done/<int:id>")
@permission_required(permissions)
@login_required
def done(id):
    receipt = Receipt.get(id)
    receipt.done = True

    return render_template(
        "receipt/done.html",
        customer_heads=customer_heads,
        product_heads=product_heads,
        receipt=receipt
    )


@bp.route("/remove_product/<int:id>")
@permission_required(permissions)
@login_required
def remove_product(id):
    sold_product = SoldProduct.get(id)
    receipt_id = sold_product.receipt.id
    sold_product.delete()

    return redirect(
        url_for('receipt.edit', id=receipt_id)
    )


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    receipt = Receipt.get(id)
    receipt.delete()

    return redirect(
        url_for('customer.customers')
    )
