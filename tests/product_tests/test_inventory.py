from . import ProductTest
from EnGo.models.product import FinishedProduct, SoldProduct


class ProductInventoryTest(ProductTest):

    def setUp(self):
        ProductTest.setUp(self)
        self.finished_product = FinishedProduct(
            product_id=self.product.id,
            warehouse_id=1,
            quantity=10,
            unit="pz"
        )
        self.finished_product.add()
        self.sold_product = SoldProduct(
            receipt_id=1,
            product_id=self.product.id,
            quantity=
        )
        