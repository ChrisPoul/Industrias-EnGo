from . import WarehouseTest
from EnGo.models.warehouse import Warehouse


class TestAdd(WarehouseTest):

    def test_should_add_warehouse(self):
        warehouse = Warehouse(
            address="Another Test Address"
        )
        warehouse.add()

        self.assertIn(warehouse, self.db.session)


class TestUpdate(WarehouseTest):

    def test_should_update_warehouse(self):
        self.warehouse.address = "New Address"
        self.warehouse.update()
        self.db.session.rollback()

        self.assertEqual(self.warehouse.address, "New Address")


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
        warehouse = Warehouse.search('Test Address')

        self.assertEqual(warehouse, self.warehouse)


class TestAddProduct(WarehouseTest):

    def test_should_add_product_to_warehouse_given_product(self):
        self.warehouse.add_product(self.product)

        self.assertEqual(self.warehouse.products, [self.product])
