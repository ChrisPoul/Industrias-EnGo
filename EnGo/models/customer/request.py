

class CustomerRequest:

    def __init__(self, customer):
        self.customer = customer

    def add(self):
        error = self.customer.validation.validate()
        if not error:
            self.customer.add()
        
        return error
    
    def update(self):
        error = self.customer.validation.validate()
        if not error:
            self.customer.update()
        
        return error

