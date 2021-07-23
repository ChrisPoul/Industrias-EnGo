from EnGo.models import validate_empty_values


class OrderValidation:

    def __init__(self, order):
        self.order = order
        self.error = None

    def validate(self):
        self.validate_empty_values()

        return self.error

    def validate_empty_values(self):
        order_required_values = [
            "title",
            "due_date"
        ]
        self.error = validate_empty_values(self.order, order_required_values)

        return self.error