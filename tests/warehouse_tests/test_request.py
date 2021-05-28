from . import WarehouseTest
from EnGo.models.raw_material import RawMaterial
from EnGo.models.warehouse import Warehouse
from EnGo.models.consumable import Consumable
from EnGo.models.product import Product


class TestAdd(WarehouseTest):

    def test_sould_add_warehouse_given_valid_warehouse(self):
        warehouse = Warehouse(
            address="Valid Address"
        )
        warehouse.request.add()

        self.assertIn(warehouse, self.db.session)

    def test_should_not_add_warehouse_given_invalid_warehouse(self):
        warehouse = Warehouse(
            address=""
        )
        warehouse.request.add()
        
        self.assertNotIn(warehouse, self.db.session)


class TestUpdate(WarehouseTest):

    def test_should_update_warehouse_given_valid_changes(self):
        self.warehouse.address = "New Address"
        self.warehouse.request.update()
        self.db.session.rollback()

        self.assertEqual(self.warehouse.address, "New Address")
    
    def test_should_not_update_warehouse_given_invalid_changes(self):
        self.warehouse.address = ""
        self.warehouse.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.warehouse.address, "")


class TestAddRawMaterial(WarehouseTest):

    def test_should_add_raw_material_to_warehouse_given_existent_raw_material(self):
        self.warehouse.request.add_raw_material(self.raw_material)

        self.assertIn(self.raw_material, self.warehouse.raw_materials)
    
    def test_should_add_raw_material_given_valid_new_raw_material(self):
        raw_material = RawMaterial(
            material_name="New Material"
        )
        self.warehouse.request.add_raw_material(raw_material)

        self.assertIn(raw_material, self.warehouse.raw_materials)

    def test_should_not_add_raw_material_given_invalid_new_raw_material(self):
        raw_material = RawMaterial(
            material_name=""
        )
        self.warehouse.request.add_raw_material(raw_material)

        self.assertNotIn(raw_material, self.warehouse.raw_materials)


class TestAddConsumable(WarehouseTest):

    def test_should_add_consumable_to_warehouse_given_existing_consumable(self):
        self.warehouse.request.add_consumable(self.consumable)

        self.assertIn(self.consumable, self.warehouse.consumables)
    
    def test_should_add_consumable_given_valid_new_consumable(self):
        consumable = Consumable(
            consumable_name="New Name"
        )
        self.warehouse.request.add_consumable(consumable)

        self.assertIn(consumable, self.warehouse.consumables)

    def test_should_not_add_consumable_to_warehouse_given_invalid_consumable(self):
        consumable = Consumable(
            consumable_name=""
        )
        self.warehouse.request.add_consumable(consumable)

        self.assertNotIn(consumable, self.warehouse.consumables)
    

class TestAddProduct(WarehouseTest):

    def test_should_add_product_given_valid_existing_product(self):
        self.warehouse.request.add_product(self.product)

        self.assertIn(self.product, self.warehouse.products)
    
    def test_should_product_given_valid_new_product(self):
        product = Product(
            code="New Code"
        )
        self.warehouse.request.add_product(product)

        self.assertIn(product, self.warehouse.products)

    def test_should_not_add_product_given_invalid_product(self):
        product = Product(
            code=""
        )
        self.warehouse.request.add_product(product)

        self.assertNotIn(product, self.warehouse.products)