class OrderRequest:

    def __init__(self, order):
        self.order = order

    def add(self):
        error = self.order.validation.validate()
        if not error:
            self.order.add()
        
        return error

    def update(self):
        error = self.order.validation.validate()
        if not error:
            self.order.update()
        
        return error
