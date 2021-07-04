from . import WarehouseTest
from EnGo.models.warehouse import Warehouse
from EnGo.models.expense import Expense


class TestAdd(WarehouseTest):

    def test_should_add_warehouse(self):
        warehouse = Warehouse(
            name="Another Test Warehouse"
        )
        warehouse.add()

        self.assertIn(warehouse, self.db.session)


class TestUpdate(WarehouseTest):

    def test_should_update_warehouse(self):
        self.warehouse.name = "New name"
        self.warehouse.update()
        self.db.session.rollback()

        self.assertEqual(self.warehouse.name, "New name")


class TestDelete(WarehouseTest):

    def test_should_delete_warehouse(self):
        self.warehouse.delete()

        self.assertNotIn(self.warehouse, self.db.session)


class TestGet(WarehouseTest):

    def test_should_return_warehouse_given_valid_id(self):
        warehouse = Warehouse.get(self.warehouse.id)

        self.assertEqual(warehouse, self.warehouse)


class TestGetAll(WarehouseTest):

    def test_should_return_all_warehouses(self):
        warehouses = Warehouse.get_all()

        self.assertEqual(warehouses, [self.warehouse])


class TestSearch(WarehouseTest):

    def test_should_return_warehouse_given_valid_search_term(self):
        warehouse = Warehouse.search('Test Warehouse')

        self.assertEqual(warehouse, self.warehouse)
