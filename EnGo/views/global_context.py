from flask import (
    Blueprint, request, session,
    redirect, url_for
)
from EnGo.models.user import User
from EnGo.models.product import Product
from EnGo.models.customer import Customer
from EnGo.models.view import View
from EnGo.models.permission import Permission
from EnGo.models.expense import Expense
from EnGo.models.warehouse import Warehouse
from EnGo.commands.settings import get_settings
from .customer import customer_heads
from . import (
    login_required, format_price,
    format_date, format_datetime
)

bp = Blueprint("global_context", __name__)


@bp.app_context_processor
def inject_functions():

    return dict(
        format_price=format_price,
        format_date=format_date,
        format_datetime=format_datetime,
        get_autocomplete_data=get_autocomplete_data,
        len=len
    )


@bp.app_context_processor
def inject_view_and_permissions():
    return dict(
        view=View.search(request.endpoint),
        permissions=Permission.get_all()
    )


@bp.app_context_processor
def inject_global_objects():
    settings = get_settings()
    warehouses = Warehouse.get_all()
    customer_autocomplete_heads = [
        "phone",
        "rfc"
    ]

    return dict(
        settings=settings,
        warehouses=warehouses,
        customer_autocomplete_heads=customer_autocomplete_heads
    )


@bp.route('/search_bar', methods=('POST', ))
@login_required
def search_bar():
    search_term = request.form['search_term']
    try:
        customer = Customer.search_all(search_term)[0]
    except IndexError:
        customer = None
    if customer:
        return redirect(
            url_for("customer.update", id=customer.id)
        )
    user = User.search(search_term)
    if user:
        return redirect(
            url_for("user.profile", id=user.id)
        )
    product = Product.search(search_term)
    if product:
        return redirect(
            url_for("product.update", id=product.id)
        )

    return redirect(
        request.referrer
    )


def get_autocomplete_data(group, attribute):
    groups = dict(
        users=User.get_all(),
        products=Product.get_all(),
        customers = Customer.get_all(),
        expenses=Expense.get_all(),
        warehouses=Warehouse.get_all()
    )
    data = []
    for obj in groups[group]:
        value = getattr(obj, attribute)
        if value not in set(data):
            data.append(value)
    
    return data