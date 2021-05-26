from flask import (
    Blueprint, request, session,
    redirect
)
from flask.helpers import url_for
from EnGo.models.user import User
from EnGo.models.product import Product
from EnGo.models.customer import Customer
from EnGo.models.view import View
from EnGo.models.permission import Permission
from . import (
    format_price, format_date
)

bp = Blueprint("global_context", __name__)


@bp.route('/search_bar')
def search_bar():
    search_term = request.args['search_term']
    bp_name = "customer"
    try:
        result = Customer.search(search_term)[0]
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
def inject_formaters():
    return dict(
        format_price=format_price,
        format_date=format_date
    )


@bp.app_context_processor
def inject_view_and_permissions():
    session["prev_url"] = request.referrer
    return dict(
        view=View.search(request.endpoint),
        permissions=Permission.get_all()
    )


@bp.app_context_processor
def inject_autocomplete():
    return dict(
        autocomplete=Autocomplete()
    )


class Autocomplete:

    def __init__(self):
        self.groups = dict(
            users=User.get_all(),
            products=Product.get_all(),
            customers = Customer.get_all(),
            views=View.get_all()
        )

    def get_data(self, group, attribute):
        data = []
        for obj in self.groups[group]:
            value = getattr(obj, attribute)
            if value not in set(data):
                data.append(value)
        
        return data