from EnGo.models import validate_empty_values
from EnGo.models.user import User


class ProductionValidation:

    def __init__(self, production):
        self.production = production
        self.error = None
    
    def validate(self):
        self.validate_empty_values()
        self.validate_user_id()
        
        return self.error
    
    def validate_empty_values(self):
        production_attrs = [
            "concept",
            "quantity"
        ]
        self.error = validate_empty_values(self.production, production_attrs)

        return self.error

    def validate_user_id(self):
        user = User.query.get(self.production.user_id)
        if not user:
            self.error = "El empleado que seleccionaste es invalido"
        
        return self.error