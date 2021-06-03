from . import Product
from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values


class ProductValidation:

    def __init__(self, product):
        self.product = product
        self.error = None
    
    def validate(self):
        self.validate_empty_values()
        self.validate_unique_values()
        self.validate_price()
        
        return self.error
    
    def validate_empty_values(self):
        product_attrs = [
            "code",
            "price",
            "inventory"
        ]
        self.error = validate_empty_values(self.product, product_attrs)
        
        return self.error

    def validate_unique_values(self):
        product = Product.search(self.product.code)
        if product and product is not self.product:
            self.error = repeated_value_error

        return self.error

    def validate_price(self):
        if not self.product.price:
            self.product.price = 0
        try:
            float(self.product.price)
        except ValueError:
            self.error = "Número invalido"

        return self.error
        
