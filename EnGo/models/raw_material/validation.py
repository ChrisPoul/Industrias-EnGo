from . import RawMaterial, raw_material_attributes
from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values




class RawMaterialValidation:

    def __init__(self, raw_material):
        self.raw_material = raw_material
        self.error = None

    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_unique_values()
        
        return self.error
    
    def validate_empty_values(self):
        self.error = validate_empty_values(self.raw_material, raw_material_attributes)

        return self.error
    
    def validate_unique_values(self):
        raw_material = RawMaterial.search(self.raw_material.material_name)
        if raw_material and raw_material is not self.raw_material:
            self.error = repeated_value_error
        
        return self.error