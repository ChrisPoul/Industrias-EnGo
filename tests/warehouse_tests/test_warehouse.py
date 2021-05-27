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
