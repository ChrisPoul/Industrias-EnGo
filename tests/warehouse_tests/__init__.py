from tests import Test
from EnGo.models.warehouse import Warehouse
from EnGo.models.consumable import Consumable
from EnGo.models.product import Product


class WarehouseTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.warehouse = Warehouse(
            address="Test Address"
        )
        self.warehouse.add()
        self.consumable = Consumable(
            consumable_name="Test Consumable"
        )
        self.consumable.add()
        self.product = Product(
            code="Test Product"
        )
        self.product.add()
