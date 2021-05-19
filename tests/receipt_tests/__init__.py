from tests import Test
from datetime import datetime
from EnGo.models.receipt import Receipt
from EnGo.models.product import Product
from EnGo.models.customer import Customer


class ReceiptTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.receipt = Receipt()
        self.receipt.add()
        self.customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="Test RFC"
        )
        self.customer.add()
        self.product_1 = Product(
            code="Code 1",
            price=10
        )
        self.product_1.add()
        self.product_2 = Product(
            code="Code 2",
            price=10
        )
        self.product_2.add()