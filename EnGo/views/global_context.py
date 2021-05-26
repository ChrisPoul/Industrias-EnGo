from flask import Blueprint, request, session
from EnGo.models.user import User
from EnGo.models.product import Product
from EnGo.models.customer import Customer
from EnGo.models.view import View
from EnGo.models.permission import Permission
from . import (
    format_price, format_date
)

bp = Blueprint("global_context", __name__)


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