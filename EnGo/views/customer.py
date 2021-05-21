from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models import customer
from EnGo.models.customer import Customer
from . import login_required, permission_required, update_obj_attrs

bp = Blueprint('customer', __name__, url_prefix='/customer')

customer_heads = dict(
    customer_name='Nombre',
    address="Dirección",
    rfc="RFC"
)
permissions = [
    "contaduría"
]


@bp.route('/customers')
@permission_required(permissions)
@login_required
def customers():
    customers = Customer.get_all()
    return render_template(
        'customer/customers.html',
        customer_heads=customer_heads,
        customers=customers
    )


@bp.route('/add', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def add():
    if request.method == 'POST':
        customer = Customer(
            customer_name=request.form['customer_name'],
            address=request.form['address'],
            rfc=request.form['rfc']
        )
        error = customer.request.add()
        if not error:
            return redirect(
                url_for('customer.customers')
            )
        flash(error)

    return render_template(
        'customer/add.html',
        customer_heads=customer_heads
    )


@bp.route('/update/<int:id>', methods=("POST", 'GET'))
@permission_required(permissions)
@login_required
def update(id):
    customer = Customer.get(id)
    if request.method == "POST":
        update_obj_attrs(customer, customer_heads)
        error = customer.request.update()
        if not error:
            return redirect(
                url_for('customer.customers')
            )
        flash(error)

    return render_template(
        'customer/update.html',
        customer_heads=customer_heads,
        customer=customer
    )


@bp.route('/delete/<int:id>')
@permission_required(permissions)
@login_required
def delete(id):
    customer = Customer.get(id)
    customer.delete()

    return redirect(
        url_for('customer.customers')
    )
    