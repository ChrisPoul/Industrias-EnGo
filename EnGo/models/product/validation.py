from . import Product


class ProductValidation:

    def __init__(self, product):
        self.product = product
        self.error = None
    
    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_unique_values()
        if not self.error:
            self.validate_price()
        
        return self.error
    
    def validate_empty_values(self):
        if self.product.code == "":
            self.error = "No se pueden dejar campos vacios"
        
        return self.error

    def validate_unique_values(self):
        product = Product.search(self.product.code)
        if product and product is not self.product:
            self.error = "Ese código no está disponible"

        return self.error

    def validate_price(self):
        try:
            float(self.product.price)
        except ValueError:
            self.error = "Número invalido"

        return self.error
        
