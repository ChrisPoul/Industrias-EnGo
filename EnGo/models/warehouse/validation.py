from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values
from EnGo.models.warehouse import Warehouse


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
            'address'
        ]
        self.error = validate_empty_values(self.warehouse, warehouse_attributes)
        
        return self.error
    
    def validate_unique_values(self):
        warehouse = Warehouse.search(self.warehouse.address)
        if warehouse and warehouse is not self.warehouse:
            self.error = repeated_value_error
        
        return self.error
