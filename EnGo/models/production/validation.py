from EnGo.models import validate_empty_values


class ProductionValidation:

    def __init__(self, user_production):
        self.user_production = user_production
        self.error = None
    
    def validate(self):
        self.validate_empty_values()
        
        return self.error
    
    def validate_empty_values(self):
        user_production_attrs = [
            "concept",
            "quantity"
        ]
        self.error = validate_empty_values(self.user_production, user_production_attrs)

        return self.error