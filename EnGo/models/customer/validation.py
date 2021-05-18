from . import Customer, customer_attributes


class CustomerValidation:

    def __init__(self, customer):
        self.customer = customer
        self.error = None
        
    def validate(self):
        self.validate_empty_values()
    
    def validate_empty_values(self):
        for attribute in customer_attributes:
            if attribute != "rfc":
                self.validate_empty_value(attribute)
         
        return self.error
    
    def validate_empty_value(self, attribute):
        value = getattr(self.customer, attribute)
        if value == "":
            self.error = "No se pueden dejar campos vacios"
        
        return self.error