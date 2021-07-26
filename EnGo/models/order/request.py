from datetime import datetime


class OrderRequest:

    def __init__(self, order):
        self.order = order

    def add(self):
        error = self.order.validation.validate()
        if not error:
            self.update_due_date()
            self.order.add()
        
        return error

    def update(self):
        error = self.order.validation.validate()
        if not error:
            self.update_due_date()
            self.order.update()
        
        return error

    def update_due_date(self):
        if type(self.order.due_date) == str:
            due_date = datetime.strptime(
                self.order.due_date, "%Y-%m-%d"
            )
            self.order.due_date = due_date
