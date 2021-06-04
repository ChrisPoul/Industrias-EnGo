from . import Product
from EnGo.errors.messages import (
    repeated_value_error
)
from EnGo.models import (
    validate_empty_values, validate_obj_nums
)


class ProductValidation:

    def __init__(self, product):
        self.product = product
        self.error = None
    
    def validate(self):
        self.validate_empty_values()
        self.validate_unique_values()
        if not self.error:
            self.validate_nums()
        
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

    def validate_nums(self):
        product_nums = [
            "price",
            "inventory"
        ]
        self.error = validate_obj_nums(self.product, product_nums)

        return self.error


class SoldProductValidation:

    def __init__(self, sold_product):
        self.sold_product = sold_product
        self.error = None

    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_nums()
        
        return self.error

    def validate_empty_values(self):
        sold_product_attrs = [
            "quantity",
            "unit",
            "price"
        ]
        self.error = validate_empty_values(self.sold_product, sold_product_attrs)

        return self.error

    def validate_nums(self):
        sold_product_nums = [
            "quantity",
            "price"
        ]
        self.error = validate_obj_nums(self.sold_product, sold_product_nums)

        return self.error
