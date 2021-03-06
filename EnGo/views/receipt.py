from datetime import datetime
from flask import (
    Blueprint, render_template, request,
    flash, url_for, session
)
from werkzeug.utils import redirect
from EnGo.models.customer import Customer
from EnGo.models.product import Product, SoldProduct
from EnGo.models.receipt import Receipt, filter_receipts_by_date
from . import (
    login_required, permission_required,
    update_obj_attrs, get_form, get_empty_form
)

bp = Blueprint('receipt', __name__)

receipt_heads = dict(
    folio="Remisión",
    date="Fecha",
    total="Total"
)
customer_heads = dict(
    customer_name="Nombre",
    address="Dirección",
    phone="Teléfono"
)
receipt_customer_heads = dict(
    customer_name="Nombre",
    address="Dirección"
)
product_heads = dict(
    quantity="Cantidad",
    code="Código",
    description="Descripción",
    unit="Unidad",
    price="Precio",
    total="Total"
)

permissions = [
    "Contaduría"
]


@bp.route('/receipts', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def receipts():
    selected_date_str = datetime.today().strftime('%Y-%m-%d')
    receipts = Receipt.query.all()
    if request.method == "POST":
        selected_date_str = request.form["selected_date"]
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
        receipts = filter_receipts_by_date(receipts, selected_date)

    return render_template(
        "receipt/receipts.html",
        receipt_heads=receipt_heads,
        selected_date=selected_date_str,
        receipts=receipts
    )


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
                phone=request.form['phone'],
                rfc=""
            )
            error = customer.request.add()
        if not error:
            receipt = Receipt(
                customer_id=customer.id
            )
            receipt.add()
            return redirect(
                url_for('receipt.update', id=receipt.id)
            )
        flash(error)    
    
    return render_template(
        'receipt/add.html',
        customer_heads=customer_heads,
        form=request.form
    )


def search_for_customer():
    customer = None
    for head in customer_heads:
        value = request.form[head]
        customers = Customer.search_all(value)
        if len(customers) != 0 and value != "":
            customer = customers[-1]
            break

    return customer


@bp.route("/update/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update(id):
    receipt = Receipt.get(id)
    form = get_product_form()
    empty_spaces = get_empty_spaces(receipt.products)
    if request.method == "POST":
        update_obj_attrs(receipt.customer, receipt_customer_heads)
        update_receipt_products(receipt)
        error = receipt.request.update()
        if not error:
            search_term = request.form["code"]
            product = Product.search(search_term)
            if not product:
                error = "No se encontró un producto con ese código"
            if not error and product not in set(receipt.products):
                sold_product = SoldProduct(
                    receipt_id=id,
                    product_id=product.id,
                    price=product.price,
                    unit=form["unit"],
                    quantity=form["quantity"]
                )
                error = sold_product.request.add()
            if not error:
                form = get_empty_product_form()
        if error:
            flash(error)

    return render_template(
        'receipt/receipt.html',
        customer_heads=receipt_customer_heads,
        product_heads=product_heads,
        empty_spaces=empty_spaces,
        receipt=receipt,
        form=form
    )


def get_product_form():
    form = get_form(product_heads)
    if not form['unit']:
        form['unit'] = "pz"
    if not form['quantity']:
        form['quantity'] = 0

    return form


def get_empty_product_form():
    form = get_empty_form(product_heads)
    form['unit'] = "pz"
    form['quantity'] = 0

    return form


@bp.route("/done/<int:id>")
@permission_required(permissions)
@login_required
def done(id):
    receipt = Receipt.get(id)
    empty_spaces = get_empty_spaces(receipt.products)
    receipt.done = True

    return render_template(
        "receipt/receipt.html",
        customer_heads=receipt_customer_heads,
        product_heads=product_heads,
        empty_spaces=empty_spaces,
        receipt=receipt
    )


@bp.route("/remove_product/<int:id>")
@permission_required(permissions)
@login_required
def remove_product(id):
    from EnGo.models.product import SoldProduct
    sold_product = SoldProduct.get(id)
    receipt_id = sold_product.receipt.id
    sold_product.delete()

    return redirect(
        url_for('receipt.update', id=receipt_id)
    )


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    receipt = Receipt.get(id)
    receipt.delete()
    if request.referrer:
        url = request.referrer
    else:
        url = url_for('home.main_page')

    return redirect(
        url
    )


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
        else:
            setattr(sold_product, attribute, value)
    except KeyError:
        pass


def get_empty_spaces(products):
    empty_spaces_length = 9 - len(products)
    empty_spaces = range(empty_spaces_length)

    return empty_spaces
