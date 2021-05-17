

class ProductRequest:

    def __init__(self, product):
        self.product = product
        
    def add(self):
        error = self.product.validation.validate()
        if not error:
            self.product.add()

        return error

    def update(self):
        error = self.product.validation.validate()
        if not error:
            self.product.update()

        return error
        