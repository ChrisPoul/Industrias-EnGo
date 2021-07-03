from tests import Test
from EnGo.models.product import Product, FinishedProduct

class FinishedProductTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.product = Product(
            warehouse_id=1,
            code="Test Code",
            description="Optional description",
            price=10
        )
        self.product.add()
        self.finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity=1,
            unit="pz"
        )
        self.finished_product.add()