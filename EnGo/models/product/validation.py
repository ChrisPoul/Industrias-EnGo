

class ProductValidation:

    def __init__(self, product):
        self.product = product
        self.error = None
    
    def validate(self):
        self.validate_empty_values()
        
        return self.error
    
    def validate_empty_values(self):
        if self.product.code == "":
            self.error = "No se pueden dejar campos vacios"
        
        return self.error
        
