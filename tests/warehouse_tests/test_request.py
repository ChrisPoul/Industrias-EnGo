from . import WarehouseTest
from EnGo.models.warehouse import Warehouse
from EnGo.models.expense import Expense
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

