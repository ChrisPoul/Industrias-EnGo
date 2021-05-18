from . import Customer, customer_attributes


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
            self.error = "No se pueden dejar campos vacios"
        
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
        if customers and self.customer not in customers:
            self.error = "Valor ya existente"

        return self.error