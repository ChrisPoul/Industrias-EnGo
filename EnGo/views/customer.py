from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models import customer
from EnGo.models.customer import Customer

bp = Blueprint('customer', __name__, url_prefix='/customer')

customer_heads = dict(
    customer_name='Nombre del cliente',
    address="Dirección",
    rfc="RFC"
)


@bp.route('/customers')
def customers():
    return render_template(
        'customer/customers.html'
    )


@bp.route('/add', methods=("POST", "GET"))
def add():
    if request.method == 'POST':
        customer = Customer(
            customer_name=request.form['customer_name'],
            address=request.form['address'],
            rfc=request.form['rfc']
        )
        error = customer.request.add()
        flash(error)

    return render_template(
        'customer/add.html'
    )


@bp.route('/update/<int:id>', methods=("POST", 'GET'))
def update(id):
    customer = Customer.get(id)
    if request.method == "POST":
        for attribute in customer_heads:
            setattr(customer, attribute, request.form[attribute])
        error = customer.request.update()
        flash(error)

    return render_template(
        'customer/update.html',
        customer=customer
    )


@bp.route('/delete/<int:id>')
def delete(id):
    customer = Customer.get(id)
    customer.delete()

    return redirect(
        url_for('customer.customers')
    )
    