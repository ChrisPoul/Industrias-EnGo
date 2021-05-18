from flask import (
    Blueprint, render_template, request,
    flash
)
from EnGo.models.customer import Customer

bp = Blueprint('customer', __name__, url_prefix='/customer')


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
