from . import WarehouseTest
from EnGo.models.warehouse import Warehouse
from EnGo.models.expense import Expense
from EnGo.models.product import Product


class TestAdd(WarehouseTest):

    def test_sould_add_warehouse_given_valid_warehouse(self):
        warehouse = Warehouse(
            name="Valid name"
        )
        warehouse.request.add()

        self.assertIn(warehouse, self.db.session)

    def test_should_not_add_warehouse_given_invalid_warehouse(self):
        warehouse = Warehouse(
            name=""
        )
        warehouse.request.add()
        
        self.assertNotIn(warehouse, self.db.session)


class TestUpdate(WarehouseTest):

    def test_should_update_warehouse_given_valid_changes(self):
        self.warehouse.name = "New name"
        self.warehouse.request.update()
        self.db.session.rollback()

        self.assertEqual(self.warehouse.name, "New name")
    
    def test_should_not_update_warehouse_given_invalid_changes(self):
        self.warehouse.name = ""
        self.warehouse.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.warehouse.name, "")    

