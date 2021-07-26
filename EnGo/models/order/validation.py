from datetime import datetime, date
from EnGo.models import validate_empty_values
from EnGo.models.user import User


class OrderValidation:

    def __init__(self, order):
        self.order = order
        self.error = None

    def validate(self):
        self.validate_empty_values()
        self.validate_user()
        if not self.error:
            self.validate_due_date()

        return self.error

    def validate_empty_values(self):
        order_required_values = [
            "title",
            "due_date"
        ]
        self.error = validate_empty_values(self.order, order_required_values)

        return self.error

    def validate_user(self):
        user = User.query.get(self.order.user_id)
        if not user:
            self.error = "No has seleccionado un empleado"
        
        return self.error

    def validate_due_date(self):
        if type(self.order.due_date) == date:
            return self.error
        try:
            due_date = datetime.strptime(self.order.due_date, "%Y-%m-%d")
            self.order.due_date = due_date
        except ValueError:
            self.error = "No has seleccionado una fecha, porfavor selecciona una"
        
        return self.error