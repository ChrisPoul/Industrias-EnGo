from tests import Test
from EnGo.models.product import Product
from EnGo.models.warehouse import Warehouse


class ProductTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.warehouse = Warehouse(
            address="Test Address"
        )
        self.warehouse.add()
        self.product = Product(
            warehouse_id=self.warehouse.id,
            code="Test Code",
            description="Optional description",
            price=10
        )
        self.product.add()
