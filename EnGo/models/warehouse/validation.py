from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values
from . import Warehouse


class WarehouseValidation:

    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.error = None
    
    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_unique_values()
            
        return self.error
    
    def validate_empty_values(self):
        warehouse_attributes = [
            'name'
        ]
        self.error = validate_empty_values(self.warehouse, warehouse_attributes)
        
        return self.error
    
    def validate_unique_values(self):
        warehouse = Warehouse.search(self.warehouse.name)
        if warehouse and warehouse is not self.warehouse:
            self.error = repeated_value_error
        
        return self.error
