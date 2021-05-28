


from EnGo.models.raw_material import RawMaterial


class WarehouseRequest:

    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.error = None
    
    def add(self):
        error = self.warehouse.validation.validate()
        if not error:
            self.warehouse.add()
        
        return error
    
    def update(self):
        error = self.warehouse.validation.validate()
        if not error:
            self.warehouse.update()
        
        return error
    
    def add_raw_material(self, raw_material_to_add):
        raw_material = RawMaterial.search(raw_material_to_add.material_name)
        if raw_material:
            self.warehouse.add_raw_material(raw_material)
        else:
            self.add_new_raw_material(raw_material_to_add)
        
        return self.error
        
    def add_new_raw_material(self, raw_material):
        self.error = raw_material.request.add()
        if not self.error:
            self.warehouse.add_raw_material(raw_material)
        
        
            


            


