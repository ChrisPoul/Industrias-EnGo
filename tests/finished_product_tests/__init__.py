from tests import Test
from EnGo.models.product import Product, FinishedProduct

class FinishedProductTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.product = Product(
            code="Test Code",
            description="Optional description",
            price=10
        )
        self.product.add()
        self.finished_product = FinishedProduct(
            product_id=self.product.id,
            warehouse_id=1,
            quantity=1,
            unit="pz",
            cost=1
        )
        self.finished_product.add()