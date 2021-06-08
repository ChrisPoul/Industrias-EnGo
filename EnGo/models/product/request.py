

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


class FinishedProductRequest:

    def __init__(self, finished_product):
        self.finished_product = finished_product

    def add(self):
        error = self.finished_product.validation.validate()
        if not error:
            self.finished_product.add()
        
        return error
    
    def update(self):
        error = self.finished_product.validation.validate()
        if not error:
            self.finished_product.update()
        
        return error