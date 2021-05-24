from . import Customer, customer_attributes
from EnGo.errors.messages import (
    repeated_value_error, empty_value_error
)


class CustomerValidation:

    def __init__(self, customer):
        self.customer = customer
        self.error = None
        
    def validate(self):
        self.validate_empty_values()
        self.validate_unique_values()

        return self.error
    
    def validate_empty_values(self):
        for attribute in customer_attributes:
            if attribute != "rfc":
                self.validate_empty_value(attribute)
         
        return self.error
    
    def validate_empty_value(self, attribute):
        value = getattr(self.customer, attribute)
        if value == "":
            self.error = empty_value_error
        
        return self.error
    
    def validate_unique_values(self):
        for attribute in customer_attributes:
            if attribute == "rfc":
                self.validate_optional_unique_value(attribute)
        
        return self.error
    
    def validate_optional_unique_value(self, attribute):
        value = getattr(self.customer, attribute)
        if value != "":
            self.validate_unique_value(attribute)
        
        return self.error
    
    def validate_unique_value(self, attribute):
        value = getattr(self.customer, attribute)
        customers = Customer.search(value)
        if customers and customers != [self.customer]:
            self.error = repeated_value_error

        return self.error