from tests import Test
from datetime import datetime
from EnGo.models.receipt import Receipt
from EnGo.models.product import Product
from EnGo.models.customer import Customer


class ReceiptTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="Test RFC"
        )
        self.customer.add()
        self.product_1 = Product(
            warehouse_id=1,
            code="Code 1",
            price=10
        )
        self.product_1.add()
        self.product_2 = Product(
            warehouse_id=1,
            code="Code 2",
            price=10
        )
        self.product_2.add()
        self.receipt = Receipt(
            customer_id=self.customer.id
        )
        self.receipt.add()