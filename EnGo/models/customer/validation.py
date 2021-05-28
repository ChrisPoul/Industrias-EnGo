from . import Customer, customer_attributes
from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values


class CustomerValidation:

    def __init__(self, customer):
        self.customer = customer
        self.error = None
        
    def validate(self):
        self.validate_empty_values()
        self.validate_unique_values()

        return self.error
    
    def validate_empty_values(self):
        non_optional_attributes = []
        for attribute in customer_attributes:
            if attribute != "rfc":
                non_optional_attributes.append(attribute)
        self.error = validate_empty_values(self.customer, non_optional_attributes)
         
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