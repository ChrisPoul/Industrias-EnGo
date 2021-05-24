from flask import Blueprint
from EnGo.models.user import User
from EnGo.models.product import Product
from EnGo.models.customer import Customer

bp = Blueprint("autocomplete", __name__)


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
            customers = Customer.get_all()
        )

    def get_data(self, group, attribute):
        data = []
        for obj in self.groups[group]:
            value = getattr(obj, attribute)
            if value not in set(data):
                data.append(value)
        
        return data