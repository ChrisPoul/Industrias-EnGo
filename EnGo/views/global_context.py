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
from .view import view_heads
from . import (
    login_required, format_price,
    format_date
)

bp = Blueprint("global_context", __name__)


@bp.route('/search_bar')
@login_required
def search_bar():
    search_term = request.args['search_term']
    bp_name = "customer"
    try:
        result = Customer.search_all(search_term)[0]
    except IndexError:
        result = None
    if not result:
        bp_name = "user"
        result = User.search(search_term)
    if not result:
        bp_name = "view"
        result = View.search(search_term)
    if not result:
        bp_name = "product"
        result = Product.search(search_term)

    if result:
        return redirect(
            url_for(f"{bp_name}.update", id=result.id)
        )
    else: 
        return redirect(
            session['prev_url']
        )


@bp.app_context_processor
def inject_functions():
    return dict(
        format_price=format_price,
        format_date=format_date,
        get_autocomplete_data=get_autocomplete_data
    )


@bp.app_context_processor
def inject_view_and_permissions():
    session["prev_url"] = request.referrer
    return dict(
        view=View.search(request.endpoint),
        view_heads=view_heads,
        permissions=Permission.get_all()
    )


@bp.app_context_processor
def inject_settings():
    settings = get_settings()
    return dict(
        settings=settings
    )


def get_autocomplete_data(group, attribute):
    groups = dict(
        users=User.get_all(),
        products=Product.get_all(),
        customers = Customer.get_all(),
        views=View.get_all(),
        expenses=Expense.get_all(),
        warehouses=Warehouse.get_all()
    )
    data = []
    for obj in groups[group]:
        value = getattr(obj, attribute)
        if value not in set(data):
            data.append(value)
    
    return data