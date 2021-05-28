


from EnGo.models.raw_material import RawMaterial
from EnGo.models.consumable import Consumable
from EnGo.models.product import Product


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
    
    def add_consumable(self, consumable_to_add):
        consumable = Consumable.search(consumable_to_add.consumable_name)
        if consumable:
            self.warehouse.add_consumable(consumable)
        else:
            self.add_new_consumable(consumable_to_add)
        
        return self.error
        
    def add_new_consumable(self, consumable):
        self.error = consumable.request.add()
        if not self.error:
            self.warehouse.add_consumable(consumable)
        
    def add_product(self, product_to_add):
        product = Product.search(product_to_add.code)
        if product:
            self.warehouse.add_product(product_to_add)
        else:
            self.add_new_product(product_to_add)
        
        self.error
    
    def add_new_product(self, product):
        self.error = product.request.add()
        if not self.error:
            self.warehouse.add_product(product)
        