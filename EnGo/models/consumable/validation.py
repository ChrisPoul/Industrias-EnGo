from . import Consumable, consumable_attributes
from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values


class ConsumableValidation:

    def __init__(self, consumable):
        self.consumable = consumable
        self.error = None

    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_unique_values()

        return self.error
    
    def validate_empty_values(self):
        self.error = validate_empty_values(self.consumable, consumable_attributes)
        
        return self.error
    
    def validate_unique_values(self):
        consumable = Consumable.search(self.consumable.consumable_name)
        if consumable and consumable is not self.consumable:
            self.error = repeated_value_error

        return self.error